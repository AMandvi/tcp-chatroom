import errno
import threading
import socket
import time


HOST = "127.0.0.1"
PORT = 15522

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

server.bind((HOST, PORT))
server.listen()

clients = []
names = []

def check_client_connection():
    while True:
        to_remove = []
        for client in clients:
            try:
                client.send(bytes('TEST', 'UTF-8'))
            except socket.error as e:
                if e.errno == errno.ECONNRESET:
                    to_remove.append(client)
        
        for remove in to_remove:
            index = clients.index(remove)
            clients.remove(remove)
            name = names[index]
            broadcast_msg('{} left the chat'.format(name).encode('ascii'))
            names.remove(name)
        time.sleep(1)



def broadcast_msg(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:

            message = client.recv(1024)
            broadcast_msg(message)
        except:

            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast_msg('{}left the chat'.format(name).encode('ascii'))
            names.remove(name)
            break


def receive_msg():
    while True:
        client, address = server.accept()
        print("Connection started with {}".format(str(address)))

        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

         # Print And Broadcast Nickname
        print("Name is {}".format(name))
        broadcast_msg("{} joined!".format(name).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

check_client_connection_thread = threading.Thread(target=check_client_connection)
check_client_connection_thread.start()
receive_msg()
