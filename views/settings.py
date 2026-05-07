"""
settings.py — صفحة الإعدادات (جدولة الامتحانات)
==================================================
تتيح للمسؤول إضافة امتحانات جديدة مع تحديد:
  - اسم الامتحان
  - التاريخ ووقت البدء
  - فترة السماح بالتأخير (بالدقائق)
كما تعرض قائمة بجميع الامتحانات المجدولة.
"""

import streamlit as st
import pandas as pd
from datetime import date, time
from database import db_add_exam, db_get_all_exams
from views._helpers import page_header


def render_settings():
    """عرض صفحة الإعدادات وجدولة الامتحانات."""
    page_header("⚙️ الإعدادات", "جدولة الامتحانات وإدارة مواعيدها")

    # ── نموذج إضافة امتحان جديد ──────────────────────────────────────────
    st.markdown("#### 🗓️ جدولة امتحان جديد")
    with st.form("add_exam_form", clear_on_submit=True):
        # حقل اسم الامتحان
        exam_name = st.text_input("📝 اسم الامتحان", placeholder="مثلاً: امتحان منتصف الفصل")
        # حقل تاريخ الامتحان
        exam_date = st.date_input("📅 تاريخ الامتحان", value=date.today())
        # حقل وقت البدء (افتراضياً 8:00 صباحاً)
        exam_time = st.time_input("⏰ وقت البدء", value=time(8, 0))
        # حقل فترة السماح (من 0 إلى 120 دقيقة، افتراضياً 15)
        grace = st.number_input("⏳ فترة السماح (دقائق)", min_value=0, max_value=120, value=15)

        # زر جدولة الامتحان
        if st.form_submit_button("جدولة الامتحان 🗓️", use_container_width=True, type="primary"):
            if not exam_name:
                st.warning("⚠️ يرجى إدخال اسم الامتحان.")
            elif db_add_exam(exam_name.strip(), str(exam_date), str(exam_time), int(grace)):
                st.success("✅ تمت جدولة الامتحان بنجاح!")

    # ── عرض قائمة الامتحانات المجدولة ────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📋 الامتحانات المجدولة")
    all_exams = db_get_all_exams()
    if all_exams:
        # تحويل البيانات إلى جدول مُنسّق
        rows = [{
            "الامتحان": e["exam_name"],
            "التاريخ": e["exam_date"],
            "وقت البدء": e["start_time"],
            "فترة السماح": f"{e['grace_period_minutes']} د"
        } for e in all_exams]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("لا يوجد امتحانات مجدولة بعد.")
