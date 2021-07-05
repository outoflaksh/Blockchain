from flask import Flask, jsonify, request
from uuid import uuid4

from main import Blockchain

app = Flask(__name__)
NODE_ID = str(uuid4())
BLOCKCHAIN = Blockchain()

# 3 endpoints: to mine a new block, to add a new transaction, and to retrieve the full chain

@app.route("/mine", methods = ['GET'])
def mine():
    """
    For mining, we need to first calculate the proof of work for the new block,
    then use this proof of work to forge a new block
    reward the node with 1 Lcoin
    and add it to the chain
    """
    proof = BLOCKCHAIN.get_proof_of_work()
    BLOCKCHAIN.add_new_transaction(sender=0, recipient=NODE_ID, amount=0)
    new_block = BLOCKCHAIN.add_new_block(proof=proof)

    response = jsonify(new_block)

    return response, 200

@app.route("/transactions/new", methods = ["POST"])
def new_transaction():
    req = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not all(value in required for value in req):
        return jsonify({'message' : 'Missing values!'})

    BLOCKCHAIN.add_new_transaction(sender = req['sender'], recipient = req['recipient'], amount = req['amount'])

    return jsonify({'message' : 'Added transaction successfully!'}), 201

if __name__ == "__main__":
    app.run(debug=True)