import socket
import select

if __name__ == '__main__':

    HEADER_LENGTH = 10
    IP = ""
    PORT = 1024
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((IP, PORT))

    serverSocket.listen()
    socketList = [serverSocket]
    clients = {}

    print(f'Waiting for connections on {IP}:{PORT}...')
    def receiveMessage(clientSocket):

        try:

            mesheader = clientSocket.recv(HEADER_LENGTH)
            if not len(mesheader):
                return False
            mesLength = int(mesheader.decode('utf-8').strip())

            return {'header': mesheader, 'data': clientSocket.recv(mesLength)}

        except:
            return False

    while True:
        read_sockets, _, exception_sockets = select.select(socketList, [], socketList)

        for notified_socket in read_sockets:

            if notified_socket == serverSocket:

                clientSocket, clientAddress = serverSocket.accept()
                user = receiveMessage(clientSocket)

                if user is False:
                    continue

                socketList.append(clientSocket)
                clients[clientSocket] = user

            else:
                message = receiveMessage(notified_socket)

                if message is False:
                    socketList.remove(notified_socket)
                    del clients[notified_socket]

                    continue
                user = clients[notified_socket]

                print(f'Message from {user["data"].decode("utf-8")}: {message["data"]}')

                for clientSocket in clients:

                    if clientSocket != notified_socket:
                        clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])

        for notified_socket in exception_sockets:
            socketList.remove(notified_socket)
            del clients[notified_socket]