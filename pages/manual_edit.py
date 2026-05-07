"""
manual_edit.py — صفحة التعديل اليدوي للحضور
==============================================
تتيح للمسؤول تعديل حالة حضور طالب معين في تاريخ محدد يدوياً.
مفيدة لتصحيح الأخطاء أو تسجيل حضور متأخر.
"""

import streamlit as st
from datetime import date
from database import db_get_all_students, db_upsert_attendance
from pages._helpers import page_header


def render_manual_edit():
    """عرض صفحة التعديل اليدوي للحضور."""
    page_header("✏️ تعديل الحضور يدوياً", "حدّد الطالب والتاريخ والحالة لتعديل سجل الحضور")

    # جلب قائمة الطلبة من قاعدة البيانات
    students = db_get_all_students()
    if not students:
        st.warning("⚠️ لا يوجد طلبة مسجّلون. أضف طلبة أولاً.")
        return

    # إنشاء قائمة منسدلة بأسماء الطلبة مع رموزهم
    # القاموس يربط النص المعروض بمعرّف الطالب في قاعدة البيانات
    stu_map = {f"{s['name']}  ({s['qr_code']})": s["id"] for s in students}
    sel_stu = st.selectbox("👤 اختر الطالب", list(stu_map.keys()))

    # اختيار التاريخ (افتراضياً تاريخ اليوم)
    att_date = st.date_input("📅 تاريخ الحضور", value=date.today())

    # اختيار الحالة (حاضر / غائب / متأخر)
    status = st.selectbox("📌 الحالة", ["Present", "Absent", "Late"])

    # زر تحديث الحضور
    if st.button("تحديث الحضور 🔄", use_container_width=True, type="primary"):
        # تحديث أو إدراج سجل الحضور (upsert)
        if db_upsert_attendance(stu_map[sel_stu], str(att_date), status):
            st.success("✅ تم تحديث سجل الحضور بنجاح!")
