import pickle
from datetime import datetime

from Cryptodome.PublicKey import RSA

from BlockChainProject.Block import Block
from Transaction import Transaction
from typing import NamedTuple
import pathlib

class Blockchain (object):
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        self.difficulty = 3
        self.blockSize = 10
        self.reward = 20

    # Returns private and public key pair
    def generateKeys(self):
        key = RSA.generate(2048)
        privateKey = key.exportKey()
        scanner = open("generate/private.pem", "wb")
        scanner.write(privateKey)

        publicKey = key.publickey().export_key()
        scanner = open("generate/public.pem", "wb")
        scanner.write(publicKey)

        keyPair = []
        keyPair.append(privateKey)
        keyPair.append(publicKey)

        return keyPair

    def addFirstBlock(self):

        if (len(self.chain) > 1):
            return

        transactions = []

        genesis = Block(transactions, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0, self)
        genesis.prev = "N/A"
        self.chain.append(genesis)
        genesis.recordBlock()

    def addFirstBlockFromData(self, time):
        if (len(self.chain) > 1):
            return

        transactions = []

        genesis = Block(transactions, time, 0, self)
        genesis.prev = "N/A"
        self.chain.append(genesis)

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        block.prev = self.chain[-1].getHash()
        self.chain.append(block)

    def addTransaction(self, receiverKey, amount, publicKey, privateKey):

        if not publicKey:
            print("No Public Key Error")
            return False
        if not privateKey:
            print("No Private Key Error")
            return False
        if not receiverKey:
            print("No Receiver Error")
            return False
        if not amount:
            print("No Amount Error")
            return False

        transaction = Transaction(receiverKey, amount, publicKey)
        transaction.signTransaction(privateKey, publicKey)

        # If public key and private key match
        if transaction.isValidTransaction():
            file = open("mempool.csv", "a")

            file.write(str(receiverKey.publickey().export_key()) + "," + str(amount) + "," + str(publicKey.publickey().export_key()) + "\n")
            file.close()

            self.pendingTransactions.append(transaction)
            return True
        return False

    def getChain(self):
        return self.chain

    def minePendingTransactions(self, miner):

        pendingLength = len(self.pendingTransactions)
        if (pendingLength <= 0):
            print("There must be at least one transaction on block to mine")
            return False
        else:
            for i in range(0, pendingLength, self.blockSize):

                end = i + self.blockSize
                if i >= pendingLength:
                    end = pendingLength

                transactionSlice = self.pendingTransactions[i:end]

                newBlock = Block(transactionSlice, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), len(self.chain), self)

                hashValue = self.chain[-1].getHash()
                newBlock.prev = hashValue
                newBlock.mineBlock(self.difficulty)
                newBlock.recordBlock()
                self.chain.append(newBlock)
            print("Mining Transactions Success!")
            # remove all old pending transactions and add miner rewards to mempool
            file = open("mempool.csv", "w")
            file.truncate()
            file.close()

            rewardGiver = Transaction(miner, self.reward, None)

            file = open("mempool.csv", "a")
            file.write(str(miner.publickey().export_key()) + "," + str(self.reward) + "," + str("MINER REWARD") + "\n")
            file.close()

            self.pendingTransactions = [rewardGiver]
        return True

    def getWalletBalance(self, publicKey):

        if (publicKey is None):
            return 0

        balance = 0

        for block in self.chain:
            for transaction in block.transactions:

                if (transaction.getReceiver() is None):
                    continue

                if (transaction.getReceiver() == publicKey):
                    balance += int(transaction.getAmount())

                if (transaction.getSender() is None):
                    continue

                if (transaction.getSender() == publicKey):
                    balance -= int(transaction.getAmount())

        return balance

    def validateBlockchain(self):
        hash = None
        index = 0

        for block in self.chain:
            if (index == 0):
                hash = block.calculateHash()
                index += 1
                continue
            index += 1

            prevHash = block.getPrev()

            if (hash != prevHash and index > 3):
                return False
            hash = block.calculateHash()
        return True

    def getBlockChainFromData(self):
        blockCounter = 0
        for path in pathlib.Path("blockchain").iterdir():
            if path.is_file():
                blockCounter += 1
        print("Amount Blocks: " + str(blockCounter))
        self.chain = []
        self.pendingTransactions = []

        for x in range(0, blockCounter):
            blockPickled = open (("blockchain/block_" + str(x) + ".block"), "rb")
            blockData = pickle.load(blockPickled)

            transactions = blockData[0]
            for transaction in transactions:
                try:
                    transaction.publicKey = RSA.import_key(transaction.publicKey)
                    transaction.receiverKey = RSA.import_key(transaction.receiverKey)
                except:
                    transaction.publicKey = None
                    transaction.receiverKey = RSA.import_key(transaction.receiverKey)


            block = Block(blockData[0], blockData[1], blockData[2], self)
            block.prev = blockData[3]
            block.nonse = blockData[4]
            block.hash = blockData[5]
            # block.mineHash = blockData[6]

            self.chain.append(block)

class EmptyBlock(NamedTuple):
    blockType = str
    index = str
    hash = str
    prevHash = str
