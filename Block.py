class Block (object):
    def __init__(self, transactions, time, index, message):
        self.transactions = transactions
        self.time = time
        self.prev = ''
        self.index = index
        self.message = message

    def createHash(self):
        hash = ""