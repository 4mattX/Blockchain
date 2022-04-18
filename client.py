import ast
import io
import pickle
import socket
import select
import errno
import sys
import threading
import traceback

from Cryptodome.PublicKey import RSA

from BlockChainProject.Block import Block

HEADER_LENGTH = 10
IP = "10.10.10.17"
PORT = 1263

class Client(object):
    def __init__(self, username, blockchain):
        self.username = username
        self.user_header = ''
        self.client_socket = None
        self.blockchain = blockchain

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
        # self.client_socket.detach()
        self.client_socket.close()

    def sendMessage(self, message):
        print("Sending Message")
        # message = message.encode('utf-8')
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

                    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    message_header = self.client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    # message = self.client_socket.recv(message_length).decode('utf-8')
                    message = self.client_socket.recv(message_length)

                    # Print message
                    # print("username -> " + username)
                    # print("message length -> " + str(message_length))
                    # print(message)
                    newBlock = pickle.loads(message)

                    if (newBlock == None):
                        continue

                    # if (len(self.blockchain.chain) >= int(username)):
                    #     return
                    #
                    # if (len(self.blockchain.chain) < int(username)):
                    #     return

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
                    self.blockchain.addBlock(block)


            except IOError as e:
                # if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                #     print('Reading error: {}'.format(str(e)))
                continue


