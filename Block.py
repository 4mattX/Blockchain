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
        self.transactions = transactions
        self.time = time
        self.prev = calculateHash(transactions)
        self.index = index
        print("Block created")

    def addTransaction(self, transaction):
        self.transactions.add(transaction)