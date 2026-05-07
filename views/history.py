"""
history.py — صفحة سجل الحضور (جدول محوري)
=============================================
تعرض جدول حضور محوري:
  - الصفوف: أسماء الطلبة
  - الأعمدة: التواريخ (الأيام)
  - الخلايا: حالة الحضور (Present / Absent / Late / —)
مع تلوين الخلايا حسب الحالة وعرض ملخص إحصائي.
"""

import streamlit as st
import pandas as pd
from datetime import date
from database import db_get_all_students, db_get_attendance_history, db_count_today_present
from views._helpers import page_header


def render_attendance_history():
    """عرض صفحة سجل الحضور الكامل."""
    page_header("📊 سجل الحضور الكامل", "جدول الحضور: الطلبة كصفوف والأيام كأعمدة")

    # ── بطاقات الإحصائيات في أعلى الصفحة ─────────────────────────────────
    total_students = len(db_get_all_students())     # إجمالي عدد الطلبة
    today_present = db_count_today_present()         # عدد الحاضرين اليوم
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 إجمالي الطلبة", total_students)
    c2.metric("✅ حاضرون اليوم", today_present)
    c3.metric("📅 التاريخ", str(date.today()))

    st.markdown("---")

    # ── فلتر نوع الجلسة ──────────────────────────────────────────────────
    filter_type = st.selectbox("🔎 نوع الجلسة", ["الكل", "حصة عادية", "امتحان"],
                               key="hist_type")

    # جلب جميع سجلات الحضور من قاعدة البيانات
    records = db_get_attendance_history()
    if not records:
        st.info("لا توجد سجلات حضور بعد.")
        return

    # ── تحويل السجلات إلى صفوف مسطحة ─────────────────────────────────────
    rows = []
    for r in records:
        student_info = r.get("students") or {}       # بيانات الطالب المرتبطة
        is_exam = r.get("is_exam", False)             # هل هو امتحان؟
        rows.append({
            "اسم الطالب": student_info.get("name", "—"),
            "النوع": "امتحان" if is_exam else "حصة",
            "التاريخ": r.get("date", ""),
            "الحالة": r.get("status", ""),
        })

    df = pd.DataFrame(rows)

    # تطبيق فلتر نوع الجلسة
    if filter_type == "حصة عادية":
        df = df[df["النوع"] == "حصة"]
    elif filter_type == "امتحان":
        df = df[df["النوع"] == "امتحان"]

    if df.empty:
        st.info("لا توجد سجلات تطابق الفلتر المحدد.")
        return

    # ── إنشاء الجدول المحوري (الطلبة × التواريخ) ─────────────────────────
    # إذا كان لطالب أكثر من سجل في نفس اليوم → نأخذ آخر حالة
    pivot = df.pivot_table(
        index="اسم الطالب",     # الصفوف = أسماء الطلبة
        columns="التاريخ",      # الأعمدة = التواريخ
        values="الحالة",        # القيم = حالة الحضور
        aggfunc="last",         # دالة التجميع = آخر قيمة
    )

    # ترتيب الأعمدة (التواريخ) من الأقدم إلى الأحدث
    pivot = pivot.reindex(sorted(pivot.columns), axis=1)

    # ملء الخلايا الفارغة بعلامة "—" (لا يوجد سجل)
    pivot = pivot.fillna("—")

    # ── تلوين الخلايا حسب الحالة ─────────────────────────────────────────
    def _color_cell(val):
        """إرجاع نمط CSS لتلوين الخلية حسب حالة الحضور."""
        if val == "Present":
            return "background-color: #0d472a; color: #34d399;"   # أخضر
        elif val == "Absent":
            return "background-color: #4a1520; color: #f87171;"   # أحمر
        elif val == "Late":
            return "background-color: #4a3a10; color: #fbbf24;"   # أصفر
        return "color: #94a3b8;"                                   # رمادي (—)

    styled = pivot.style.map(_color_cell)

    # عرض الجدول المحوري الملوّن
    st.dataframe(styled, use_container_width=True, height=450)

    # ── جدول ملخص الحضور لكل طالب ────────────────────────────────────────
    st.markdown("---")
    st.subheader("📈 ملخص الحضور")

    summary_rows = []
    for student in pivot.index:
        # حساب الإحصائيات لكل طالب
        total_days = (pivot.loc[student] != "—").sum()        # عدد الأيام المسجلة
        present = (pivot.loc[student] == "Present").sum()     # أيام الحضور
        absent = (pivot.loc[student] == "Absent").sum()       # أيام الغياب
        late = (pivot.loc[student] == "Late").sum()           # أيام التأخر
        # حساب نسبة الحضور المئوية
        pct = round(present / total_days * 100, 1) if total_days else 0
        summary_rows.append({
            "اسم الطالب": student,
            "أيام الحضور": int(present),
            "أيام الغياب": int(absent),
            "تأخر": int(late),
            "إجمالي الأيام": int(total_days),
            "نسبة الحضور %": pct,
        })

    # ترتيب الملخص حسب نسبة الحضور (الأعلى أولاً)
    summary_df = pd.DataFrame(summary_rows).sort_values("نسبة الحضور %", ascending=False)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
