import sqlite3

class DatabaseManager:
    def __init__(self, db_name="company.db"):
        self.db_name = db_name
        self.setup_db()

    def setup_db(self):
        """إنشاء الجداول والمستخدم المسؤول الأول"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        # إضافة الـ Admin إذا لم يكن موجوداً
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           ("mohamed404", "admin404", "admin"))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()

    def check_login(self, username, password):
        """التحقق من بيانات الدخول وإعادة الرتبة (admin/employee)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def add_employee(self, username, password):
        """إضافة موظف جديد بواسطة الادمن"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, password, "employee"))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False