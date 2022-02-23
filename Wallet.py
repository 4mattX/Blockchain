
class Wallet(object):
    def __init__(self, publicKey, balance):
        self.publicKey = publicKey
        self.balance = balance

    def getPublicKey(self):
        return self.publicKey

    def getBalance(self):
        return self.balance

    def addBalance(self, amount):
        self.balance += amount

    def removeBalance(self, amount):
        self.balance -= amount

    def setBalance(self, amount):
        self.balance = amount
