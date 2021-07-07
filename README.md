# L-Coin: Blockchain from scratch💰
To better understand the blockchain technology and how cryptocurrency works, I decided to implement my own basic blockchain from scratch in Python. 

A blockchain can be defined as an immutable, appendable, distributed, open digital ledger that can be used to store a database of all transactions that take place.

To implement all that in python, I wrote a block class and a blockchain class. The block class consisted of properties that make up a block: index, timestamp, data, for chaining, the previous block's hash, and a proof (obtained from the [proof of work](https://www.investopedia.com/terms/p/proof-work.asp) algorithm).

The blockchain class contains all the significant methods such as creation and addition of a new block, addition of new transaction info, the proof of work algorithm, the [consensus algorithm](https://www.investopedia.com/terms/c/consensus-mechanism-cryptocurrency.asp#:~:text=A%20consensus%20mechanism%20is%20a,systems%2C%20such%20as%20with%20cryptocurrencies.) (conflict resolution), and methods for registration of a new node.

## 🛠 API Endpoints:
**GET** `/chain`

*Retrieves the node's chain*
<hr>

**GET** `/mine`

*Mine/forge a new block*
<hr>

**POST** `/transactions/new`

*Add new transaction info*

Body:

`{
  "sender" : "sender-address",
  "recipient" : "recipient-address",
  "amount" : amount transferred
 }`

<hr>


**POST** `/nodes/register`

*Register new block*

Body:

`{
  "url" : "node-url"
 }`

<hr>

**GET** `/nodes/resolve`

*Resolve conflict between nodes*
