from flask import Flask, jsonify, request
from uuid import uuid4

from main import Blockchain

app = Flask(__name__)
NODE_ID = str(uuid4())
BLOCKCHAIN = Blockchain()

BLOCKCHAIN.create_genesis_block()
# 3 endpoints: to mine a new block, to add a new transaction, and to retrieve the full chain

@app.route("/mine", methods = ['GET'])
def mine():
    """Proof of work calculated, node rewarded, and new block added to the chain.
    """
    proof = BLOCKCHAIN.get_proof_of_work()
    BLOCKCHAIN.add_new_transaction(sender=0, recipient=NODE_ID, amount=1)
    new_block = BLOCKCHAIN.add_new_block(proof=proof)

    response = {'message' : 'New block mined successfully!', 
                'index' : new_block['index'],
                'transactions' : new_block['transactions'],
                'proof of work' : new_block['proof of work'],
                'previous hash' : new_block['previous hash']}

    return jsonify(response), 200

@app.route("/transactions/new", methods = ["POST"])
def new_transaction():
    """ Transaction request retrieved, validated, and added to the chain
    """
    req = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not all(value in required for value in req):
        return jsonify({'message' : 'Missing values!'})

    BLOCKCHAIN.add_new_transaction(sender = req['sender'], recipient = req['recipient'], amount = req['amount'])

    return jsonify({'message' : 'Added transaction successfully!'}), 201

@app.route("/chain", methods = ['GET'])
def chain():
    """Current chain is returned as json response"""
    return jsonify(BLOCKCHAIN.chain), 200


if __name__ == "__main__":
    app.run(debug=True)