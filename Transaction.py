from datetime import datetime
import hashlib
from Cryptodome.PublicKey import RSA


class Transaction (object):
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash = self.calculateHash()
        self.signed = False

    # def signTransaction(self):

    def calculateHash(self):
        # Hash String Value that will be converted into a hash value
        inputString = self.sender + self.receiver + str(self.amount) + str(self.time)

        # SHA256 HashValue
        hashValue = hashlib.sha256(inputString.encode('utf-8')).hexdigest()

        return hashValue

    def signTransaction(self, key, senderKey):
        if (self.hash != self.calculateHash()):
            print("!!! Invalid Transaction !!!")
            return False

        # Converting StringKeys into Byte Data Structure
        byteKey = RSA.importKey(key.encode("ASCII"))
        byteSenderKey = RSA.importKey(senderKey.encode("ASCII"))

        if (key != senderKey):
            print("Tampered Transaction Error")
            return False

        self.signed = True;
        print("Transaction Signed")
        return True


        print("Transaction Signed")
        self.signed = True
        return True

    def isValidTransaction(self):
        if (self.hash != self.calculateHash()):
            return False

        if(self.sender == self.receiver):
            return False

        if not self.signed:
            return False

        return True

    def getSender(self):
        return self.sender

    def getReceiver(self):
        return self.receiver

    def getAmount(self):
        return self.amount

    def getHash(self):
        return self.hash

