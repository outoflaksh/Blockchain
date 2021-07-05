from hashlib import sha256
from urllib.parse import urlparse
import requests
import time

class Block():
    def __init__(self, index, timestamp, transactions, prev_hash, proof):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.proof = proof
        self.hash = self.hash_block()

    def hash_block(self):
        to_hash = (str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.prev_hash)).encode()
        return sha256(to_hash).hexdigest()
        
    @property
    def info(self):
        return {'index': self.index, 'timestamp' : self.timestamp, 'transactions' : self.transactions, 'previous hash' : self.prev_hash, 'proof of work' : self.proof, 'hash' : self.hash}



class Blockchain():
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()


    def add_new_block(self, proof, prev_hash = None):
        block = Block(
                index = len(self.chain),
                timestamp = time.time(),
                transactions = self.current_transactions,
                prev_hash = prev_hash or self.chain[-1]['hash'],
                proof = proof
            )

        self.chain.append(block.info)
        self.current_transactions = []

        print(f"Added new block on index #{len(self.chain)}")

        return block.info

    def add_new_transaction(self, sender, recipient, amount):
        transaction = {'sender' : sender, 'recipient' : recipient, 'amount' : amount}

        self.current_transactions.append(transaction)

        print(f"New transaction added, current transactions: {len(self.current_transactions)}")
        return len(self.chain)

    def get_proof_of_work(self, prev_proof = None):
        prev_proof = prev_proof or self.last_block['proof of work']
        proof = 0

        while not(self.validate_proof(prev_proof, proof)):
            proof += 1

        return proof 

    def validate_proof(self, prev_proof, proof):
        return sha256(f'{prev_proof}{proof}'.encode()).hexdigest()[:4] == '0000'

    def create_genesis_block(self):
        genesis_block = self.add_new_block(0, "#")
        return genesis_block

    def validate_chain(self, chain):
        for i in range(1, len(chain)):
            prev_hash = chain[i-1]['hash']
            prev_proof = chain[i-1]['proof of work']

            if chain[i]['previous hash'] != prev_hash:
                return False 
            
            if not self.validate_proof(prev_proof, chain[i]['proof of work']):
                return False 

        return True


    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def get_chain(self):
        return {'chain' : self.chain, 'length' : len(self.chain)}

    def register_new_node(self, node_url):
        parsed_url = urlparse(node_url).netloc
        self.nodes.add(parsed_url)
        return 

    def resolve_conflict(self):
        new_chain = None 
        max_length = len(self.chain)

        for node in self.nodes():
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                current_length = response.json()['length']
                current_chain = response.json()['chain']

                if current_length > max_length and self.validate_chain(current_chain):
                    max_length = current_length
                    new_chain = current_chain

        if new_chain:
            self.chain = new_chain
            return True 
        
        return False