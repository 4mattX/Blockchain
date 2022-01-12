from datetime import datetime
import hashlib

class index (object):
    def __init__(self, blockNumber):
        #hash value of previous block
        self.blockNumber = blockNumber
        self.hash = self.calculateHash()

    def calculateHash(self):
        # Hash String Value that will be converted into a hash value
        inputString = self.blockNumber

        # SHA256 HashValue
        hashValue = hashlib.sha256(inputString.encode('utf-8')).hexdigest()

        return hashValue

    def getHash(self):
        return self.hash