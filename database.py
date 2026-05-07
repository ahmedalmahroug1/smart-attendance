"""
database.py — دوال التعامل مع قاعدة البيانات
===============================================
هذا الملف يحتوي على جميع الدوال التي تتواصل مع قاعدة بيانات Supabase.
الجداول المستخدمة:
  - students: جدول الطلبة (الاسم، رمز QR)
  - exams: جدول الامتحانات (الاسم، التاريخ، الوقت، فترة السماح)
  - attendance: جدول الحضور (الطالب، التاريخ، الحالة، نوع الجلسة)
"""

import streamlit as st
from datetime import datetime, date
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY


# ─── إنشاء الاتصال بقاعدة البيانات ──────────────────────────────────────────
# نستخدم cache_resource حتى لا يُنشأ اتصال جديد مع كل تحديث للصفحة
@st.cache_resource
def get_supabase_client() -> Client:
    """إنشاء وإرجاع عميل Supabase — يتم تخزينه مؤقتاً لتجنب إعادة الاتصال."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def _sb():
    """اختصار للحصول على عميل Supabase في كل دالة."""
    return get_supabase_client()


# ─── دوال الطلبة ─────────────────────────────────────────────────────────────

def db_get_all_students() -> list[dict]:
    """جلب جميع الطلبة من جدول students وإرجاعهم كقائمة قواميس."""
    return (_sb().table("students").select("*").execute()).data or []


def db_student_exists(qr_code: str) -> dict | None:
    """
    البحث عن طالب باستخدام رمز QR الخاص به.
    يرجع بيانات الطالب إذا وُجد، أو None إذا لم يُوجد.
    """
    r = _sb().table("students").select("*").eq("qr_code", qr_code).limit(1).execute()
    return r.data[0] if r.data else None


def db_add_student(name: str, qr_code: str) -> bool:
    """
    إضافة طالب جديد إلى قاعدة البيانات.
    المعاملات:
      - name: اسم الطالب
      - qr_code: رمز QR الفريد المولّد تلقائياً
    يرجع True عند النجاح، False عند حدوث خطأ.
    """
    try:
        _sb().table("students").insert({"name": name, "qr_code": qr_code}).execute()
        return True
    except Exception as e:
        st.error(f"❌ خطأ في إضافة الطالب: {e}")
        return False


# ─── دوال الامتحانات ─────────────────────────────────────────────────────────

def db_add_exam(exam_name: str, exam_date: str, start_time: str, grace: int) -> bool:
    """
    إضافة امتحان جديد إلى جدول exams.
    المعاملات:
      - exam_name: اسم الامتحان
      - exam_date: تاريخ الامتحان (نص بصيغة YYYY-MM-DD)
      - start_time: وقت بداية الامتحان (نص بصيغة HH:MM)
      - grace: فترة السماح بالدقائق (المدة المسموحة للتأخير)
    """
    try:
        _sb().table("exams").insert({
            "exam_name": exam_name, "exam_date": exam_date,
            "start_time": start_time, "grace_period_minutes": grace,
        }).execute()
        return True
    except Exception as e:
        st.error(f"❌ خطأ: {e}")
        return False


def db_get_exams_today() -> list[dict]:
    """جلب الامتحانات المجدولة لهذا اليوم فقط."""
    return (_sb().table("exams").select("*")
            .eq("exam_date", str(date.today())).execute()).data or []


def db_get_all_exams() -> list[dict]:
    """جلب جميع الامتحانات مرتبة من الأحدث إلى الأقدم."""
    return (_sb().table("exams").select("*")
            .order("exam_date", desc=True).execute()).data or []


# ─── دوال الحضور ─────────────────────────────────────────────────────────────

def db_log_attendance(student_id: str, status: str = "Present",
                      is_exam: bool = False, exam_id: str | None = None) -> bool:
    """
    تسجيل حضور طالب (إضافة سجل جديد).
    المعاملات:
      - student_id: معرّف الطالب في قاعدة البيانات
      - status: الحالة (Present/Absent/Late)
      - is_exam: هل الجلسة امتحان أم حصة عادية
      - exam_id: معرّف الامتحان (اختياري، فقط إذا كان امتحان)
    """
    try:
        # إنشاء صف البيانات الأساسي
        row = {
            "student_id": student_id,
            "date": str(date.today()),        # تاريخ اليوم
            "status": status,                  # حالة الحضور
            "timestamp": datetime.now().isoformat(),  # الوقت الكامل (تاريخ + ساعة)
            "is_exam": is_exam,               # هل هو امتحان؟
        }
        # إذا كان امتحان، نضيف معرّف الامتحان
        if exam_id:
            row["exam_id"] = exam_id
        _sb().table("attendance").insert(row).execute()
        return True
    except Exception as e:
        st.error(f"❌ خطأ في تسجيل الحضور: {e}")
        return False


def db_upsert_attendance(student_id: str, att_date: str, status: str) -> bool:
    """
    تحديث أو إدراج سجل حضور (upsert).
    إذا كان هناك سجل موجود لنفس الطالب ونفس التاريخ → يتم تحديثه.
    إذا لم يوجد سجل → يتم إنشاء سجل جديد.
    المعاملات:
      - student_id: معرّف الطالب
      - att_date: التاريخ المراد تعديله
      - status: الحالة الجديدة
    """
    try:
        # البحث عن سجل موجود لنفس الطالب ونفس التاريخ
        existing = (_sb().table("attendance").select("id")
                    .eq("student_id", student_id).eq("date", att_date)
                    .limit(1).execute())
        # تجهيز البيانات المراد تحديثها
        payload = {"status": status, "timestamp": datetime.now().isoformat()}
        if existing.data:
            # إذا وُجد سجل → نحدّثه
            _sb().table("attendance").update(payload).eq("id", existing.data[0]["id"]).execute()
        else:
            # إذا لم يُوجد → ننشئ سجل جديد
            payload.update({"student_id": student_id, "date": att_date, "is_exam": False})
            _sb().table("attendance").insert(payload).execute()
        return True
    except Exception as e:
        st.error(f"❌ خطأ في تحديث الحضور: {e}")
        return False


def db_get_attendance_history() -> list[dict]:
    """
    جلب جميع سجلات الحضور مع بيانات الطالب المرتبطة.
    يتم ربط جدول attendance مع جدول students لجلب اسم الطالب ورمز QR.
    النتائج مرتبة من الأحدث إلى الأقدم.
    """
    return (_sb().table("attendance")
            .select("id, date, status, timestamp, is_exam, student_id, students(name, qr_code)")
            .order("timestamp", desc=True).execute()).data or []


def db_count_today_present() -> int:
    """
    حساب عدد الطلبة الحاضرين اليوم.
    نستخدم set لتجنب تكرار نفس الطالب (لو سُجّل أكثر من مرة).
    """
    r = (_sb().table("attendance").select("student_id")
         .eq("date", str(date.today())).eq("status", "Present").execute())
    return len({x["student_id"] for x in (r.data or [])})
