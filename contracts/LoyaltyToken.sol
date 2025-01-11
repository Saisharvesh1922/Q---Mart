// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

//import "OpenZeppelin/openzeppelin-contracts@4.9.2/contracts/token/ERC20/ERC20.sol";
import "C:/Users/Hp/Desktop/dApp/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
contract LoyaltyToken is ERC20 {
    address public owner;

    constructor() ERC20("QTOKEN", "QT") {
        owner = msg.sender;
    }

    // Mint function modified to accept purchaseAmount and mint 2% of it
    function mint(address to, uint256 purchaseAmount) public {
        require(msg.sender == owner, "Only owner can mint tokens");
        
        // Calculate the amount to mint (2% of the purchaseAmount)
        uint256 mintAmount = purchaseAmount * 2 / 100;
        
        _mint(to, mintAmount);
    }

    function burn(address from, uint256 amount) public {
        require(msg.sender == owner, "Only owner can burn tokens");
        _burn(from, amount);
    }
}
event Mint(address indexed to, uint256 amount);
event Burn(address indexed from, uint256 amount);
