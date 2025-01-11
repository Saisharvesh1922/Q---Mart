from web3 import Web3
import json
import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    private_key = os.getenv('PRIVATE_KEY')
    infura_project_id = os.getenv('INFURA_PROJECT_ID')
    if not private_key or not infura_project_id:
        print("Missing environment variables. Please set PRIVATE_KEY and INFURA_PROJECT_ID in your .env file.")
        exit()
    return private_key, infura_project_id

def connect_to_polygon(infura_project_id):
    infura_url = f"https://polygon-mainnet.infura.io/v3/{infura_project_id}"
    provider = Web3.HTTPProvider(infura_url)
    web3 = Web3(provider)
    if web3.is_connected():
        print("Successfully connected to the Polygon mainnet!")
    else:
        print("Failed to connect to Polygon network. Check your Infura setup.")
        exit()
    return web3

def load_contract(web3):
    try:
        with open("build/contracts/MyContract.json") as f:
            compiled_contract = json.load(f)
        abi = compiled_contract['abi']
        bytecode = compiled_contract['bytecode'].strip()
        contract_address = "DEPLOYED_CONTRACT_ADDRESS"  # Replace with your deployed contract address
        contract = web3.eth.contract(address=contract_address, abi=abi)
    except FileNotFoundError:
        print("Contract file not found. Please ensure the path is correct.")
        exit()
    return contract

def call_mint_function(web3, contract, private_key, to_address, purchase_amount):
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    tx = contract.functions.mint(to_address, purchase_amount).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'chainId': 137
    })
    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Mint function called. Transaction hash: {tx_hash.hex()}")
    print(f"Transaction receipt: {tx_receipt}")

def main():
    private_key, infura_project_id = load_environment_variables()
    web3 = connect_to_polygon(infura_project_id)
    contract = load_contract(web3)

    # Replace with your recipient address and purchase amount
    to_address = '0xRecipientAddressHere'
    purchase_amount = 1000  # Example purchase amount

    call_mint_function(web3, contract, private_key, to_address, purchase_amount)

if __name__ == "__main__":
    main()
