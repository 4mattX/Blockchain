import ast
import base64
import binascii
import io
import pickle
import socket
import select
import errno
import sys
import threading
import time
import traceback


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

        # self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
        # self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)

        user = self.username.encode('utf-8')
        user_header = f"{len(user):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(user_header + user)

    def disconnect(self):
        # self.client_socket.detach()
        self.client_socket.close()

    def updateMaxKnownBlock(self, num):
        if (num > self.maxKnownBlock):
            self.maxKnownBlock = num

    def sendMessage(self, message):
        print("Sending Block")
        # message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)

    def sendPending(self, message):
        print("Sending Pending Transaction")
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)

    def startThread(self):
        clientThread = threading.Thread(target=self.receiveMessage, name="clientThread")
        clientThread.start()

    def receiveMessage(self):
        print("STARTED RECEIVING MESSAGES")
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
                            # transaction.setSignature(binascii.unhexlify(signature.strip()))


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

                        # print(receiverKey)
                        # print(self.blockchain.getChain()[-1].getMiner().decode('utf-8'))
                        #
                        # if str(receiverKey) == str(self.blockchain.getChain()[-1].getMiner().decode('utf-8')):
                        print("SENT MINER REWARD SUCCESS")
                        transaction = Transaction(receiverKey, amount, None)
                        transaction.receiverKey = RSA.import_key(transaction.receiverKey)

                        self.blockchain.pendingTransactions.append(transaction)
                        continue

                    if (username == "request"):
                        message = ""
                        # isMore = True
                        #
                        # while isMore:
                        #     try:
                        #         chunk = self.client_socket.recv(RECV_BUF_SIZE).decode('utf-8')
                        #         if not chunk:
                        #             isMore = False
                        #         message += chunk
                        #     except:
                        #         break
                        # message.strip()
                        message_header = self.client_socket.recv(HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())
                        message = self.client_socket.recv(message_length).decode('utf-8')

                        # blockNum = int(message.split(" ")[0])
                        blockNum = int(message)

                        print("Sending Block Num From Request #" + str(blockNum))

                        blockPickled = open (("blockchain/block_" + str(blockNum) + ".block"), "rb")
                        blockData = pickle.load(blockPickled)

                        self.disconnect()
                        self.setUsername(str(blockNum))
                        self.createConnection()
                        self.sendMessage(pickle.dumps(blockData))
                        continue

                    try:
                        # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                        message_header = self.client_socket.recv(HEADER_LENGTH)
                        message_length = int(message_header.decode('utf-8').strip())
                        # message = self.client_socket.recv(message_length).decode('utf-8')
                        # message = self.client_socket.recv(message_length)

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
                    except:
                        print("Failed Reading, Sending Request for Block #" +  (str(len(self.blockchain.chain))))
                        self.disconnect()
                        self.setUsername("request")
                        self.createConnection()
                        self.sendMessage(str(len(self.blockchain.chain)).encode())
                        continue

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

                    # print("Block Loaded Success -> " + str(block.index))

                    # Occurs when the receiver has most up to date blockchain

                    self.updateMaxKnownBlock(int(username))
                    self.clientBlock = len(self.blockchain.chain)
                    # print("max: " + str(self.maxKnownBlock))
                    # print("client: " + str(self.clientBlock))

                    if (int(username) == self.clientBlock):
                        # block.recordBlockNoSend()
                        self.blockchain.addBlock(block)
                        self.blockchain.pendingTransactions.clear()
                        print("added block up-to-date receiver Block #" + str(username))

                        if (self.clientBlock < self.maxKnownBlock):
                            print("Sending Request for Block #" +  (str(self.clientBlock + 1)))
                            self.disconnect()
                            self.setUsername("request")
                            self.createConnection()
                            self.sendMessage((str(self.clientBlock + 1)).encode())
                        continue


            except Exception as e:
                # if (e.__class__.__name__ == "BlockingIOError" or
                #     e.__class__.__name__ == "TypeError" or
                #     e.__class__.__name__ == "IndexError" or
                #     e.__class__.__name__ == "UnicodeDecodeError"):
                #     continue
                # # if (e.__class__.__name__ != "UnpicklingError"):
                # #     continue
                #
                # print(e.__class__.__name__)
                # print("Failed Reading, Sending Request for Block #" +  (str(len(self.blockchain.chain))))
                # self.disconnect()
                # self.setUsername("request")
                # self.createConnection()
                # self.sendMessage(str(len(self.blockchain.chain)).encode())
                # continue

                # if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                # if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
                #     print('Reading error: {}'.format(str(e)))


                # if (self.clientBlock < self.maxKnownBlock):
                #     self.disconnect()
                #     self.setUsername("request")
                #     self.createConnection()
                #     self.sendMessage((str(self.clientBlock + 1)).encode())
                continue


