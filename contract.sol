pragma solidity ^0.8.0;
import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";


contract ProofOfID is OpenContract {
    
    mapping(bytes32 => address) private _account;
    mapping(address => bytes32) private _ID;

    constructor() {
        setOracle("any", this.createID.selector);  // developer mode, allows any oracle for 'createID'
    }

    function getID(address account) public view returns(bytes32) {
        require(_ID[account] != bytes32(0), "Account doesn't have an ID.");
        return _ID[account];
    }

    function getAccount(bytes32 ID) public view returns(address) {
        require(_account[ID] != address(0), "ID was never created.");
        return _account[ID];
    }

    function createID(bytes32 oracleID, address user, bytes32 ID) 
    public checkOracle(oracleID, this.createID.selector) {
        _ID[_account[ID]] = bytes32(0);
        _account[ID] = user;
        _ID[user] = ID;
    }
}
