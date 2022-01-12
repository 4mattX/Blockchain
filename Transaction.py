from datetime import datetime
import hashlib


class Transaction (object):
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash = self.calculateHash()

    def calculateHash(self):
        # Hash String Value that will be converted into a hash value
        inputString = self.sender + self.receiver + str(self.amount) + str(self.time)

        # SHA256 HashValue
        hashValue = hashlib.sha256(inputString.encode('utf-8')).hexdigest()

        return hashValue

    def getHash(self):
        return self.hash
