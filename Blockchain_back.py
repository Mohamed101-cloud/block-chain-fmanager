from web3 import Web3
import json

class BlockchainManager:
    def __init__(self):
        # 1. الاتصال بـ Ganache
        self.ganache_url = "http://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(self.ganache_url))
        
        # 2. عنوان العقد (تأكد من تحديثه بعد عمل Deploy للعقد في Remix)
        raw_address = "0x09Fb3881A869C605bB51dbc1C2bFef531C212d2E"
        self.contract_address = self.web3.to_checksum_address(raw_address)
        
        self.abi = [
            
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "cid",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "uploader",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "time",
				"type": "uint256"
			}
		],
		"name": "DocumentRecorded",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_cid",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			}
		],
		"name": "recordDocument",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "allCIDs",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "docs",
		"outputs": [
			{
				"internalType": "string",
				"name": "ipfsCID",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "fileName",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "uploader",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_cid",
				"type": "string"
			}
		],
		"name": "exists",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getCID",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_cid",
				"type": "string"
			}
		],
		"name": "getDocument",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTotalDocuments",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_cid",
				"type": "string"
			}
		],
		"name": "verifyDocument",
		"outputs": [
			{
				"internalType": "bool",
				"name": "isAuthentic",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "fileName",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "uploader",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
        
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        
        if self.web3.is_connected():
            # استخدام الحساب الأول من Ganache كحساب افتراضي لإرسال المعاملات
            self.web3.eth.default_account = self.web3.eth.accounts[0]
            print(f"Connection successful. Active Account: {self.web3.eth.default_account}")
        else:
            print("Warning: Connection to Ganache failed!")

    def record_file_on_blockchain(self, cid, file_name):
        """تسجيل ملف جديد باستخدام الـ CID والاسم"""
        try:
            # إرسال المعاملة للدالة recordDocument(string, string)
            tx_hash = self.contract.functions.recordDocument(cid, file_name).transact()
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True, receipt.transactionHash.hex()
        except Exception as e:
            return False, str(e)

    def verify_file(self, cid):
        """التحقق من صحة الملف باستخدام الـ CID"""
        try:
            # استدعاء دالة verifyDocument(string) من العقد
            result = self.contract.functions.verifyDocument(cid).call()
            
            # العقد يرجع: (bool, string, address, uint256)
            is_authentic = result[0]
            file_name = result[1]
            uploader = result[2]
            timestamp = result[3]
            
            if is_authentic:
                return {
                    "status": "success",
                    "is_authentic": True,
                    "file_name": file_name,
                    "uploader": uploader,
                    "timestamp": timestamp
                }
            else:
                return {
                    "status": "not_found",
                    "is_authentic": False,
                    "message": "هذا الملف غير مسجل في البلوكشين."
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

# --- مثال على الاستخدام المباشر ---
if __name__ == "__main__":
    manager = BlockchainManager()
    
    # تجربة التسجيل
    # status, tx = manager.record_file_on_blockchain("Qm123test", "MyReport.pdf")
    # print(f"Transaction: {tx}")
    
    # تجربة التحقق
    # result = manager.verify_file("Qm123test")
    # print(result)