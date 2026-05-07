"""
students.py — صفحة إضافة الطلبة
==================================
تتيح إضافة طالب جديد مع توليد رمز QR فريد تلقائياً.
كما تعرض قائمة بجميع الطلبة المسجّلين مع إمكانية طباعة رموز QR.
"""

import streamlit as st
import pandas as pd
import base64
import uuid as uuid_mod
from database import db_add_student, db_get_all_students
from qr_utils import generate_qr_image, qr_card_html, qr_to_b64
from views._helpers import page_header


def render_add_students():
    """عرض صفحة إضافة الطلبة."""
    page_header("➕ إضافة طلبة", "أضف طالباً جديداً — سيتم توليد رمز QR تلقائياً")

    # ── نموذج إضافة طالب جديد ────────────────────────────────────────────
    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input("📝 اسم الطالب", placeholder="مثلاً: أحمد محمد")
        if st.form_submit_button("إضافة الطالب وتوليد QR ✅",
                                  use_container_width=True, type="primary"):
            if not name:
                st.warning("⚠️ يرجى إدخال اسم الطالب.")
            else:
                # توليد رمز QR فريد (STU- متبوع بـ 8 أحرف عشوائية)
                qr_code = f"STU-{uuid_mod.uuid4().hex[:8].upper()}"
                # حفظ الطالب في قاعدة البيانات
                if db_add_student(name.strip(), qr_code):
                    # حفظ بيانات آخر طالب مُضاف لعرض رمز QR الخاص به
                    st.session_state["last_added_student"] = {
                        "name": name.strip(), "qr_code": qr_code}
                    st.success(f"✅ تمت إضافة الطالب **{name}** — الرمز: `{qr_code}`")
                    st.balloons()

    # ── عرض رمز QR لآخر طالب تمت إضافته ──────────────────────────────────
    if st.session_state.get("last_added_student"):
        stu = st.session_state["last_added_student"]
        # توليد صورة QR وتحويلها إلى base64 للعرض في HTML
        img_bytes = generate_qr_image(stu["qr_code"])
        img_b64 = base64.b64encode(img_bytes).decode()

        # عرض بطاقة QR مُنسّقة
        st.markdown(qr_card_html(img_b64, stu["name"], stu["qr_code"]),
                    unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            # زر تحميل صورة QR كملف PNG
            st.download_button("⬇️ تحميل QR كصورة", data=img_bytes,
                               file_name=f"QR_{stu['qr_code']}.png",
                               mime="image/png", use_container_width=True)
        with c2:
            # زر طباعة QR — يفتح نافذة جديدة ويطبعها مباشرة
            print_js = f"""
            <script>function printQR(){{var w=window.open('','_blank');
            w.document.write('<html><head><title>QR - {stu["name"]}</title>\
<style>body{{font-family:Cairo,sans-serif;text-align:center;padding:2rem}}</style>\
</head><body><img src="data:image/png;base64,{img_b64}" width="300"/>\
<h2>{stu["name"]}</h2><p>رمز: {stu["qr_code"]}</p></body></html>');
            w.document.close();w.print();}}</script>
            <button onclick="printQR()" style="width:100%;padding:.6rem;border-radius:12px;
                background:linear-gradient(135deg,rgba(108,99,255,.15),rgba(108,99,255,.06));
                color:#a78bfa;border:1px solid rgba(108,99,255,.15);font-size:1rem;
                font-family:Cairo,sans-serif;cursor:pointer;font-weight:600;">🖨️ طباعة QR</button>"""
            st.markdown(print_js, unsafe_allow_html=True)

    # ── عرض قائمة جميع الطلبة المسجّلين ──────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📋 الطلبة المسجّلون")
    students = db_get_all_students()
    if students:
        # تحويل البيانات إلى جدول وعرضه
        df = pd.DataFrame(students)[["name", "qr_code"]]
        df.columns = ["اسم الطالب", "رمز QR"]
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ── زر طباعة جميع رموز QR مرة واحدة ─────────────────────────
        st.markdown("---")
        if st.button("🖨️ طباعة جميع رموز QR", use_container_width=True):
            # بناء بطاقات HTML لكل طالب
            cards = ""
            for s in students:
                ib = qr_to_b64(s["qr_code"])
                cards += (f'<div style="display:inline-block;text-align:center;margin:15px;'
                          f'border:1px solid #ddd;border-radius:12px;padding:15px;width:220px;">'
                          f'<img src="data:image/png;base64,{ib}" width="180"/>'
                          f'<p style="font-weight:700;margin:.5rem 0 .1rem;">{s["name"]}</p>'
                          f'<p style="color:#888;font-size:.85rem;margin:0;">{s["qr_code"]}</p></div>')
            # فتح نافذة طباعة تحتوي على جميع البطاقات
            st.markdown(
                f'<script>(function(){{var w=window.open("","_blank");w.document.write(\''
                f'<html><head><title>QR Codes</title><style>body{{font-family:Cairo,sans-serif;'
                f'text-align:center;padding:1rem}}@media print{{div{{page-break-inside:avoid}}}}'
                f'</style></head><body>{cards}</body></html>\');w.document.close();w.print();}})();'
                f'</script>', unsafe_allow_html=True)
    else:
        st.info("لا يوجد طلبة مسجّلون بعد.")
