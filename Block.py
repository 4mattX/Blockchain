import base64
import hashlib
import json
import pickle
import time
from base64 import b64decode
from time import sleep

from Cryptodome.Signature.pkcs1_15 import PKCS115_SigScheme

from BlockChainProject import Blockchain
from BlockChainProject.Wallet import Wallet
from Cryptodome.Hash import SHA256, SHA384
from Cryptodome.Signature import pkcs1_15
from Cryptodome import Signature
from Cryptodome import Hash
from Cryptodome.PublicKey import RSA
from numba import jit, cuda


class Block (object):
    def __init__(self, transactions, time, index, blockchain):
        #record of transaction sender, receiver, amount transfered, and time of transaction processed
        self.transactions = transactions
        self.blockchain = blockchain

        #time of this block's creation
        self.time = time

        #interger value of the block created
        self.index = index

        self.prev = ''
        self.nonse = 0
        self.hash = self.calculateHash()


    def calculateHash(self):

        transactionsHash = ''

        inputUnicode = 0
        for transaction in self.transactions:
            transactionsHash += transaction.getHash()

        hashString = str(self.time) + transactionsHash + self.getPrev() + str(self.getNonse())
        encodedHash = json.dumps(hashString, sort_keys=True).encode()

        return hashlib.sha256(encodedHash).hexdigest()


    def mineBlock(self):
        appRef = self.blockchain.app
        difficulty = self.blockchain.difficulty

        solutionArray = []
        for i in range (0, difficulty):
            solutionArray.append(i)

        solutionString = map(str, solutionArray)
        hashPuzzle = ''.join(solutionString)

        while self.hash[0:difficulty] != hashPuzzle:

            if (self.blockchain.killMine):
                return

            self.nonse += 1

            # if (self.nonse % 100 == 0):
            self.blockchain.app.nonse = self.nonse
            self.blockchain.app.hashRate += 1
                # appRef.mineBlockchain()

            # if (self.nonse % 100 == 0):
            #     print(self.blockchain.app.nonse)
            #     appRef.mineBlockchain()

            self.hash = self.calculateHash()
            # print("Nonse: ", self.nonse)
            # print("Hash Attempt: ", self.hash)
            # print(("Hash We Want: ", hashPuzzle, "..."))

        # Make sure each transaction is valid in the amount
        # Makes a list of all wallets

        wallets = []
        invalidWallets = []

        blockchain = self.blockchain

        for transaction in self.transactions:
            inWallets = False

            # Checking signature of transaction
            if (transaction.getSignature() != None):
                try:
                    verifier = Signature.pkcs1_15.new(transaction.getSender())
                    hash = Hash.SHA256.new()
                    hash.update(transaction.getSender().publickey().export_key())
                    verifier.verify(hash, transaction.getSignature())

                    print("VALID SIGNATURE")
                except ValueError:
                    self.transactions.remove(transaction)
                    continue

            for wallet in wallets:

                if (transaction.getSender() is None):
                    continue
                if (wallet.getPublicKey() is None):
                    continue

                if (str(wallet.getPublicKey().publickey().export_key()) == str(transaction.getSender().publickey().export_key())):
                    inWallets = True

            if (inWallets == False):
                newWallet = Wallet(transaction.getSender(), blockchain.getWalletBalance(transaction.getSender()))
                wallets.append(newWallet)

        for wallet in wallets:
            for transaction in self.transactions:

                if (transaction.getSender() is None):
                    continue
                if (wallet.getPublicKey() is None):
                    continue

                if (str(transaction.getSender().publickey().export_key()) == str(wallet.getPublicKey().publickey().export_key())):
                    wallet.removeBalance(int(transaction.getAmount()))

                    if (wallet.getBalance() < 0):
                        invalidWallets.append(wallet)

        for transaction in self.transactions:
            for invalidWallet in invalidWallets:

                if (transaction.getSender() is None):
                    continue
                if (wallet.getPublicKey() is None):
                    continue

                if (str(transaction.getSender().publickey().export_key()) == str(invalidWallet.getPublicKey().publickey().export_key())):
                    try:
                        self.transactions.remove(transaction)
                        print("Wallet address with balance < 0 Found!")
                        print(str(invalidWallet.getPublicKey().publickey().export_key()))
                        continue
                    except:
                        continue


        print("")
        print("Block Mined! Nonse: " + str(self.getNonse()))
        return self

    def addTransaction(self, transaction):
        self.transactions.add(transaction)

    def getPrev(self):
        return self.prev

    def getNonse(self):
        return self.nonse

    def getTransactions(self):
        return self.transactions

    def getHash(self):
        return self.hash

    def recordBlock(self):
        fileName = "blockchain/block_" + str(self.index) + ".block"

        # Must Serialize all transactions first
        serialTransactions = []
        for transaction in self.transactions:
            try:
                transaction.publicKey = transaction.publicKey.publickey().export_key()
                transaction.receiverKey = transaction.receiverKey.publickey().export_key()
            except AttributeError:
                transaction.publicKey = ""
                transaction.receiverKey = transaction.receiverKey.publickey().export_key()
                serialTransactions.append(transaction)
                continue
            serialTransactions.append(transaction)

        emptyBlock = (serialTransactions, self.time, self.index, self.prev, self.nonse, self.hash)

        filehandler = open(fileName, 'wb')
        pickle.dump(emptyBlock, filehandler)
        filehandler.close()

        # After Serialization and recording must un-serialize
        for transaction in self.transactions:
            try:
                transaction.publicKey = RSA.import_key(transaction.publicKey)
                transaction.receiverKey = RSA.import_key(transaction.receiverKey)
            except:
                transaction.publicKey = None
                transaction.receiverKey = RSA.import_key(transaction.receiverKey)

        # message = "DB,"
        # message += str(self.index) + ","
        # message += str(self.getHash()) + ","
        # message += str(self.getPrev()) + ","
        # message += str(self.time) + ","
        # message += "\n"
        # for transaction in self.getTransactions():
        #     try:
        #         message += (str(transaction.getSender().publickey().export_key()) + "," +
        #                     str(transaction.getReceiver().publickey().export_key()) + "," +
        #                     str(transaction.getAmount()) + "," +
        #                     str(transaction.getSignature()) + "," +
        #                     str(transaction.getTime())) + "," + "\n"
        #     # Occurs when Miner Rewards are given
        #     except (ValueError, AttributeError):
        #         message += (str(transaction.getSender()) + "," +
        #                     str(transaction.getReceiver().publickey().export_key()) + "," +
        #                     str(transaction.getAmount()) + "," +
        #                     str(transaction.getSignature()) + "," +
        #                     str(transaction.getTime())) + "," + "\n"
        #
        # file = open("blockchain.csv", "a")
        # file.write(message)
        # file.close()

