from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
private_key = os.getenv('PRIVATE_KEY')

web3 = Web3()
account = web3.eth.account.from_key(private_key)
print(account.address)
