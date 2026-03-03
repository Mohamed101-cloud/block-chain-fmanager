import hashlib
import os
from Blockchain_back import BlockchainManager

class FileProcessor:
    def __init__(self):
        self.blockchain = BlockchainManager()

    def calculate_sha256(self, file_path):
        """توليد بصمة رقمية فريدة للملف"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error calculating hash: {e}")
            return None

    def upload_to_blockchain(self, file_path):
        """العملية الكاملة: حساب الهاش ثم الرفع"""
        # 1. حساب الهاش
        f_hash = self.calculate_sha256(file_path)
        if not f_hash:
            return False, "تعذر معالجة الملف"

        # 2. محاولة التسجيل في البلوكتشين
        success, result = self.blockchain.record_file_hash(f_hash)
        
        if success:
            return True, result  # نتيجة النجاح هي رقم المعاملة
        else:
            return False, result # نتيجة الفشل هي رسالة الخطأ

    def check_authenticity(self, file_path):
        """التحقق من صحة الملف المختار"""
        f_hash = self.calculate_sha256(file_path)
        data = self.blockchain.verify_file(f_hash)
        if data and data[1] != 0: # إذا كان الـ timestamp ليس صفراً
            return True, data
        return False, "هذا الملف غير مسجل في النظام!"