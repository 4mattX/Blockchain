from datetime import datetime, time
from random import randint

from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction

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

    key = blockchain.generateKeys()
    key = blockchain.generateKeys()
    print(key)

    blockchain.addTransaction("Sender", "Receiver", 10, key, key)

    blockchain.minePendingTransactions("Sender")

if __name__ == '__main__':
    # createTestBlockChain()
    testValidTransaction()