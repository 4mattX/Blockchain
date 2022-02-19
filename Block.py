import hashlib
import json
from time import sleep


class Block (object):
    def __init__(self, transactions, time, index):
        #record of transaction sender, receiver, amount transfered, and time of transaction processed
        self.transactions = transactions

        #time of this block's creation
        self.time = time

        #interger value of the block created
        self.index = index

        self.prev = ''
        self.nonse = 0
        self.hash = self.calculateHash()
        self.recordBlock()

    def calculateHash(self):

        transactionsHash = ''

        inputUnicode = 0
        for transaction in self.transactions:
            transactionsHash += transaction.getHash()

        hashString = str(self.time) + transactionsHash + self.getPrev() + str(self.getNonse())
        encodedHash = json.dumps(hashString, sort_keys=True).encode()

        return hashlib.sha256(encodedHash).hexdigest()

    def mineBlock(self, difficulty):
        solutionArray = []
        for i in range (0, difficulty):
            solutionArray.append(i)

        solutionString = map(str, solutionArray)
        hashPuzzle = ''.join(solutionString)

        while self.hash[0:difficulty] != hashPuzzle:
            self.nonse += 1
            self.hash = self.calculateHash()
            print("Nonse: ", self.nonse)
            print("Hash Attempt: ", self.hash)
            print(("Hash We Want: ", hashPuzzle, "..."))
            # sleep(0.8)
        print("")
        print("Block Mined! Nonse: " + str(self.getNonse()))
        return True

    def addTransaction(self, transaction):
        self.transactions.add(transaction)

    def getPrev(self):
        return self.prev

    def getNonse(self):
        return self.nonse

    def getTransactions(self):
        return self.transactions

    def getHash(self):
        return self.hash

    def recordBlock(self):
        message = "-=-= START OF BLOCK =-=-" + "\n"
        message += "Block #" + str(self.index) + "\n"
        message += "Hash: " + self.getHash() + "\n"
        message += "Prev: " + self.getPrev() + "\n"
        message += "Transactions:" + "\n"
        for transaction in self.getTransactions():
            try:
                message += ("    sender: " + str(transaction.getSender().publickey().export_key()) + "  receiver: " + str(transaction.getReceiver().publickey().export_key()) + "  amount: " + str(transaction.getAmount())) + "\n"
            except (ValueError, AttributeError):
                message += ("    sender: " + str(transaction.getSender()) + "  receiver: " + str(transaction.getReceiver().publickey().export_key()) + "  amount: " + str(transaction.getAmount())) + "\n"
        message += "-=-= END OF BLOCK =-=-" + "\n"

        file = open("blockchain.txt", "a")
        file.write(message)
        file.close()

