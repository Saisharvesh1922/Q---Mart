import hashlib
import time

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        This function creates the hash of the block based on its content.
        """
        block_string = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block in the chain (the genesis block).
        """
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        """
        Add a new block to the chain.
        """
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), transactions, previous_block.hash)
        self.chain.append(new_block)

    def display_chain(self):
        """
        Display the entire blockchain.
        """
        for block in self.chain:
            print(f"Block #{block.index} [Hash: {block.hash}]")
            print(f"Data: {block.transactions}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Previous Hash: {block.previous_hash}\n")

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Example difficulty (4 leading zeros)
