from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
private_key = os.getenv('PRIVATE_KEY')
infura_project_id = os.getenv('INFURA_PROJECT_ID')

# Connect to Mumbai testnet using Infura
infura_url = f"https://polygon-mumbai.infura.io/v3/{infura_project_id}"
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    print("Successfully connected to the Polygon Mumbai testnet!")
else:
    print("Failed to connect to Polygon Mumbai testnet. Check your Infura setup.")
    exit()

account = web3.eth.account.from_key(private_key)
balance = web3.eth.get_balance(account.address)
print(f"Account balance: {web3.from_wei(balance, 'ether')} MATIC")
