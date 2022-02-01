from datetime import datetime

from Block import Block
from Transaction import Transaction


class Blockchain (object):
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        self.addFirstBlock()

    def addFirstBlock(self):
        transactions = []
        # transactions.append(Transaction('dat', 'boi', 420))
        genesis = Block(transactions, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)
        genesis.prev = "N/A"
        self.chain.append(genesis)

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        block.prev = self.chain[-1].getHash()
        self.chain.append(block)

    def addTransaction(self, sender, receiver, amount, key, senderKey):
        transaction = Transaction(sender, receiver, amount)

        if not sender:
            print("No Sender Error")
            return False
        if not receiver:
            print("No Receiver Error")
            return False
        if not amount:
            print("No Amount Error")
            return False

        transaction.signTransaction(key, senderKey)
        self.pendingTransactions.append(transaction)

    def getChain(self):
        return self.chain

