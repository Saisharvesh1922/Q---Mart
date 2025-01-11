from brownie import accounts, LoyaltyToken, network

def deploy():
    # Get the account to deploy the contract
    account = accounts[0]

    # Deploy the contract
    print("Deploying LoyaltyToken contract...")
    try:
        loyalty_token = LoyaltyToken.deploy({'from': account})
        # Print the contract address after deployment
        print(f"LoyaltyToken deployed at: {loyalty_token.address}")
    except Exception as e:
        print(f"Failed to deploy LoyaltyToken: {e}")

def main():
    # Ensure the correct network is selected (e.g., Goerli testnet)
    if network.show_active() == "goerli":
        deploy()
    else:
        print("This migration is intended to be used with the Goerli testnet.")
