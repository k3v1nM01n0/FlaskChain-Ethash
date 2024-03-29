from hashlib import sha256
import json
import time
import pyethash
import json


from flask import Flask, request
import requests

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
        

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    difficulty = 2
    def proof_of_work(self, block):
        block.nonce = 0
        while True:
            mix_digest = pyethash.get_mix_digest(block.nonce, block.timestamp)
            if int.from_bytes(mix_digest, byteorder='big') < DIFFICULTY:
                return block.nonce
            block.nonce += 1


    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.last_block

        new_block = Block(index=last_block.index +1,
                        transactions = self.unconfirmed_transactions,
                        timestamp=time.time(),
                        previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
        
app = Flask(__name__)
blockchain = Blockchain()


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = {}
    count = 1

    for block in blockchain.chain:
        chain_data['chain: {}'.format(count)] = block.__dict__
        count += 1
    return chain_data


@app.route('/mine', methods=['GET'])
def get_mine():
    if not blockchain.unconfirmed_transactions:
        return 'No transactions to mine', 400
    blockchain.mine()
    block_data = blockchain.chain[-1].__dict__
    return json.dumps(block_data)


@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    if index < 0:
        return 'Invalid block index', 400
    if index >= len(blockchain.chain):
        return 'Block not found', 404
    block = blockchain.chain[index]
    return json.dumps(block.__dict__)


@app.route('/transaction/<int:index>', methods=['GET'])
def get_transaction(index):
    if index < 0:
        return 'Invalid transaction index', 400
    for block in blockchain.chain:
        if len(block.transactions) > index:
            return json.dumps(block.transactions[index])
    return 'Transaction not found', 404


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if not request.is_json:
        return 'Invalid request, expected JSON', 400
    transaction = request.get_json()
    if not transaction:
        return 'Invalid transaction', 400
    blockchain.add_new_transaction(transaction)
    return 'Transaction added', 201


@app.route('/block/<int:index>', methods=['DELETE'])
def delete_block(index):
    if index < 1:
        return 'Cannot delete genesis block', 400
    if index >= len(blockchain.chain):
        return 'Block not found', 404
    blockchain.chain.pop(index)
    return 'Block deleted', 200



app.run(debug=True, port=5000)

