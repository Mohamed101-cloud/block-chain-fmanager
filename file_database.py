import sqlite3
import os
import shutil
import time

class DatabaseManager:
    def __init__(self, db_name="local_vault.db"):
        self.db_name = db_name

        # مجلد تخزين الملفات داخل المشروع
        self.storage_dir = "files_storage"
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS secure_files (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                path TEXT,
                                hash TEXT,
                                date TEXT
                            )''')
            conn.commit()

    def add_file(self, name, path, f_hash, date):
        try:
            filename = os.path.basename(path)
            new_filename = f"{int(time.time())}_{filename}"

            new_path = os.path.join(self.storage_dir, new_filename)

            shutil.copy(path, new_path)

            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO secure_files (name, path, hash, date) VALUES (?, ?, ?, ?)",
                    (name, new_path, f_hash, date)
                )
                conn.commit()

            return True

        except Exception as e:
            print(f"Error copying file: {e}")
            return False

    def get_all_files(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, path, date, hash FROM secure_files ORDER BY id DESC")
            return cursor.fetchall()