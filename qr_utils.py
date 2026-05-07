"""
qr_utils.py — أدوات توليد رموز QR
=====================================
هذا الملف يحتوي على دوال توليد صور رموز QR وتحويلها
إلى صيغة مناسبة للعرض في واجهة المستخدم.
"""

import io       # للتعامل مع تدفقات البيانات في الذاكرة
import base64   # لتحويل الصور إلى نص base64 للعرض في HTML
import qrcode   # مكتبة توليد رموز QR


def generate_qr_image(data: str) -> bytes:
    """
    توليد صورة رمز QR بصيغة PNG وإرجاعها كبيانات خام (bytes).
    المعاملات:
      - data: النص المراد تشفيره في رمز QR (مثلاً رمز الطالب)
    الخطوات:
      1. إنشاء كائن QR بإعدادات محددة
      2. إضافة البيانات وتوليد المصفوفة
      3. تحويل المصفوفة إلى صورة PNG
      4. حفظ الصورة في الذاكرة وإرجاع البيانات الخام
    """
    # إنشاء كائن QR مع ضبط الإعدادات
    qr = qrcode.QRCode(
        version=1,                                    # حجم المصفوفة (1 = أصغر حجم)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # أعلى مستوى تصحيح أخطاء
        box_size=10,                                  # حجم كل مربع بالبكسل
        border=4                                      # عرض الحدود البيضاء
    )
    qr.add_data(data)       # إضافة البيانات المراد تشفيرها
    qr.make(fit=True)       # توليد المصفوفة مع ضبط الحجم تلقائياً

    # تحويل المصفوفة إلى صورة بألوان مخصصة
    img = qr.make_image(fill_color="#1a1c25", back_color="white").convert("RGB")

    # حفظ الصورة في ذاكرة مؤقتة (بدلاً من ملف) وإرجاع البيانات
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def qr_card_html(img_b64: str, student_name: str, qr_code: str) -> str:
    """
    إنشاء بطاقة HTML مُنسّقة لعرض رمز QR مع اسم الطالب.
    المعاملات:
      - img_b64: صورة QR مشفّرة بصيغة base64
      - student_name: اسم الطالب
      - qr_code: رمز QR النصي
    يُرجع: نص HTML جاهز للعرض في Streamlit
    """
    return f"""
    <div style="text-align:center; padding:1.5rem;
         background:linear-gradient(145deg,rgba(26,28,42,.7),rgba(20,22,36,.5));
         border:1px solid rgba(108,99,255,.12); border-radius:18px; margin:1rem 0;">
        <img src="data:image/png;base64,{img_b64}" width="220" style="border-radius:12px;"/>
        <p style="color:#fff; font-size:1.2rem; font-weight:700; margin:.8rem 0 .2rem;">{student_name}</p>
        <p style="color:#8b8fa3; font-size:.9rem; margin:0;">رمز: {qr_code}</p>
    </div>
    """


def qr_to_b64(data: str) -> str:
    """
    دالة مختصرة: توليد رمز QR وتحويله مباشرة إلى نص base64.
    تُستخدم عند الحاجة لتضمين الصورة في HTML مباشرة.
    """
    return base64.b64encode(generate_qr_image(data)).decode()
