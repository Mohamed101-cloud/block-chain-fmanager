from web3 import Web3
import json

class BlockchainManager:
    def __init__(self):
        # 1. الاتصال بـ Ganache
        self.ganache_url = "http://127.0.0.1:8545"
        self.web3 = Web3(Web3.HTTPProvider(self.ganache_url))
        
        # 2. معلومات العقد (تأكد من مطابقة العنوان)
        self.contract_address = ""
        
        # تم تصحيح الـ ABI ليكون مصفوفة مباشرة
        self.abi = [
        ]
        
        # إنشاء كائن العقد
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        
        # تعيين الحساب الأول كمرسل افتراضي
        if self.web3.is_connected():
            self.web3.eth.default_account = self.web3.eth.accounts[0]

    def record_file_hash(self, file_hash_hex):
        """تسجيل الهاش في البلوكتشين"""
        try:
            # إضافة 0x إذا لم تكن موجودة
            if not file_hash_hex.startswith('0x'):
                file_hash_hex = '0x' + file_hash_hex
                
            hash_bytes = self.web3.to_bytes(hexstr=file_hash_hex)
            tx_hash = self.contract.functions.recordDocument(hash_bytes).transact()
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True, receipt.transactionHash.hex()
        except Exception as e:
            return False, str(e)

    def verify_file(self, file_hash_hex):
        """التحقق من بيانات الملف"""
        try:
            if not file_hash_hex.startswith('0x'):
                file_hash_hex = '0x' + file_hash_hex
            hash_bytes = self.web3.to_bytes(hexstr=file_hash_hex)
            return self.contract.functions.verifyDocument(hash_bytes).call()
        except Exception as e:
            return None