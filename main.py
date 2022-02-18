from datetime import datetime, time
from random import randint

from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15

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

    blockchain.addTransaction("Sender", "Receiver", 10, privateKey, publicKey)

    blockchain.minePendingTransactions("Sender")

if __name__ == '__main__':
    # createTestBlockChain()
    testValidTransaction()