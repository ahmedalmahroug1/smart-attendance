"""
login.py — صفحة تسجيل الدخول
===============================
تعرض واجهة تسجيل الدخول. بيانات الدخول: admin / admin123
"""

import streamlit as st
from styles import inject_login_styles


def render_login_page():
    """عرض صفحة تسجيل الدخول."""
    # حقن أنماط CSS الخاصة بصفحة الدخول
    inject_login_styles()

    # بطاقة تسجيل الدخول (HTML مخصص)
    st.markdown("""<div class="login-wrapper"><div class="login-card">
    <span class="login-icon">🎓</span><h1>نظام الحضور الذكي</h1>
    <p class="subtitle">Smart Attendance System — تسجيل الدخول</p>
    </div></div>""", unsafe_allow_html=True)

    # حقول الإدخال في العمود الأوسط
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("---")
        username = st.text_input("👤 اسم المستخدم", placeholder="admin")
        password = st.text_input("🔒 كلمة المرور", type="password", placeholder="••••••")
        if st.button("تسجيل الدخول 🚀", use_container_width=True, type="primary"):
            if username == "admin" and password == "admin123":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
