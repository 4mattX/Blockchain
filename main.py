import base64
from datetime import datetime, time
from random import randint
import sys

from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15
import uvicorn
from fastapi.responses import JSONResponse



def createTestBlock():
    transactions = [Transaction("Matthew0", "Thuan0", 420),
                    Transaction("Matthew1", "Thuan1", 69),
                    Transaction("Matthew2", "Thuan2", 1738),
                    Transaction("Matthew3", "Thuan3", 8008),
                    Transaction("Matthew4", "Thuan4", 25)]

    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    block = Block(transactions, time, 0)

    for transaction in transactions:
        print("-----------------------")
        print("Sender -> " + transaction.getSender())
        print("Receiver -> " + transaction.getReceiver())
        print("Amount -> " + str(transaction.getAmount()))
        print("HashValue: -> " + transaction.getHash())
        print("-----------------------")
        print("")

def createTestBlockChain():
    blockChain = Blockchain()

    transactions = [];
    block = Block(getRandomTransactions(), time(), 0, blockChain)
    blockChain.addBlock(block)
    block = Block(getRandomTransactions(), time(), 1, blockChain)
    blockChain.addBlock(block)
    block = Block(getRandomTransactions(), time(), 2, blockChain)
    blockChain.addBlock(block)
    block = Block(getRandomTransactions(), time(), 3, blockChain)
    blockChain.addBlock(block)

    for block in blockChain.getChain():
        print("Hash -> " + block.getHash())
        print("Prev -> " + block.getPrev())
        print("Transactions -> ")
        for transaction in block.getTransactions():
            print("    sender: " + str(transaction.getSender()) + "  receiver: " + str(transaction.getReceiver()) + "  amount: " + str(transaction.getAmount()))
        print("-----------------------------------------------------------------------------")

def getRandomTransactions():
    transactions = []

    sender = 'me'
    receiver = 'you'

    amtTransactions = randint(1, 10)

    for x in range(amtTransactions):
        amount = randint(1, 1000)
        transactions.append(Transaction(sender, receiver, amount))

    return transactions

def mineTestBlock():
    blockchain = Blockchain()

    senderKey = blockchain.generateKeys()
    receiverKey = blockchain.generateKeys()

    transaction = Transaction("Sender", "Receiver", 10, senderKey, receiverKey)
    blockchain.pendingTransactions.append(transaction)
    blockchain.minePendingTransactions("Matthew")

    print("Length: ", len(blockchain.chain))

def testValidTransaction():
    blockchain = Blockchain()

    keyPair = blockchain.generateKeys()

    privateKey = keyPair[0]
    publicKey = keyPair[1]

    keyPair2 = blockchain.generateKeys()
    fakePublicKey = keyPair2[1]

    # print(privateKey)
    # print(publicKey)
    #
    # newPrivateKey = RSA.import_key(privateKey)
    # newPublicKey = RSA.import_key(publicKey)
    #
    # message = b'very nice message'
    # h = SHA256.new(message)
    # signature = pkcs1_15.new(newPrivateKey).sign(h)
    #
    # try:
    #     pkcs1_15.new(newPublicKey).verify(h, signature)
    #     print("Valid")
    # except (ValueError, TypeError):
    #     print("INVALID")

    print(privateKey)
    print(publicKey)

    blockchain.addTransaction("Receiver", 10, publicKey, privateKey)

    # blockchain.minePendingTransactions(publicKey)

def simulateBlockchain():
    blockchain = None
    firstTransaction = True

    loop = True
    while (loop):
        print("1 - Add Transaction")
        print("2 - Mine Block")
        print("3 - Print Pending Transactions")
        print("4 - Print Blockchain")
        print("5 - Generate Wallet Keys")
        print("6 - Balance of Sender")
        print("7 - Balance of Receiver")
        print("8 - Load Blockchain from file")
        print("9 - Validate Blockchain")
        print("-------------------------------")
        value = input("-> ")

        if (value == "1"):

            if (firstTransaction):
                blockchain = Blockchain()
                blockchain.addFirstBlock()
                firstTransaction = False

            print("In the receiver directory place the correct Public Key")
            print("In the sender directory place both your Private and Public Key")
            amount = input("Amount -> ")

            with open('receiver/public.pem', "rb") as file:
                receiverKey = RSA.import_key(file.read())

            with open('sender/public.pem', "rb") as file:
                publicKey = RSA.import_key(file.read())

            with open('sender/private.pem', "rb") as file:
                privateKey = RSA.import_key(file.read())


            blockchain.addTransaction(receiverKey, amount, publicKey, privateKey)

        if (value == "2"):

            if (firstTransaction):
                blockchain = Blockchain()
                blockchain.addFirstBlock()
                firstTransaction = False

            with open('miner/public.pem', "rb") as file:
                minerKey = RSA.import_key(file.read())

            blockchain.minePendingTransactions(minerKey)

        if (value == "3"):

            if (firstTransaction):
                blockchain = Blockchain()
                blockchain.addFirstBlock()
                firstTransaction = False

            with open("mempool.csv", "rb") as file:
                print(file.read())


        if (value == "4"):

            if (firstTransaction):
                blockchain = Blockchain()
                blockchain.addFirstBlock()
                firstTransaction = False

            for block in blockchain.getChain():
                print("Hash -> " + block.getHash())
                print("Prev -> " + block.getPrev())
                print("Transactions -> ")
                for transaction in block.getTransactions():
                    print("    sender: " + str(transaction.getSender()) + "  receiver: " + str(transaction.getReceiver()) + "  amount: " + str(transaction.getAmount()))
                print("-----------------------------------------------------------------------------")

        if (value == "5"):
            if (firstTransaction):
                blockchain = Blockchain()
                blockchain.addFirstBlock()
                firstTransaction = False

            keyPair = blockchain.generateKeys()
            print ("Check Files")

        if (value == "6"):

            if (firstTransaction):
                blockchain = Blockchain()
                blockchain.addFirstBlock()
                firstTransaction = False

            with open('sender/public.pem', "rb") as file:
                senderKey = RSA.import_key(file.read())
            balance = blockchain.getWalletBalance(senderKey)
            print("")
            print("Balance = " + str(balance))
            print("")

        if (value == "7"):

            if (firstTransaction):
                blockchain = Blockchain()
                blockchain.addFirstBlock()
                firstTransaction = False

            with open('receiver/public.pem', "rb") as file:
                receiverKey = RSA.import_key(file.read())
            balance = blockchain.getWalletBalance(receiverKey)
            print("")
            print("Balance = " + str(balance))
            print("")

        if (value == "8"):

            if (firstTransaction):
                blockchain = Blockchain()
                blockchain.addFirstBlock()
                firstTransaction = False

            blockchain.getBlockChainFromData()
            print("Loaded Blockchain from data")
            print("")

        if (value == "9"):
            print("")
            if (blockchain.validateBlockchain()):
                print("Valid Blockchain")
            else:
                print("Invalid Blockchain")
            print("")

if __name__ == '__main__':
    simulateBlockchain()