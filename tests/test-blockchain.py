import unittest
from blockchain import Blockchain
import json
from flask import Flask
from scripts.mine import app

class TestBlockchain(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh blockchain before each test"""
        self.blockchain = Blockchain()
        self.app = app.test_client()  # Flask test client
        self.app.testing = True

    def test_initial_blockchain(self):
        """Test that the blockchain is initialized correctly"""
        self.assertEqual(len(self.blockchain.chain), 1)  # Should have the genesis block
        self.assertEqual(self.blockchain.chain[0].data, "Genesis Block")
        self.assertEqual(self.blockchain.chain[0].index, 0)

    def test_add_block(self):
        """Test that new blocks are added correctly"""
        self.blockchain.add_block("Block 1 data")
        self.assertEqual(len(self.blockchain.chain), 2)  # Should have two blocks now
        self.assertEqual(self.blockchain.chain[1].data, "Block 1 data")
        self.assertEqual(self.blockchain.chain[1].index, 1)

    def test_mine_route(self):
        """Test the /mine route in the Flask app"""
        response = self.app.get('/mine')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Block mined!', response.data)

    def test_chain_route(self):
        """Test the /chain route in the Flask app"""
        response = self.app.get('/chain')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue("chain" in data)
        self.assertEqual(len(data['chain']), 1)  # Only genesis block initially

if __name__ == "__main__":
    unittest.main()
