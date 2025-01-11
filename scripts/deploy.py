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

def load_contract():
    try:
        with open("build/contracts/MyContract.json") as f:
            compiled_contract = json.load(f)
        abi = compiled_contract['abi']
        bytecode = compiled_contract['bytecode'].strip()
        if not bytecode.startswith('0x'):
            bytecode = '0x' + bytecode  # Ensure bytecode is properly formatted
    except FileNotFoundError:
        print("Contract file not found. Please ensure the path is correct.")
        exit()
    return abi, bytecode

def deploy_contract(web3, abi, bytecode, private_key):
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    balance = web3.eth.get_balance(account.address)
    min_balance = Web3.to_wei(0.1, 'ether')  # Minimum required balance in MATIC
    print(f"Account balance: {web3.from_wei(balance, 'ether')} MATIC")

    if balance < min_balance:
        print(f"Insufficient funds in the account. Minimum required balance is {web3.from_wei(min_balance, 'ether')} MATIC. Please add more MATIC for gas fees.")
        exit()

    gas_estimate = web3.eth.estimate_gas({
        'to': None,
        'data': bytecode
    })
    gas_price = web3.eth.gas_price
    tx_cost = gas_price * gas_estimate
    if balance < tx_cost + min_balance:
        print(f"Insufficient funds for gas. Transaction cost: {web3.from_wei(tx_cost, 'ether')} MATIC. Account balance: {web3.from_wei(balance, 'ether')} MATIC.")
        exit()

    LoyaltyToken = web3.eth.contract(abi=abi, bytecode=bytecode)
    transaction = LoyaltyToken.constructor().build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': gas_estimate,
        'gasPrice': gas_price,
        'chainId': 137  # Polygon's chain ID
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Contract deployed at: {tx_receipt.contractAddress}")

def send_matic(web3, private_key, to_address, amount_ether):
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    value = web3.to_wei(amount_ether, 'ether')
    
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': value,
        'gas': 2000000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'chainId': 137
    }

    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction hash: {tx_hash.hex()}")

def main():
    private_key, infura_project_id = load_environment_variables()
    web3 = connect_to_polygon(infura_project_id)
    abi, bytecode = load_contract()
    deploy_contract(web3, abi, bytecode, private_key)

    # Replace with your recipient address
    recipient_address = '0x0Bbd707447Ddbb1184F64755D1704F535b1F97b4'
    amount_matic = 10  # Amount in MATIC

    send_matic(web3, private_key, recipient_address, amount_matic)

if __name__ == "__main__":
    main()
