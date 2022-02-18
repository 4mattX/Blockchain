from datetime import datetime
import hashlib
from Cryptodome.PublicKey import RSA
from base64 import b64decode, b64encode
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15


class Transaction (object):
    def __init__(self, sender, receiver, amount, senderKey, key):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.senderKey = senderKey
        self.receiverKey = key
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

        newPrivateKey = RSA.import_key(privateKey)
        newPublicKey = RSA.import_key(publicKey)

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
        inputString = self.sender + self.receiver + str(self.amount) + str(self.time)

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

