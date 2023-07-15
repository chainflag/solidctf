// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.12;

contract Challenge {
    mapping(address => bool) public success;
    mapping(address => bool) public betted;
    mapping(address => uint) public win_counts;
    event SendFlag(address);
    bool public isSolved;

    constructor () {}

    function bet(bytes32 guess) public payable {
        require(! betted[msg.sender], "You have already tried this before.");
        bytes32 answer = keccak256(abi.encodePacked(blockhash(block.number), block.timestamp));
        require(answer == guess, "Bad luck.");
        win_counts[msg.sender] ++;
        (bool res,) = msg.sender.call{value: msg.value}("") ;
        require(res,"Message sender refuse to receive the reward.");
        betted[msg.sender] = true;
    }
    
    function checkwin() public payable {
        require(win_counts[msg.sender] >= 10, "Not enough wins .");
        success[msg.sender] = true;
        emit SendFlag(msg.sender);
        isSolved = true;
    }
}
