pragma solidity ^0.8.0;
import "https://github.com/open-contracts/ethereum-protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract ProofOfID is OpenContract {
    
    mapping(bytes32 => address) private _account;
    mapping(address => bytes32) private _ID;

    constructor() {
        setOracleHash(this.createID.selector, 0x23884987967292cf67af3da3b2a1fd5c32d90990b0c99a0305a13443aa43c27d);
    }

    function getID(address account) public view returns(bytes32) {
        require(_ID[account] != bytes32(0), "Account doesn't have an ID.");
        return _ID[account];
    }

    function getAccount(bytes32 ID) public view returns(address) {
        require(_account[ID] != address(0), "ID was never created.");
        return _account[ID];
    }

    function createID(address user, bytes32 ID) public requiresOracle {
        _ID[_account[ID]] = bytes32(0);
        _account[ID] = user;
        _ID[user] = ID;
    }
}
