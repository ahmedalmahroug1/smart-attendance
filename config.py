"""
config.py — إعدادات الاتصال بقاعدة البيانات
==============================================
هذا الملف يحتوي على رابط ومفتاح الاتصال بقاعدة بيانات Supabase.
يتم استيراد هذه القيم في ملف database.py لإنشاء الاتصال.
"""

# رابط مشروع Supabase (يتم الحصول عليه من لوحة تحكم Supabase)
SUPABASE_URL = "https://ztwmibtncsummztpescg.supabase.co"

# مفتاح الوصول العام (anon key) — يسمح بالوصول إلى الجداول حسب صلاحيات RLS
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp0d21pYnRuY3N1bW16dHBlc2NnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgwOTM1NDcsImV4cCI6MjA5MzY2OTU0N30.RswyGxVu5VaH9trphkhHNPRvkk0QITKZuJLDt38wUYM"
