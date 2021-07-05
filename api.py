from flask import Flask, json, jsonify, request
from uuid import uuid4

from main import Blockchain

app = Flask(__name__)
NODE_ID = str(uuid4())
BLOCKCHAIN = Blockchain()

BLOCKCHAIN.create_genesis_block()
# 5 endpoints: to mine a new block, to add a new transaction, to retrieve the full chain, to register new node and to resolve conflict

# ENDPOINTS FOR BLOCKS
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
    return jsonify(BLOCKCHAIN.get_chain), 200

# ENDPOINTS FOR NODES
@app.route("/nodes/register", methods = ['POST'])
def register_node():
    req = request.get_json()

    if 'url' not in req.keys():
        return jsonify({'message' : 'Node URL missing from request!'}), 400
    url = req['url']
    BLOCKCHAIN.register_new_node(url)

    return jsonify({'message' : 'Node URL added successfully!'}), 201

@app.route("/nodes/resolve", methods = ['GET'])
def resolve_conflicts():
    if BLOCKCHAIN.resolve_conflict():
        return jsonify({'message' : 'One chain changed!'})
    return jsonify({'message' : 'No chain changed, current chain authoratative!'})
    

if __name__ == "__main__":
    app.run(debug=True)