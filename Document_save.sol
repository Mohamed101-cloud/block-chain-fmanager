// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DocumentRegistry {
    
    enum Status { Active, Revoked, Archived }

    struct Document {
        bytes32 fileHash;
        address uploader;
        uint256 timestamp;
        Status status;
    }

    address public owner;
    mapping(bytes32 => Document) public docs;

    event DocumentRecorded(bytes32 indexed fileHash, address indexed uploader, uint256 timestamp);
    event DocumentStatusChanged(bytes32 indexed fileHash, Status status);

    modifier onlyOwner() {
        require(msg.sender == owner, "Manager only");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    //الوظائف الأساسية 

    // 
    function recordDocument(bytes32 _hash) public {
        require(docs[_hash].timestamp == 0, "Document already exists");

        docs[_hash] = Document({
            fileHash: _hash,
            uploader: msg.sender,
            timestamp: block.timestamp,
            status: Status.Active
        });

        emit DocumentRecorded(_hash, msg.sender, block.timestamp);
    }

    function verifyDocument(bytes32 _hash)
        public
        view
        returns (address uploader, uint256 timestamp, Status status)
    {
        require(docs[_hash].timestamp != 0, "Document does not exist");
        Document memory doc = docs[_hash];
        return (doc.uploader, doc.timestamp, doc.status);
    }

    function setDocumentStatus(bytes32 _hash, Status _status) public onlyOwner {
        require(docs[_hash].timestamp != 0, "Document not found");
        docs[_hash].status = _status;
        emit DocumentStatusChanged(_hash, _status);
    }
}