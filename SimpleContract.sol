// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleContract {
    uint public value;
    
    constructor() {
        value = 42;
    }
    
    function setValue(uint _value) public {
        value = _value;
    }
} 