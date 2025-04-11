// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleLandRegistry is ERC721 {
    uint public landId;
    address public owner;

    constructor() 
        ERC721("LandToken", "LAND") 
    {
        owner = msg.sender;
        landId = 0;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    function registerLand(string memory location) 
        public 
    {
        require(bytes(location).length > 0, "Location cannot be empty");
        
        landId++;
        _safeMint(msg.sender, landId);
    }
} 