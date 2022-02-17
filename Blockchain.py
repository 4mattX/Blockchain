from datetime import datetime

from crypto.PublicKey import RSA

from Block import Block
from Transaction import Transaction


class Blockchain (object):
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        self.difficulty = 3
        self.blockSize = 10
        self.reward = 20
        self.addFirstBlock()

    # REWORK THIS!
    def generateKeys(self):
        key = RSA.generate(2048)
        privateKey = key.exportKey()
        scanner = open("private.pem", "wb")
        scanner.write(privateKey)

        publicKey = key.publickey().export_key()
        scanner = open("receiver.pem", "wb")
        scanner.write(publicKey)

    def addFirstBlock(self):
        transactions = []
        # transactions.append(Transaction('dat', 'boi', 420))
        genesis = Block(transactions, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)
        genesis.prev = "N/A"
        self.chain.append(genesis)

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        block.prev = self.chain[-1].getHash()
        self.chain.append(block)

    def addTransaction(self, sender, receiver, amount, key, senderKey):
        transaction = Transaction(sender, receiver, amount)

        if not sender:
            print("No Sender Error")
            return False
        if not receiver:
            print("No Receiver Error")
            return False
        if not amount:
            print("No Amount Error")
            return False

        transaction.signTransaction(key, senderKey)
        self.pendingTransactions.append(transaction)

    def getChain(self):
        return self.chain

    def minePendingTransactions(self, miner):

        pendingLength = len(self.pendingTransactions);
        if (pendingLength <= 0):
            print("There must be at least one transaction on block to mine")
            return False
        else:
            for i in range(0, pendingLength, self.blockSize):

                end = i + self.blockSize
                if i >= pendingLength:
                    end = pendingLength

                transactionSlice = self.pendingTransactions[i:end]

                newBlock = Block(transactionSlice, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), len(self.chain))

                hashValue = self.getLastBlock().getHash()
                newBlock.prev = hashValue
                newBlock.mineBlock(self.difficulty)
                self.chain.append(newBlock)
            print("Mining Transactions Success!")

            rewardGiver = Transaction("Dat Boi Rewards", miner, self.reward)
            self.pendingTransactions = [rewardGiver]
        return True

