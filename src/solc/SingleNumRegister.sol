pragma solidity ^0.8.9;

contract StoreVar {

    uint8 public _myVar;

    function setVar(uint8 _var) public {
        _myVar = _var;
    }

    function getVar() public view returns (uint8) {
        return _myVar;
    }

}

HexBytes('0xc251e8882c2ba1dd2f15697b2262ecafa2d9f343072facd5e454cf7aba06cb24')