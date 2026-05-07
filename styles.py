"""
styles.py — أنماط CSS الخاصة بالتطبيق
========================================
هذا الملف يحتوي على جميع أنماط CSS المستخدمة في التطبيق.
يتم تقسيم الأنماط إلى أقسام:
  1. استيراد الخطوط (Google Fonts)
  2. إخفاء عناصر Streamlit الافتراضية + السمة العامة
  3. أنماط صفحة تسجيل الدخول
  4. أنماط لوحة التحكم (الشريط الجانبي، البطاقات، الأزرار...)
"""

# ─── استيراد خطوط Google ─────────────────────────────────────────────────────
# نستخدم خط Cairo للعربية و Inter للإنجليزية
FONT_IMPORT = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
</style>
"""

# ─── إخفاء عناصر Streamlit الافتراضية + السمة العامة ─────────────────────────
HIDE_STREAMLIT_STYLE = """
<style>
    /* إخفاء القائمة والهيدر والفوتر الافتراضية لـ Streamlit */
    #MainMenu, header, footer {visibility: hidden !important; height: 0 !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}

    /* ── الخط والألوان العامة ─────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Cairo', 'Inter', sans-serif !important;
    }

    /* تمرير سلس بين الأقسام */
    html {scroll-behavior: smooth;}

    /* خلفية التطبيق — تدرج داكن */
    .stApp {
        background: linear-gradient(160deg, #0a0c14 0%, #0f1221 30%, #141830 60%, #0f1221 100%);
    }

    /* تقليل المسافة العلوية الافتراضية */
    .block-container {
        padding-top: 2rem !important;
    }
</style>
"""

# ─── أنماط صفحة تسجيل الدخول ─────────────────────────────────────────────────
LOGIN_PAGE_CSS = """
<style>
    /* إخفاء الشريط الجانبي في صفحة تسجيل الدخول */
    section[data-testid="stSidebar"] {display: none !important;}

    /* حاوية تسجيل الدخول — توسيط عمودي وأفقي */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 82vh;
        perspective: 1000px;  /* تأثير ثلاثي الأبعاد */
    }

    /* بطاقة تسجيل الدخول — تصميم زجاجي (glassmorphism) */
    .login-card {
        background: linear-gradient(145deg, rgba(26,28,42,.95), rgba(34,37,52,.9));
        backdrop-filter: blur(20px);               /* تأثير الضبابية */
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem 2.8rem;
        width: 100%;
        max-width: 440px;
        box-shadow:
            0 25px 80px rgba(0, 0, 0, .6),          /* ظل خارجي */
            0 0 0 1px rgba(108, 99, 255, .1),       /* حدود رفيعة */
            0 0 60px rgba(108, 99, 255, .06),       /* توهج */
            inset 0 1px 0 rgba(255, 255, 255, .04); /* ضوء داخلي علوي */
        text-align: center;
        animation: cardFloat 0.8s ease-out;          /* تأثير ظهور البطاقة */
        position: relative;
        overflow: hidden;
    }

    /* توهج خلف البطاقة (عنصر زخرفي) */
    .login-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 50% 50%,
            rgba(108, 99, 255, .06) 0%,
            transparent 60%);
        pointer-events: none;  /* لا يتفاعل مع النقر */
    }

    /* عنوان البطاقة */
    .login-card h1 {
        font-size: 2rem;
        color: #fff;
        margin-bottom: .3rem;
        font-weight: 800;
        letter-spacing: -.5px;
        text-shadow: 0 2px 10px rgba(108, 99, 255, .3);
    }

    /* العنوان الفرعي */
    .login-card .subtitle {
        color: #8b8fa3;
        font-size: .92rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* أيقونة القبعة الأكاديمية */
    .login-icon {
        font-size: 4rem;
        margin-bottom: 1.2rem;
        display: block;
        filter: drop-shadow(0 4px 12px rgba(108, 99, 255, .4));
        animation: iconPulse 2.5s ease-in-out infinite;  /* نبض مستمر */
    }

    /* تأثير ظهور البطاقة من الأسفل */
    @keyframes cardFloat {
        from {opacity: 0; transform: translateY(30px) scale(0.97);}
        to   {opacity: 1; transform: translateY(0) scale(1);}
    }

    /* تأثير نبض الأيقونة */
    @keyframes iconPulse {
        0%, 100% {transform: scale(1);}
        50%      {transform: scale(1.08);}
    }

    /* تنسيق حقول الإدخال في صفحة الدخول */
    .login-wrapper ~ div input {
        background: rgba(20, 22, 36, .8) !important;
        border: 1px solid rgba(108, 99, 255, .2) !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 0.7rem 1rem !important;
        transition: border-color .3s, box-shadow .3s !important;
    }

    /* تأثير التركيز على حقول الإدخال */
    .login-wrapper ~ div input:focus {
        border-color: rgba(108, 99, 255, .5) !important;
        box-shadow: 0 0 20px rgba(108, 99, 255, .15) !important;
    }
</style>
"""

# ─── أنماط لوحة التحكم الرئيسية ──────────────────────────────────────────────
DASHBOARD_CSS = """
<style>
    /* ── الشريط الجانبي ──────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0f1a 0%, #141830 50%, #0d0f1a 100%) !important;
        border-right: 1px solid rgba(108, 99, 255, .08);  /* خط فاصل يمين */
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    /* عنوان الشريط الجانبي */
    .sidebar-title {
        text-align: center;
        padding: 0.5rem 0 1rem;
    }
    .sidebar-title h2 {
        font-size: 1.3rem;
        font-weight: 800;
        /* تدرج لوني للنص */
        background: linear-gradient(135deg, #6c63ff, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .sidebar-title p {
        color: #5a5f7a;
        font-size: .75rem;
        margin: .3rem 0 0;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* أزرار الراديو في الشريط الجانبي (قائمة التنقل) */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 4px !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 1rem !important;
        padding: 0.6rem 1rem !important;
        border-radius: 12px !important;
        transition: all .25s ease !important;
        margin: 0 !important;
    }
    /* تأثير المرور فوق عناصر القائمة */
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(108, 99, 255, .08) !important;
    }
    /* تنسيق العنصر المختار (خط جانبي بنفسجي) */
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"],
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[aria-checked="true"] {
        background: linear-gradient(135deg, rgba(108,99,255,.15), rgba(108,99,255,.06)) !important;
        border-left: 3px solid #6c63ff !important;
    }

    /* الخط الفاصل في الشريط الجانبي */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(108, 99, 255, .1) !important;
        margin: 1rem 0 !important;
    }

    /* ── بطاقات الإحصائيات (Metric Cards) ────────────────── */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(30,32,54,.8), rgba(38,41,68,.6));
        border: 1px solid rgba(108, 99, 255, .1);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        backdrop-filter: blur(10px);
        transition: transform .3s ease, box-shadow .3s ease;
    }
    /* تأثير الرفع عند المرور */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(108, 99, 255, .12);
    }
    /* عنوان البطاقة */
    div[data-testid="stMetric"] label {
        color: #6b7094 !important;
        font-size: .85rem !important;
        font-weight: 500 !important;
        letter-spacing: .5px;
    }
    /* القيمة الرقمية في البطاقة */
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #fff !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
    }

    /* ── الأزرار ──────────────────────────────────────────── */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Cairo', sans-serif !important;
        letter-spacing: .3px;
        transition: all .3s ease !important;
        border: none !important;
    }
    /* الزر الأساسي (بنفسجي) */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #6c63ff, #5a52d5) !important;
        box-shadow: 0 6px 20px rgba(108, 99, 255, .3) !important;
    }
    /* تأثير المرور على الزر الأساسي */
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #7b73ff, #6c63ff) !important;
        box-shadow: 0 8px 30px rgba(108, 99, 255, .4) !important;
        transform: translateY(-2px);
    }
    /* الزر الثانوي (شفاف مع حدود) */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="stBaseButton-secondary"] {
        background: rgba(108, 99, 255, .08) !important;
        color: #a78bfa !important;
        border: 1px solid rgba(108, 99, 255, .15) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover {
        background: rgba(108, 99, 255, .15) !important;
    }

    /* ── حقول الإدخال ─────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(20, 22, 40, .6) !important;
        border: 1px solid rgba(108, 99, 255, .15) !important;
        border-radius: 12px !important;
        color: #e6e6e6 !important;
        transition: all .3s ease !important;
    }
    /* تأثير التركيز على حقول الإدخال */
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #6c63ff !important;
        box-shadow: 0 0 0 3px rgba(108, 99, 255, .1) !important;
    }

    /* القوائم المنسدلة */
    .stSelectbox > div > div {
        background: rgba(20, 22, 40, .6) !important;
        border: 1px solid rgba(108, 99, 255, .15) !important;
        border-radius: 12px !important;
    }

    /* حقل اختيار التاريخ */
    .stDateInput > div > div {
        background: rgba(20, 22, 40, .6) !important;
        border: 1px solid rgba(108, 99, 255, .15) !important;
        border-radius: 12px !important;
    }

    /* ── الجداول (DataFrames) ─────────────────────────────── */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden;
        border: 1px solid rgba(108, 99, 255, .1) !important;
    }

    /* ── التنبيهات ────────────────────────────────────────── */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }

    /* ── لافتة نجاح تسجيل الحضور ─────────────────────────── */
    .attendance-success {
        background: linear-gradient(135deg, rgba(46,204,113,.1), rgba(46,204,113,.03));
        border: 1px solid rgba(46,204,113,.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        animation: fadeSlideIn .5s ease-out;  /* تأثير ظهور */
    }
    .attendance-success h3 {
        color: #2ecc71;
        margin: 0 0 .4rem;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .attendance-success p {
        color: #b0b3c5;
        margin: 0;
        font-size: .95rem;
    }

    /* ── لافتة رفض الدخول (تأخر في الامتحان) ─────────────── */
    .attendance-denied {
        background: linear-gradient(135deg, rgba(231,76,60,.1), rgba(231,76,60,.03));
        border: 1px solid rgba(231,76,60,.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        animation: shakeIn .5s ease-out;  /* تأثير اهتزاز */
    }
    .attendance-denied h3 {
        color: #e74c3c;
        margin: 0 0 .4rem;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .attendance-denied p {
        color: #b0b3c5;
        margin: 0;
        font-size: .95rem;
    }

    /* ── عناوين الصفحات ───────────────────────────────────── */
    .page-header {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(108, 99, 255, .08);
    }
    .page-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #fff;
        margin: 0 0 .3rem;
        display: flex;
        align-items: center;
        gap: .5rem;
    }
    .page-subtitle {
        font-size: .95rem;
        color: #6b7094;
        margin: 0;
        font-weight: 400;
    }

    /* ── بطاقات الأقسام ───────────────────────────────────── */
    .section-card {
        background: linear-gradient(145deg, rgba(26,28,42,.7), rgba(20,22,36,.5));
        border: 1px solid rgba(108, 99, 255, .08);
        border-radius: 18px;
        padding: 1.8rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    .section-card h4 {
        color: #c4c7de;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* ── شارات الحالة (حاضر / غائب / متأخر) ──────────────── */
    .badge {
        display: inline-block;
        padding: .25rem .75rem;
        border-radius: 20px;
        font-size: .8rem;
        font-weight: 600;
    }
    .badge-present {background: rgba(46,204,113,.15); color: #2ecc71;}   /* أخضر */
    .badge-absent  {background: rgba(231,76,60,.15);  color: #e74c3c;}   /* أحمر */
    .badge-late    {background: rgba(243,156,18,.15);  color: #f39c12;}   /* برتقالي */

    /* ── تأثيرات الحركة ───────────────────────────────────── */
    /* ظهور سلس من الأسفل */
    @keyframes fadeSlideIn {
        from {opacity: 0; transform: translateY(15px);}
        to   {opacity: 1; transform: translateY(0);}
    }

    /* اهتزاز (للأخطاء والرفض) */
    @keyframes shakeIn {
        0%   {opacity: 0; transform: translateX(-10px);}
        25%  {transform: translateX(8px);}
        50%  {transform: translateX(-5px);}
        75%  {transform: translateX(3px);}
        100% {opacity: 1; transform: translateX(0);}
    }

    /* ── القوائم القابلة للطي (Expander) ──────────────────── */
    .streamlit-expanderHeader {
        background: rgba(20, 22, 40, .5) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }

    /* ── التبويبات (Tabs) ─────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 600;
    }

    /* ── النماذج (Forms) ──────────────────────────────────── */
    [data-testid="stForm"] {
        background: linear-gradient(145deg, rgba(26,28,42,.5), rgba(20,22,36,.3));
        border: 1px solid rgba(108, 99, 255, .08);
        border-radius: 18px;
        padding: 1.8rem;
    }

    /* ── أزرار الراديو الأفقية ────────────────────────────── */
    .stRadio > div[role="radiogroup"] {
        gap: 6px !important;
    }
</style>
"""


# ─── دوال حقن الأنماط في التطبيق ─────────────────────────────────────────────

def inject_global_styles():
    """
    حقن الأنماط العامة (الخطوط + إخفاء عناصر Streamlit).
    يتم استدعاؤها مرة واحدة في بداية main().
    """
    import streamlit as st
    st.markdown(FONT_IMPORT, unsafe_allow_html=True)
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)


def inject_login_styles():
    """حقن أنماط CSS الخاصة بصفحة تسجيل الدخول."""
    import streamlit as st
    st.markdown(LOGIN_PAGE_CSS, unsafe_allow_html=True)


def inject_dashboard_styles():
    """حقن أنماط CSS الخاصة بلوحة التحكم (بعد تسجيل الدخول)."""
    import streamlit as st
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
