// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BasicLandRegistry {
    uint public landId;
    address public owner;
    
    mapping(uint => string) public landLocations;
    mapping(uint => address) public landOwners;
    
    event LandRegistered(uint indexed id, address indexed owner, string location);
    
    constructor() {
        owner = msg.sender;
        landId = 0;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }
    
    function registerLand(string memory location) public {
        require(bytes(location).length > 0, "Location cannot be empty");
        
        landId++;
        landLocations[landId] = location;
        landOwners[landId] = msg.sender;
        
        emit LandRegistered(landId, msg.sender, location);
    }
    
    function transferLand(uint _landId, address to) public {
        require(landOwners[_landId] == msg.sender, "Not the owner of this land");
        require(to != address(0), "Invalid recipient");
        
        landOwners[_landId] = to;
    }
}
