"""
app.py — نقطة الدخول الرئيسية للتطبيق
========================================
نظام الحضور الذكي — Smart Attendance System
هذا الملف هو الملف الرئيسي الذي يتم تشغيله عبر: streamlit run app.py
يقوم بـ:
  1. ضبط إعدادات الصفحة (العنوان، الأيقونة، التخطيط)
  2. حقن الأنماط (CSS) العامة
  3. التحقق من تسجيل الدخول (بوابة المصادقة)
  4. عرض الشريط الجانبي للتنقل بين الصفحات
  5. توجيه المستخدم إلى الصفحة المختارة
"""

import streamlit as st

# ── استيراد دوال حقن الأنماط (CSS) ──────────────────────────────────────────
from styles import inject_global_styles, inject_dashboard_styles

# ── استيراد صفحات التطبيق ────────────────────────────────────────────────────
from pages.login import render_login_page          # صفحة تسجيل الدخول
from pages.scanner import render_qr_scanner        # صفحة مسح رموز QR
from pages.students import render_add_students     # صفحة إضافة الطلبة
from pages.history import render_attendance_history # صفحة سجل الحضور
from pages.manual_edit import render_manual_edit   # صفحة التعديل اليدوي
from pages.settings import render_settings         # صفحة الإعدادات

def main():
    """الدالة الرئيسية — يتم استدعاؤها عند تشغيل التطبيق."""

    # ── ضبط إعدادات الصفحة ───────────────────────────────────────────────
    # يجب أن يكون هذا أول أمر Streamlit في التطبيق
    st.set_page_config(
        page_title="نظام الحضور الذكي",  # العنوان الذي يظهر في تبويب المتصفح
        page_icon="🎓",                   # الأيقونة في تبويب المتصفح
        layout="wide",                    # تخطيط عريض يستغل كامل الشاشة
        initial_sidebar_state="expanded"  # الشريط الجانبي مفتوح افتراضياً
    )

    # حقن الأنماط العامة (الخطوط + إخفاء عناصر Streamlit الافتراضية)
    inject_global_styles()

    # إخفاء قائمة التنقل التلقائية لـ Streamlit (نستخدم قائمة مخصصة)
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # ── بوابة المصادقة ───────────────────────────────────────────────────
    # إذا لم يكن المستخدم مسجل الدخول → نعرض صفحة تسجيل الدخول ونتوقف
    if not st.session_state.get("authenticated"):
        render_login_page()
        return

    # ── المستخدم مسجل الدخول → عرض لوحة التحكم ──────────────────────────
    # حقن أنماط لوحة التحكم (الشريط الجانبي، البطاقات، الأزرار...)
    inject_dashboard_styles()

    # ── الشريط الجانبي (القائمة الرئيسية) ────────────────────────────────
    with st.sidebar:
        # عنوان التطبيق في أعلى الشريط الجانبي
        st.markdown("""<div class="sidebar-title">
            <h2>🎓 نظام الحضور الذكي</h2>
            <p>Smart Attendance</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")  # خط فاصل

        # أزرار التنقل بين الصفحات (راديو = خيار واحد فقط في كل مرة)
        page = st.radio("القائمة", [
            "📷 مسح QR",        # صفحة مسح رموز QR بالكاميرا
            "➕ إضافة طلبة",    # صفحة إضافة طلبة جدد
            "📊 سجل الحضور",   # صفحة عرض سجلات الحضور
            "✏️ تعديل يدوي",   # صفحة تعديل الحضور يدوياً
            "⚙️ الإعدادات"     # صفحة إعدادات الامتحانات
        ], label_visibility="collapsed")  # إخفاء عنوان "القائمة"

        st.markdown("---")  # خط فاصل

        # زر تسجيل الخروج
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state["authenticated"] = False  # إلغاء المصادقة
            st.rerun()  # إعادة تحميل الصفحة (ستظهر صفحة تسجيل الدخول)

    # ── توجيه المستخدم إلى الصفحة المختارة ───────────────────────────────
    # قاموس يربط اسم كل صفحة بالدالة التي تعرضها
    pages = {
        "📷 مسح QR": render_qr_scanner,
        "➕ إضافة طلبة": render_add_students,
        "📊 سجل الحضور": render_attendance_history,
        "✏️ تعديل يدوي": render_manual_edit,
        "⚙️ الإعدادات": render_settings,
    }
    # استدعاء الدالة المناسبة حسب اختيار المستخدم
    pages[page]()


# ── نقطة الدخول ──────────────────────────────────────────────────────────────
# هذا الشرط يضمن أن الدالة main() تُستدعى فقط عند تشغيل الملف مباشرة
if __name__ == "__main__":
    main()
