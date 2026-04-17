Here is the professionally updated **README.md** in English, tailored for your graduation project at the University of Kufa:

---

# 🛡️ Hybrid Blockchain-Based Document Verification System

## 📌 Description
This project is an advanced document management and authentication system that merges traditional **Backend** architectures with the power of **Blockchain** technology. The system ensures data integrity and prevents tampering by recording a unique digital fingerprint (CID/Hash) for every document on a decentralized network.

## ⚙️ Key Features
* **Secure File Upload:** Seamlessly upload and store files in the cloud using the **IPFS** protocol via the **Pinata** gateway.
* **Immutable Documentation:** Register file **CIDs** into a **Smart Contract** deployed on a **Ganache** blockchain network.
* **Integrity Verification:** A smart verification engine that compares local files against blockchain records to detect any unauthorized modifications.
* **Hybrid Storage Architecture:** Utilizes **SQLite** for high-performance dashboard rendering while relying on the Blockchain as the ultimate "Source of Truth".
* **Modern UI/UX:** A sleek, dark-themed user interface built with **Tkinter** for an intuitive user experience.

## 🛠️ Technologies & Prerequisites
To run this application, ensure the following software and libraries are installed:

### 1. Essential Software
* **Python 3.10+**: The core programming language.
* **Ganache**: To host a local blockchain network for development and testing.
* **Microsoft Edge**: Recommended browser for managing Pinata and GitHub configurations.
* **VS Code / PyCharm**: Recommended Integrated Development Environments (IDEs).

### 2. Python Dependencies
Install the required libraries using the following command:
`pip install web3 customtkinter requests pillow`

* **`web3`**: For interacting with Ethereum smart contracts on Ganache.
* **`customtkinter`**: For the enhanced graphical user interface.
* **`requests`**: To communicate with the **Pinata API** for IPFS uploads.
* **`pillow`**: For processing images and UI assets.
* **`sqlite3`**: Standard library for managing the local database.

## 📂 Project Structure
* **`login_ui.py`**: Handles user authentication and secure access.
* **`File_Manager_ui.py`**: The main dashboard for managing and viewing secured documents.
* **`file.py`**: The core logic engine connecting the UI, IPFS, and Blockchain.
* **`Blockchain_back.py`**: The blockchain layer responsible for smart contract interaction and transaction management.
* **`file_database.py`**: Manages local records to ensure the dashboard remains fast and responsive.

## 👨‍💻 Author
**Mohammed Sattar Saeed**
*Undergraduate Student, University of Kufa*
