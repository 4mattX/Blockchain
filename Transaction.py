import binascii
from datetime import datetime
import hashlib
from Cryptodome.PublicKey import RSA
from base64 import b64decode, b64encode
from Cryptodome.Hash import SHA256, SHA384
from Cryptodome.Signature import pkcs1_15
from Cryptodome import Signature
from Cryptodome import Hash
from Cryptodome.Signature.pkcs1_15 import PKCS115_SigScheme


class Transaction (object):
    def __init__(self, receiverKey, amount, publicKey):
        self.receiverKey = receiverKey
        self.publicKey = publicKey
        self.amount = amount
        self.signature = None
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash = self.calculateHash()
        self.signed = False

    # FIX LATER
    def signTransaction(self, privateKey, publicKey):
        signer = Signature.pkcs1_15.new(privateKey)
        signatureHash = Hash.SHA256.new()
        signatureHash.update(publicKey.publickey().export_key())
        self.signature = signer.sign(signatureHash)
        self.signed = True

    def calculateHash(self):
        # Hash String Value that will be converted into a hash value
        inputString = str(self.publicKey) + str(self.receiverKey) + str(self.amount) + str(self.time)

        # SHA256 HashValue
        hashValue = hashlib.sha256(inputString.encode('utf-8')).hexdigest()

        return hashValue

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

    def getTime(self):
        return self.time

    def getSignature(self):
        return self.signature

    def setSignature(self, signature):
        self.signature = signature

    def setDate(self, time):
        self.time = time

    def resetHash(self):
        self.hash = self.calculateHash()

