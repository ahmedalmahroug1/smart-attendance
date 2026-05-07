"""
_helpers.py — دوال مساعدة مشتركة بين الصفحات
===============================================
يحتوي على عناصر واجهة مستخدم يتم إعادة استخدامها في أكثر من صفحة.
"""

import streamlit as st


def page_header(title: str, subtitle: str):
    """
    عرض ترويسة (عنوان) مُنسّقة أعلى كل صفحة.
    المعاملات:
      - title: العنوان الرئيسي للصفحة (مثلاً "📊 سجل الحضور")
      - subtitle: وصف مختصر يظهر تحت العنوان
    """
    st.markdown(
        f'<div class="page-header"><p class="page-title">{title}</p>'
        f'<p class="page-subtitle">{subtitle}</p></div>',
        unsafe_allow_html=True,
    )
