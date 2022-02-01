import hashlib
import json


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

    def calculateHash(self):

        transactionsHash = ''

        inputUnicode = 0
        for transaction in self.transactions:
            transactionsHash += transaction.getHash()

        hashString = str(self.time) + transactionsHash + self.getPrev() + str(self.getNonse)
        encodedHash = json.dumps(hashString, sort_keys=True).encode()

        return hashlib.sha256(encodedHash).hexdigest()

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