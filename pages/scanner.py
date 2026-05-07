"""
scanner.py — صفحة مسح رموز QR بالكاميرا
==========================================
تفتح كاميرا الجهاز وتبحث عن رموز QR لتسجيل الحضور تلقائياً.
تدعم وضعين: حصة عادية أو امتحان (مع التحقق من فترة السماح).
"""

import streamlit as st
from datetime import datetime, date, time, timedelta
from database import db_student_exists, db_get_exams_today, db_log_attendance
from pages._helpers import page_header


def render_qr_scanner():
    """عرض صفحة مسح رموز QR."""
    # استيراد مكتبات الكاميرا (داخل الدالة لتجنب خطأ عند عدم وجودها)
    import cv2
    from pyzbar.pyzbar import decode as pyzbar_decode

    page_header("📷 مسح QR", "وجّه كاميرا الجهاز نحو رمز QR لتسجيل الحضور")

    # ── اختيار نوع الجلسة (حصة عادية أو امتحان) ─────────────────────────
    session_type = st.radio("نوع الجلسة", ["📖 حصة عادية", "📝 امتحان"],
                            horizontal=True, key="qr_mode")
    is_exam = session_type == "📝 امتحان"

    # إذا كان الوضع "امتحان" → نحتاج لاختيار الامتحان من القائمة
    exam_data = None
    if is_exam:
        today_exams = db_get_exams_today()  # جلب امتحانات اليوم
        if not today_exams:
            st.warning("⚠️ لا يوجد امتحان مجدول لهذا اليوم.")
            return
        # إنشاء قائمة منسدلة بالامتحانات المتاحة
        exam_labels = {
            f"{e['exam_name']} — {e['start_time']} (سماح {e['grace_period_minutes']} د)": e
            for e in today_exams
        }
        sel_exam_label = st.selectbox("🗓️ اختر الامتحان", list(exam_labels.keys()))
        exam_data = exam_labels[sel_exam_label]

    st.markdown("---")

    # ── أزرار التحكم بالكاميرا ───────────────────────────────────────────
    # حفظ حالة الكاميرا في session_state حتى لا تُفقد عند تحديث الصفحة
    if "camera_running" not in st.session_state:
        st.session_state["camera_running"] = False
    if "last_scanned" not in st.session_state:
        st.session_state["last_scanned"] = None

    c1, c2 = st.columns(2)
    with c1:
        # زر تشغيل الكاميرا
        if st.button("▶️ تشغيل الكاميرا", use_container_width=True, type="primary"):
            st.session_state["camera_running"] = True
            st.session_state["last_scanned"] = None
    with c2:
        # زر إيقاف الكاميرا
        if st.button("⏹️ إيقاف الكاميرا", use_container_width=True):
            st.session_state["camera_running"] = False

    # عناصر نائبة لعرض الصورة والحالة (يتم تحديثها في الحلقة)
    frame_ph = st.empty()    # مكان عرض إطار الكاميرا
    status_ph = st.empty()   # مكان عرض رسائل الحالة

    # ── حلقة الكاميرا الرئيسية ───────────────────────────────────────────
    if st.session_state["camera_running"]:
        cap = cv2.VideoCapture(0)  # فتح الكاميرا الافتراضية (رقم 0)
        if not cap.isOpened():
            st.error("❌ تعذّر فتح الكاميرا.")
            st.session_state["camera_running"] = False
            return

        status_ph.info("📡 جارٍ البحث عن رمز QR…")

        # قراءة الإطارات من الكاميرا حتى يتم إيقافها أو العثور على رمز
        while st.session_state["camera_running"]:
            ret, frame = cap.read()  # قراءة إطار واحد
            if not ret:
                status_ph.warning("⚠️ لم يتم استلام إطار من الكاميرا.")
                break

            # محاولة فك تشفير رموز QR في الإطار الحالي
            decoded_objects = pyzbar_decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8").strip()  # النص المشفر في QR
                if not qr_data:
                    continue

                # رسم إطار أخضر حول رمز QR المكتشف
                pts = obj.polygon
                if len(pts) == 4:
                    for i in range(4):
                        cv2.line(frame, (pts[i].x, pts[i].y),
                                 (pts[(i+1)%4].x, pts[(i+1)%4].y), (0, 255, 0), 3)

                # إيقاف الكاميرا بعد أول مسح ناجح
                st.session_state["camera_running"] = False
                st.session_state["last_scanned"] = qr_data

                # البحث عن الطالب في قاعدة البيانات
                student = db_student_exists(qr_data)
                if not student:
                    status_ph.error(f"❌ لم يتم العثور على طالب بالرمز: {qr_data}")
                    break

                # ── التحقق من فترة السماح (في حالة الامتحان) ──────────
                if is_exam and exam_data:
                    # حساب وقت بداية الامتحان + فترة السماح
                    parts = exam_data["start_time"].split(":")
                    exam_start = datetime.combine(
                        date.today(), time(int(parts[0]), int(parts[1])))
                    deadline = exam_start + timedelta(
                        minutes=exam_data["grace_period_minutes"])
                    now = datetime.now()
                    # إذا تجاوز الوقت الحالي الموعد النهائي → رفض الدخول
                    if now > deadline:
                        status_ph.empty()
                        st.markdown(f"""<div class="attendance-denied">
                            <h3>🚫 الطالب متأخر — تم رفض الدخول</h3>
                            <p>الطالب: <strong>{student['name']}</strong><br>
                            الموعد النهائي: {deadline.strftime('%H:%M')}
                            — الوقت الحالي: {now.strftime('%H:%M')}</p>
                            </div>""", unsafe_allow_html=True)
                        st.error("الطالب متأخر - لا يمكن تسجيل الحضور لانتهاء فترة السماح")
                        break

                # ── تسجيل الحضور في قاعدة البيانات ────────────────────
                db_log_attendance(student["id"], "Present",
                                  is_exam, exam_data["id"] if exam_data else None)
                status_ph.empty()
                label = f"({exam_data['exam_name']})" if is_exam and exam_data else "(حصة)"
                st.markdown(f"""<div class="attendance-success">
                    <h3>✅ تم تسجيل الحضور بنجاح</h3>
                    <p>الطالب: <strong>{student['name']}</strong> {label}</p>
                    </div>""", unsafe_allow_html=True)
                st.balloons()  # تأثير بصري للاحتفال
                break

            # تحويل الإطار من BGR إلى RGB وعرضه
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_ph.image(frame_rgb, channels="RGB", use_container_width=True)

        cap.release()  # تحرير الكاميرا بعد الانتهاء

    # عرض آخر رمز تم مسحه (بعد إيقاف الكاميرا)
    if not st.session_state["camera_running"] and st.session_state.get("last_scanned"):
        st.info(f"🔍 آخر رمز تم مسحه: **{st.session_state['last_scanned']}**")
