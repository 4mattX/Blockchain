from datetime import datetime
import hashlib
from Cryptodome.PublicKey import RSA
from base64 import b64decode, b64encode
from Cryptodome.Hash import SHA256, SHA384
from Cryptodome.Signature import pkcs1_15
from Cryptodome import Signature
from Cryptodome import Hash


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
        # if (self.hash != self.calculateHash()):
        #     print("INVALID Transaction")
        #     return False
        #
        # newPrivateKey = privateKey
        # newPublicKey = publicKey
        #
        # message = b'Verifier Message'
        # h = SHA256.new(message)
        # signature = pkcs1_15.new(newPrivateKey).sign(h)
        #
        # try:
        #     pkcs1_15.new(newPublicKey).verify(h, signature)
        #     print("Valid Transaction")
        #     self.signed = True
        #     return True
        # except (ValueError, TypeError):
        #     print("INVALID Transaction signature")
        # return False
        signer = Signature.pkcs1_15.new(privateKey)
        signatureHash = Hash.SHA384.new()
        signatureHash.update(publicKey.publickey().export_key())
        self.signature = signer.sign(signatureHash)
        print("Transaction Here ->" + str(self.signature))
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

    def getSignature(self):
        return self.signature

