import sqlite3
import os
import shutil
import time

class DatabaseManager:
    def __init__(self, db_name="local_vault.db"):
        self.db_name = db_name

        # مجلد تخزين نسخة محلية من الملفات داخل المشروع لضمان بقائها حتى لو حذف الأصل
        self.storage_dir = "files_storage"
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

        self.init_db()

    def init_db(self):
        """إنشاء الجدول مع استخدام CID كمعرف فريد متوافق مع IPFS والبلوكشين"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # تم تغيير hash إلى cid ليتوافق مع مخرجات Pinata والعقد الذكي المحدث
            cursor.execute('''CREATE TABLE IF NOT EXISTS secure_files (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                path TEXT,
                                cid TEXT,
                                date TEXT
                            )''')
            conn.commit()

    def add_file(self, name, path, cid, date):
        """إضافة سجل ملف جديد وحفظ نسخة منه في المجلد المحلي"""
        try:
            # 1. إنشاء اسم فريد للملف محلياً باستخدام الوقت لتجنب تكرار الأسماء
            filename = os.path.basename(path)
            new_filename = f"{int(time.time())}_{filename}"
            new_path = os.path.join(self.storage_dir, new_filename)

            # 2. نسخ الملف إلى مجلد التخزين المحلي (Storage) لضمان استمرارية النظام الهجين
            shutil.copy(path, new_path)

            # 3. حفظ البيانات (الاسم، المسار الجديد، الـ CID، والتاريخ)
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO secure_files (name, path, cid, date) VALUES (?, ?, ?, ?)",
                    (name, new_path, cid, date)
                )
                conn.commit()

            return True

        except Exception as e:
            print(f"Error in local database operation: {e}")
            return False

    def get_all_files(self):
        """جلب القائمة الكاملة لعرضها في واجهة المستخدم (Dashboard) مرتبة من الأحدث"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # نرجع البيانات لعرضها مباشرة لصديقك المسؤول عن الفرونت اند
            cursor.execute("SELECT name, path, date, cid FROM secure_files ORDER BY id DESC")
            return cursor.fetchall()