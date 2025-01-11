from brownie import accounts, LoyaltyToken
import pytest

# Setup the contract before running tests
@pytest.fixture
def token():
    # Deploy the contract
    return LoyaltyToken.deploy({"from": accounts[0]})

def test_initial_supply(token):
    # Check the initial balance of the owner (should be 0 if minting isn't done yet)
    assert token.balanceOf(accounts[0]) == 0

def test_minting(token):
    # Mint tokens and check the balance
    token.mint(accounts[1], 1000, {"from": accounts[0]})
    assert token.balanceOf(accounts[1]) == 20  # 2% of 1000

def test_burning(token):
    # Mint tokens, burn some, and check balance
    token.mint(accounts[1], 1000, {"from": accounts[0]})
    token.burn(accounts[1], 10, {"from": accounts[0]})
    assert token.balanceOf(accounts[1]) == 10  # 20 - 10

def test_only_owner_can_mint(token):
    # Ensure only the owner can mint
    with pytest.raises(Exception):  # Expecting an error if someone else tries to mint
        token.mint(accounts[1], 1000, {"from": accounts[1]})

def test_only_owner_can_burn(token):
    # Ensure only the owner can burn
    token.mint(accounts[1], 1000, {"from": accounts[0]})
    with pytest.raises(Exception):  # Expecting an error if someone else tries to burn
        token.burn(accounts[1], 10, {"from": accounts[1]})
