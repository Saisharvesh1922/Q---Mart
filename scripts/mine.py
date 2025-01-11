from flask import Flask, jsonify
from blockchain import Blockchain

app = Flask(__name__)

# Initialize Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.add_block("New block data")
    return jsonify({"message": "Block mined!"})

@app.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    return jsonify({"chain": chain})

if __name__ == '__main__':
    app.run(debug=True)
