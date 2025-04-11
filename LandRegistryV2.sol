// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LandRegistryV2 is ERC721, Ownable {
    uint public landId;

    constructor() 
        ERC721("LandToken", "LAND") 
        Ownable(msg.sender) 
    {
        landId = 0;
    }

    function registerLand(string memory location) 
        public 
    {
        require(bytes(location).length > 0, "Location cannot be empty");
        
        landId++;
        _safeMint(msg.sender, landId);
    }
} 