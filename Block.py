import hashlib

# Adds UniCoded representations of Hashes together then converts that summation into a new hashValue
def calculateHash(trans):
    inputUnicode = 0
    for tran in trans:
        hash = tran.getHash()

        for i in range (len(hash)):
            inputUnicode += ord(hash[i])

    # SHA256 HashValue
    hashValue = hashlib.sha256(str(inputUnicode).encode('utf-8')).hexdigest()
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