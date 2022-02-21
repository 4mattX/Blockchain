from datetime import datetime
import hashlib
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15


class Transaction (object):
    def __init__(self, receiverKey, amount, publicKey, privateKey):
        self.receiverKey = receiverKey
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.amount = amount
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash = self.calculateHash()
        self.signed = False


    # FIX LATER
    def signTransaction(self, privateKey, publicKey):
        if (self.hash != self.calculateHash()):
            print("INVALID Transaction")
            return False

        # if(str(key.publickey().export_key()) != str(senderKey.publickey().export_key())):
        #     print("INVALID Transaction signature")
        #     return False

        newPrivateKey = privateKey
        newPublicKey = publicKey

        message = b'Verifier Message'
        h = SHA256.new(message)
        signature = pkcs1_15.new(newPrivateKey).sign(h)

        try:
            pkcs1_15.new(newPublicKey).verify(h, signature)
            print("Valid Transaction")
            self.signed = True
            return True
        except (ValueError, TypeError):
            print("INVALID Transaction signature")
        return False


    def calculateHash(self):
        # Hash String Value that will be converted into a hash value
        inputString = str(self.publicKey) + str(self.receiverKey) + str(self.amount) + str(self.time)

        # SHA256 HashValue
        hashValue = hashlib.sha256(inputString.encode('utf-8')).hexdigest()

        return hashValue

    # def signTransaction(self, key, senderKey):
    #     if (self.hash != self.calculateHash()):
    #         print("!!! Invalid Transaction !!!")
    #         return False
    #
    #     # Converting StringKeys into Byte Data Structure
    #     byteKey = RSA.importKey(key.encode("ASCII"))
    #     byteSenderKey = RSA.importKey(senderKey.encode("ASCII"))
    #
    #     if (byteKey != byteSenderKey):
    #         print("Tampered Transaction Error")
    #         return False
    #
    #     self.signed = True
    #     print("Transaction Signed")
    #     return True


    def isValidTransaction(self):
        if (self.hash != self.calculateHash()):
            return False

        if(self.publicKey == self.receiverKey):
            return False

        if not self.signed:
            return False

        return True

    def getSender(self):
        return self.publicKey

    def getReceiver(self):
        return self.receiverKey

    def getAmount(self):
        return self.amount

    def getHash(self):
        return self.hash

