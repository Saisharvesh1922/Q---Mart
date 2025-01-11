// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library MathLibrary {
    function add(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }

    function subtract(uint256 a, uint256 b) public pure returns (uint256) {
        require(b <= a, "Underflow error");
        return a - b;
    }
}
