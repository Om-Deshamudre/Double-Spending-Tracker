from flask import Flask, render_template
import time
import random
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Simulated Blockchain Environment Setup
class Blockchain:
    def __init__(self):
        self.transactions = set()  # Use a set to store unique transaction IDs
        self.graph = nx.DiGraph()  # Graph to represent transactions

    def add_transaction(self, transaction):
        self.transactions.add(transaction.txid)
        self.graph.add_node(transaction.txid)

    def validate_transaction(self, transaction):
        # Check if the transaction ID is already in the set (indicating a double-spending attempt)
        if transaction.txid in self.transactions:
            return False  # Reject the transaction
        else:
            return True   # Accept the transaction

    def track_transaction(self, transaction):
        for input_ in transaction.inputs:
            prev_txid = input_["prev_txid"]
            self.graph.add_edge(prev_txid, transaction.txid)

        # If the transaction is a fraudulent one, add an edge to represent the new user
        if transaction.txid.startswith("fake_txid"):
            new_user_txid = f"new_user_txid_{random.randint(1000, 9999)}"
            self.graph.add_edge(transaction.txid, new_user_txid)

# Define the Fraudulent Transaction
class FakeTransaction:
    def __init__(self, txid, inputs, outputs, fees, signatures, timestamp, metadata=None):
        self.txid = txid
        self.inputs = inputs
        self.outputs = outputs
        self.fees = fees
        self.signatures = signatures
        self.timestamp = timestamp
        self.metadata = metadata if metadata else {}

    def display(self):
        print("Transaction ID:", self.txid)
        print("Timestamp:", self.timestamp)
        print("Inputs:")
        for input_ in self.inputs:
            print("\tPrevious Transaction ID:", input_["prev_txid"])
            print("\tOutput Index:", input_["output_index"])
            print("\tScriptSig:", input_["script_sig"])
        print("Outputs:")
        for output in self.outputs:
            print("\tAmount:", output["amount"])
            print("\tScriptPubKey:", output["script_pubkey"])
        print("Fees:", self.fees)
        print("Signatures:", self.signatures)
        print("Metadata:", self.metadata)

# Algorithm Development: Detect and Track Double-Spending Transactions
def detect_double_spending(blockchain, transaction):
    if blockchain.validate_transaction(transaction):
        blockchain.add_transaction(transaction)
        blockchain.track_transaction(transaction)
        print("Transaction added to the blockchain:", transaction.txid)
    else:
        print("Double-spending detected:", transaction.txid)
        transaction.display()
        # Additional tracking and reporting logic can be added here

# Create a blockchain instance
blockchain = Blockchain()

# Generate Legitimate Transactions
for _ in range(10):
    txid = f"txid_{random.randint(1000, 9999)}"
    inputs = [{"prev_txid": f"prev_txid_{random.randint(1000, 9999)}", "output_index": random.randint(0, 9), "script_sig": f"script_sig_{random.randint(1000, 9999)}"}]
    outputs = [{"amount": random.randint(1, 10), "script_pubkey": f"script_pubkey_{random.randint(1000, 9999)}"}]
    fees = random.randint(0, 2)
    signatures = [f"signature_{random.randint(1000, 9999)}"]
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    transaction = FakeTransaction(txid, inputs, outputs, fees, signatures, timestamp)
    detect_double_spending(blockchain, transaction)

# Generate Fraudulent Double-Spending Transaction
fake_txid = "fake_txid"
fake_inputs = [{"prev_txid": "prev_txid_1234", "output_index": 0, "script_sig": "script_sig_5678"}]
fake_outputs = [{"amount": 10, "script_pubkey": "script_pubkey_9012"}]
fake_fees = 1
fake_signatures = ["signature_3456"]
fake_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
fake_transaction = FakeTransaction(fake_txid, fake_inputs, fake_outputs, fake_fees, fake_signatures, fake_timestamp)
detect_double_spending(blockchain, fake_transaction)

# Flask route to serve the graph
@app.route("/")
def index():
    # Draw the graph
    pos = nx.spring_layout(blockchain.graph)
    plt.figure(figsize=(10, 6))
    nx.draw(blockchain.graph, pos, with_labels=True, node_size=800, node_color="skyblue", font_size=10, edge_color="gray", width=0.5)
    plt.title("Blockchain Transaction Graph")

    # Convert the graph to a base64 encoded image
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    # Render the template with the base64 encoded image
    return render_template("index.html", img_base64=img_base64)

if __name__ == "__main__":
    app.run(debug=True)
