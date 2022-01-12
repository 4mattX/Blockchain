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
        #record of transaction sender, receiver, amount transfered, and time of transaction processed
        self.transactions = transactions

        #time of this block's creation
        self.time = time

        #header that SHOULD match the previous block's Proof of Work hash function, if not this block is invalid
        self.prev = calculateHash(transactions)

        #interger value of the block created
        self.index = index
        print("Block created")

    def addTransaction(self, transaction):
        self.transactions.add(transaction)