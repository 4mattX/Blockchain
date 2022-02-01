from datetime import datetime, time

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
    block = Block(transactions, time(), 0)
    blockChain.addBlock(block)
    block = Block(transactions, time(), 1)
    blockChain.addBlock(block)
    block = Block(transactions, time(), 2)
    blockChain.addBlock(block)
    block = Block(transactions, time(), 3)
    blockChain.addBlock(block)

    for block in blockChain.getChain():
        print("-----------------------------")
        print("Hash -> " + block.getHash())
        print("Prev -> " + block.getPrev())
        print("Transactions -> " + str(block.getTransactions()))
        print("-----------------------------")

if __name__ == '__main__':
    createTestBlockChain()