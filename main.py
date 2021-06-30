from hashlib import sha256
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
        return {'index': self.index, 'timestamp' : self.timestamp, 'transcations' : self.transactions, 'previous hash' : self.prev_hash, 'proof of work' : self.proof, 'hash' : self.hash}



class Blockchain():
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def add_new_block(self, proof, prev_hash = None):
        block = Block(
                index = len(self.chain),
                timestamp = time.time(),
                transactions = self.current_transactions,
                prev_hash = prev_hash or self.chain[-1].hash,
                proof = proof
            )

        self.chain.append(block)
        self.current_transactions = []

        print(f"Added new block on index #{len(self.chain)}")
        return block.info

    def add_new_transaction(self, sender, recipient, amount):
        transaction = {'sender' : sender, 'recipient' : recipient, 'amount' : amount}

        self.current_transactions.append(transaction)

        print("Transaction added")
        return len(self.chain)

    @property
    def get_last_block(self):
        return self.chain[-1]

# genesis = Block(index = 0, timestamp = time.time(), transactions = "NA", prev_hash = "0", proof = 1)

# print(genesis.info)