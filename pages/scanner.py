"""
scanner.py — صفحة مسح رموز QR بالكاميرا
==========================================
تستخدم كاميرا المتصفح عبر st.camera_input لالتقاط صورة رمز QR.
تدعم وضعين: حصة عادية أو امتحان (مع التحقق من فترة السماح).
"""

import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime, date, time, timedelta
from database import db_student_exists, db_get_exams_today, db_log_attendance
from pages._helpers import page_header


def render_qr_scanner():
    """عرض صفحة مسح رموز QR."""
    from pyzbar.pyzbar import decode as pyzbar_decode

    page_header("📷 مسح QR", "التقط صورة لرمز QR لتسجيل الحضور")

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

    # ── التقاط صورة من كاميرا المتصفح ────────────────────────────────────
    # st.camera_input يفتح كاميرا المتصفح (يعمل على السحابة والموبايل)
    camera_photo = st.camera_input("📸 وجّه الكاميرا نحو رمز QR واضغط التقاط")

    if camera_photo is not None:
        # تحويل الصورة الملتقطة إلى مصفوفة numpy لتحليلها
        img = Image.open(camera_photo)
        img_array = np.array(img)

        # محاولة فك تشفير رموز QR في الصورة
        decoded_objects = pyzbar_decode(img_array)

        if not decoded_objects:
            st.warning("⚠️ لم يتم العثور على رمز QR في الصورة. حاول مرة أخرى.")
            return

        # أخذ أول رمز QR مكتشف
        qr_data = decoded_objects[0].data.decode("utf-8").strip()

        if not qr_data:
            st.warning("⚠️ رمز QR فارغ.")
            return

        st.info(f"🔍 تم مسح الرمز: **{qr_data}**")

        # البحث عن الطالب في قاعدة البيانات
        student = db_student_exists(qr_data)
        if not student:
            st.error(f"❌ لم يتم العثور على طالب بالرمز: {qr_data}")
            return

        # ── التحقق من فترة السماح (في حالة الامتحان) ──────────────────
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
                st.markdown(f"""<div class="attendance-denied">
                    <h3>🚫 الطالب متأخر — تم رفض الدخول</h3>
                    <p>الطالب: <strong>{student['name']}</strong><br>
                    الموعد النهائي: {deadline.strftime('%H:%M')}
                    — الوقت الحالي: {now.strftime('%H:%M')}</p>
                    </div>""", unsafe_allow_html=True)
                return

        # ── تسجيل الحضور في قاعدة البيانات ────────────────────────────
        db_log_attendance(student["id"], "Present",
                          is_exam, exam_data["id"] if exam_data else None)
        label = f"({exam_data['exam_name']})" if is_exam and exam_data else "(حصة)"
        st.markdown(f"""<div class="attendance-success">
            <h3>✅ تم تسجيل الحضور بنجاح</h3>
            <p>الطالب: <strong>{student['name']}</strong> {label}</p>
            </div>""", unsafe_allow_html=True)
        st.balloons()  # تأثير بصري للاحتفال
