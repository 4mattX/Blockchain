from datetime import datetime, time
from random import randint
import sys

from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return {"Home Page"}

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
    block = Block(getRandomTransactions(), time(), 0)
    blockChain.addBlock(block)
    block = Block(getRandomTransactions(), time(), 1)
    blockChain.addBlock(block)
    block = Block(getRandomTransactions(), time(), 2)
    blockChain.addBlock(block)
    block = Block(getRandomTransactions(), time(), 3)
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
    blockchain = Blockchain()

    loop = True
    while (loop):
        print("1 - Add Transaction")
        print("2 - Mine Block")
        print("3 - Print Pending Transactions")
        print("4 - Print Blockchain")
        print("5 - Generate Wallet Keys")
        print("6 - End Program")
        print("-------------------------------")
        value = input("-> ")

        if (value == "1"):
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

            print("")
            print("Added to pending transaction MEMPOOL")
            print("added to temporary pending transaction TEMPMEMPOOL")
            print("")

        if (value == "2"):
            with open('miner/public.pem', "rb") as file:
                minerKey = RSA.import_key(file.read())

            blockchain.minePendingTransactions(minerKey)

        if (value == "3"):
            with open("mempool.txt", "rb") as file:
                print(file.read())


        if (value == "4"):
            for block in blockchain.getChain():
                print("Hash -> " + block.getHash())
                print("Prev -> " + block.getPrev())
                print("Transactions -> ")
                for transaction in block.getTransactions():
                    print("    sender: " + str(transaction.getSender()) + "  receiver: " + str(transaction.getReceiver()) + "  amount: " + str(transaction.getAmount()))
                print("-----------------------------------------------------------------------------")

        if (value == "5"):
            keyPair = blockchain.generateKeys()
            print ("Check Files")

        if (value == "6"):
            break

if __name__ == '__main__':
    simulateBlockchain()

#sends a transaction object
@app.post("/addPendingTransaction/{receiverKey}/{amount}/{publicKey}/{privateKey}")
def APIaddPendingTransactionData(receiverKey: str, amount: float, publicKey: str):
    file = open("mempool.txt", "a")
    file.write(r"b'-----BEGIN PUBLIC KEY-----\n"+receiverKey+r"\n-----END PUBLIC KEY-----',"+amount+r",b'-----BEGIN PUBLIC KEY-----\n"
               +publicKey+r"\n----END PUBLIC KEY-----'")
    file.close()
    return {"API add pending transaction processed."}

@app.post("/addPendingTransaction2/{transaction}")
def APIaddPendingTransaction2(transaction: Transaction):
    file = open("mempool.txt", "a")
    file.write(
        r"b'-----BEGIN PUBLIC KEY-----\n" + Transaction.receiverKey + r"\n-----END PUBLIC KEY-----'," + Transaction.amount + r",b'-----BEGIN PUBLIC KEY-----\n"
        + Transaction.publicKey + r"\n----END PUBLIC KEY-----'")
    file.close()
    return {"API add pending transaction processed."}




#shows the contents of TempMemPool
@app.get("/getTempMemePool")
def getTempMemePool():
    file = open("TempMempool.txt", "r")
    return file.read()

# @app.post("/getNewBlock/")
# def APIgetNewBlock():



uvicorn.run(app)


