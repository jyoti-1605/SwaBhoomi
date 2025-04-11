// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract LandRegistry is Ownable {
    event OwnerSet(address owner);

    constructor(address initialOwner) Ownable(initialOwner) {
        emit OwnerSet(initialOwner);
    }

    // Example function
    function hello() public pure returns (string memory) {
        return "Hello, Land!";
    }
}
