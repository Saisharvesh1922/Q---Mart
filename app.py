from flask import Flask, jsonify, request
from blockchain import Blockchain  # Make sure the Blockchain class is correctly imported

app = Flask(__name__)

# Initialize the blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    """
    This endpoint mines a new block and adds it to the blockchain.
    """
    blockchain.add_block("New block data")
    return jsonify({"message": "Block mined!"})

@app.route('/chain', methods=['GET'])
def get_chain():
    """
    This endpoint returns the entire blockchain in JSON format.
    """
    chain = []
    for block in blockchain.chain:
        # Represent each block as a dictionary
        block_dict = {
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash
        }
        chain.append(block_dict)
    
    return jsonify({"chain": chain})

if __name__ == '__main__':
    app.run(debug=True)
