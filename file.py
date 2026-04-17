import os
import requests
from datetime import datetime
from file_database import DatabaseManager 
from Blockchain_back import BlockchainManager 

class FileProcessor:
    def __init__(self):
        self.db = DatabaseManager()
        self.blockchain = BlockchainManager()
        
        # معلومات Pinata الخاصة بك
        self.pinata_api_key = "03bd6ef508c78c49739c"
        self.pinata_secret_api_key = "3325b02d1d0f927af0fe99c53b353e00075738bba25a79cd54c3cf289d787ee0"
        self.pinata_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    def upload_to_pinata(self, file_path):
        """رفع الملف لـ Pinata والحصول على CID (Qm...)"""
        headers = {
            'pinata_api_key': self.pinata_api_key,
            'pinata_secret_api_key': self.pinata_secret_api_key
        }
        try:
            with open(file_path, 'rb') as file:
                filename = os.path.basename(file_path)
                response = requests.post(
                    self.pinata_url,
                    files={'file': (filename, file)},
                    headers=headers
                )
                if response.status_code == 200:
                    return response.json()['IpfsHash'] # الـ CID
                return None
        except Exception:
            return None

    def process_upload(self, file_path):
        """الرفع والتوثيق"""
        cid = self.upload_to_pinata(file_path)
        if not cid:
            return False, "فشل الرفع لـ Pinata"

        filename = os.path.basename(file_path)
        
        # التسجيل في البلوكشين (تأكد من مطابقة اسم الدالة في Blockchain_back)
        success, result = self.blockchain.record_file_on_blockchain(cid, filename)
        
        if success:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.db.add_file(filename, file_path, cid, current_date)
            return True, f"Verification Successful! CID: {cid}"        
        return False, f"Blockchain Error: {result}"

    def process_verification(self, file_path):
        """التحقق من صحة الملف"""
        cid = self.upload_to_pinata(file_path)
        if not cid:
            return {"status": "error", "message": "Connection to Pinata failed"}
        # التحقق من العقد الذكي
        return self.blockchain.verify_file(cid)