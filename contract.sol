pragma solidity ^0.8.0;

import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract ProofOfIdentity is OpenContractAlpha {
    
    mapping(bytes32 => address) private _account;
    mapping(address => bytes32) private _ID;

    function getID(address account) public view returns(bytes32) {
        require(_ID[account] != bytes32(0), "Account never created an ID.");
        require(_account[_ID[account]] == account, "Account does not have an ID anymore.");
        return _ID[account];
    }

    function getAccount(bytes32 ID) public view returns(address) {
        require(_account[ID] != address(0), "ID was never created.");
        return _account[ID];
    }

    function createID(bytes32 oracleHash, address msgSender, bytes32 ID) 
    public _oracle(oracleHash, msgSender, this.createIdentity.selector) {
        _account[ID] = msgSender;
        _ID[msgSender] = ID;
    }
}
