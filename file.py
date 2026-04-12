import hashlib
import os
from datetime import datetime
from file_database import DatabaseManager
from Blockchain_back import BlockchainManager 

class FileProcessor:
    def __init__(self):
        self.db = DatabaseManager()
        self.blockchain = BlockchainManager()

    def calculate_sha256(self, file_path):
        
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error hashing file: {e}")
            return None

    def process_upload(self, file_path):
        
        # توليد البصمة الرقمية للملف
        f_hash = self.calculate_sha256(file_path)
        if not f_hash:
            return False, 

        success, result = self.blockchain.record_file_hash(f_hash)
        
        if success:
            try:
            
                filename = os.path.basename(file_path)
                current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.db.add_file(filename, file_path, f_hash, current_date)
                
                return True, f"تم بنجاح! رقم المعاملة: {result}"
            except Exception as e:
                return False, f"نجح البلوكتشين ولكن فشل الحفظ المحلي: {str(e)}"
        else:
            
            return False, f"فشل التسجيل في البلوكتشين: {result}"

    def get_local_records(self):
        return self.db.get_all_files()