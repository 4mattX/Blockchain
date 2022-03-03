from datetime import datetime

from Cryptodome.PublicKey import RSA

from BlockChainProject.Block import Block
from Transaction import Transaction

class Blockchain (object):
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        self.difficulty = 3
        self.blockSize = 10
        self.reward = 20
        self.addFirstBlock()

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

            #brute force code to add a overwriting record of the latest transaction to be broadcasted
            file = open("TempMempool.txt", "w")
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

                hashValue = self.getLastBlock().getHash()
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
