import binascii
import pickle
import socket
import threading

from Cryptodome.PublicKey import RSA

from BlockChainProject.Block import Block
from BlockChainProject.Transaction import Transaction

HEADER_LENGTH = 10
IP = "173.255.193.198"
PORT = 1024

SEND_BUF_SIZE = 256
RECV_BUF_SIZE = 256

class Client(object):
    def __init__(self, username, blockchain):
        self.username = username
        self.user_header = ''
        self.client_socket = None
        self.blockchain = blockchain
        self.maxKnownBlock = 0
        self.clientBlock = 0

    def setUsername(self, username):
        self.username = username

    def createConnection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        self.client_socket.setblocking(False)

        user = self.username.encode('utf-8')
        user_header = f"{len(user):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(user_header + user)

    def disconnect(self):
        self.client_socket.close()

    def updateMaxKnownBlock(self, num):
        if (num > self.maxKnownBlock):
            self.maxKnownBlock = num

    def sendMessage(self, message):
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)

    def sendPending(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)

    def startThread(self):
        clientThread = threading.Thread(target=self.receiveMessage, name="clientThread")
        clientThread.start()

    def receiveMessage(self):
        while True:
            try:
                while True:

                    user_header = self.client_socket.recv(HEADER_LENGTH)

                    username_length = int(user_header.decode('utf-8').strip())

                    # Receive and decode username
                    username = self.client_socket.recv(username_length).decode('utf-8')

                    # Check if message is pending transaction
                    if (username == "mempool"):
                        message_header = self.client_socket.recv(HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())
                        # message = self.client_socket.recv(message_length).decode('utf-8')
                        message = ""
                        isMore = True

                        while isMore:
                            try:
                                chunk = self.client_socket.recv(RECV_BUF_SIZE).decode('utf-8')
                                if not chunk:
                                    isMore = False
                                message += chunk
                            except:
                                break
                        message.strip()

                        receiverKey = message.split(",")[0]
                        amount = message.split(",")[1]
                        senderKey = message.split(",")[2]
                        signature = message.split(",")[3]

                        transaction = Transaction(receiverKey, amount, senderKey)

                        transaction.publicKey = RSA.import_key(transaction.publicKey)
                        transaction.receiverKey = RSA.import_key(transaction.receiverKey)

                        try:
                            transaction.setSignature(binascii.unhexlify(signature.strip()))
                        except binascii.Error:
                            print("BYTE DATA CORRUPTED")

                        if (transaction.isValidTransaction()):
                            self.blockchain.pendingTransactions.append(transaction)

                        continue

                    if (username == "minerReward"):
                        message_header = self.client_socket.recv(HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())

                        message = ""
                        isMore = True

                        while isMore:
                            try:
                                chunk = self.client_socket.recv(RECV_BUF_SIZE).decode('utf-8')
                                if not chunk:
                                    isMore = False
                                message += chunk
                            except:
                                break
                        message.strip()

                        receiverKey = message.split(",")[0]
                        amount = message.split(",")[1]

                        transaction = Transaction(receiverKey, amount, None)
                        transaction.receiverKey = RSA.import_key(transaction.receiverKey)

                        self.blockchain.pendingTransactions.append(transaction)
                        continue

                    if (username == "request"):
                        message_header = self.client_socket.recv(HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())
                        message = self.client_socket.recv(message_length).decode('utf-8')

                        # blockNum = int(message.split(" ")[0])
                        blockNum = int(message)

                        if (blockNum > len(self.blockchain.getChain())):
                            continue

                        blockPickled = open (("blockchain/block_" + str(blockNum) + ".block"), "rb")
                        blockData = pickle.load(blockPickled)

                        self.disconnect()
                        self.setUsername(str(blockNum))
                        self.createConnection()
                        self.sendMessage(pickle.dumps(blockData))
                        continue

                    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    message_header = self.client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())

                    message = b''
                    isMore = True

                    while isMore:
                        try:
                            chunk = self.client_socket.recv(RECV_BUF_SIZE)
                            if not chunk:
                                isMore = False
                            message += chunk
                        except:
                            break

                    newBlock = pickle.loads(bytes(message))

                    transactions = newBlock[0]
                    for transaction in transactions:
                        try:
                            transaction.publicKey = RSA.import_key(transaction.publicKey)
                            transaction.receiverKey = RSA.import_key(transaction.receiverKey)
                        except:
                            transaction.publicKey = None
                            transaction.receiverKey = RSA.import_key(transaction.receiverKey)

                    block = Block(newBlock[0], newBlock[1], newBlock[2], self)
                    block.prev = newBlock[3]
                    block.nonse = newBlock[4]
                    block.hash = newBlock[5]

                    # Occurs when the receiver has most up to date blockchain
                    self.clientBlock = len(self.blockchain.chain)

                    if (int(username) == self.clientBlock):
                        block.recordBlockNoSend()
                        self.blockchain.addBlock(block)
                        self.blockchain.pendingTransactions.clear()
                        continue

            except Exception as e:
                continue