import hashlib


def calculateHash(trans):

    inputString = ''

    for tran in trans:
        inputString += tran.getHash()

    # SHA256 HashValue
    hashValue = hashlib.sha256(inputString.encode('utf-8')).hexdigest()
    return hashValue


class Block (object):
    def __init__(self, transactions, time, index):
        self.transactions = transactions
        self.time = time
        self.prev = calculateHash(transactions)
        self.index = index
        print("Block created")

    def addTransaction(self, transaction):
        self.transactions.add(transaction)