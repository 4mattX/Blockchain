class Blockchain (object):
    def __init__(self):
        self.chain = []

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        self.chain.append(block)