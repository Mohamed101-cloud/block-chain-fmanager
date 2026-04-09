from web3 import Web3
import json

class BlockchainManager:
    def __init__(self):
        # 1. الاتصال بـ Ganache
        self.ganache_url = "http://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(self.ganache_url))
        
        # 2. عنوان العقد (تأكد من تحديثه بعد عمل Deploy للعقد الجديد)
        raw_address = "0xD6deBfE263819c7F423eB59c0a27a25d44814951"
        self.contract_address = self.web3.to_checksum_address(raw_address)
        
        # 3. الـ ABI المحدث (أضفنا دالة updateDocumentStatus)
        self.abi = [
            
	
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "fileHash",
				"type": "bytes32"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "uploader",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "DocumentRecorded",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "fileHash",
				"type": "bytes32"
			},
			{
				"indexed": False,
				"internalType": "enum DocumentRegistry.Status",
				"name": "status",
				"type": "uint8"
			}
		],
		"name": "DocumentStatusChanged",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_hash",
				"type": "bytes32"
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
				"internalType": "bytes32",
				"name": "_hash",
				"type": "bytes32"
			},
			{
				"internalType": "enum DocumentRegistry.Status",
				"name": "_status",
				"type": "uint8"
			}
		],
		"name": "setDocumentStatus",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "docs",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "fileHash",
				"type": "bytes32"
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
			},
			{
				"internalType": "enum DocumentRegistry.Status",
				"name": "status",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_hash",
				"type": "bytes32"
			}
		],
		"name": "verifyDocument",
		"outputs": [
			{
				"internalType": "address",
				"name": "uploader",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "enum DocumentRegistry.Status",
				"name": "status",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]


        
        
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        
        if self.web3.is_connected():
            self.web3.eth.default_account = self.web3.eth.accounts[0]
        else:
            print("تحذير: لم يتم الاتصال بـ Ganache!")

    def record_file_hash(self, file_hash_hex):
        try:
            if not file_hash_hex.startswith('0x'):
                file_hash_hex = '0x' + file_hash_hex
            hash_bytes = self.web3.to_bytes(hexstr=file_hash_hex)
            tx_hash = self.contract.functions.recordDocument(hash_bytes).transact()
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True, receipt.transactionHash.hex()
        except Exception as e:
            return False, str(e)

    def verify_file(self, file_hash_hex):
        try:
            if not file_hash_hex.startswith('0x'):
                file_hash_hex = '0x' + file_hash_hex
            hash_bytes = self.web3.to_bytes(hexstr=file_hash_hex)
            result = self.contract.functions.verifyDocument(hash_bytes).call()
            
            # تحويل الحالة من رقم إلى نص مفهوم
            status_map = {0: "Active", 1: "Revoked", 2: "Archived"}
            return {
                "uploader": result[0],
                "timestamp": result[1],
                "status": status_map.get(result[2], "Unknown")
            }
        except Exception as e:
            print(f"Error verifying: {e}")
            return None

    def update_file_status(self, file_hash_hex, new_status):
        """
        تغيير حالة الملف: 0 = Active, 1 = Revoked, 2 = Archived
        """
        try:
            if not file_hash_hex.startswith('0x'):
                file_hash_hex = '0x' + file_hash_hex
            hash_bytes = self.web3.to_bytes(hexstr=file_hash_hex)

            # استدعاء الدالة من العقد
            tx_hash = self.contract.functions.setDocumentStatus(hash_bytes, int(new_status)).transact(...)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True, receipt.transactionHash.hex()
        except Exception as e:
            print(f"Error updating status: {e}")
            return False, str(e)


