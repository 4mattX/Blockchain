import hashlib
import json
from time import sleep

from BlockChainProject import Blockchain
from BlockChainProject.Wallet import Wallet


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

    def mineBlock(self, difficulty):
        solutionArray = []
        for i in range (0, difficulty):
            solutionArray.append(i)

        solutionString = map(str, solutionArray)
        hashPuzzle = ''.join(solutionString)

        while self.hash[0:difficulty] != hashPuzzle:
            self.nonse += 1
            self.hash = self.calculateHash()
            print("Nonse: ", self.nonse)
            print("Hash Attempt: ", self.hash)
            print(("Hash We Want: ", hashPuzzle, "..."))

        # Make sure each transaction is valid in the amount
        # Makes a list of all wallets
        wallets = []
        invalidWallets = []

        blockchain = self.blockchain

        for transaction in self.transactions:
            inWallets = False

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
                    self.transactions.remove(transaction)
                    print("Wallet address with balance < 0 Found!")
                    print(str(invalidWallet.getPublicKey().publickey().export_key()))

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
        message = "-=-= START OF BLOCK =-=-" + "\n"
        message += "Block #" + str(self.index) + "\n"
        message += "Hash: " + self.getHash() + "\n"
        message += "Prev: " + self.getPrev() + "\n"
        message += "Transactions:" + "\n"
        for transaction in self.getTransactions():
            try:
                message += ("    sender: " + str(transaction.getSender().publickey().export_key()) + "  receiver: " + str(transaction.getReceiver().publickey().export_key()) + "  amount: " + str(transaction.getAmount())) + "\n"
            except (ValueError, AttributeError):
                message += ("    sender: " + str(transaction.getSender()) + "  receiver: " + str(transaction.getReceiver().publickey().export_key()) + "  amount: " + str(transaction.getAmount())) + "\n"
        message += "-=-= END OF BLOCK =-=-" + "\n"

        file = open("blockchain.txt", "a")
        file.write(message)
        file.close()

