from datetime import datetime

from Block import Block
from Transaction import Transaction

if __name__ == '__main__':
    transactions = []

    transactions.append(Transaction("Matthew0", "Thuan0", 420))
    transactions.append(Transaction("Matthew1", "Thuan1", 69))
    transactions.append(Transaction("Matthew2", "Thuan2", 1738))
    transactions.append(Transaction("Matthew3", "Thuan3", 8008))
    transactions.append(Transaction("Matthew4", "Thuan4", 25))

    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    block = Block(transactions,time, 0 )

    for transaction in transactions:
        print(transaction.getHash())