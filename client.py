import socket
import sys
import threading

name = input("Whats your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 15522))

def receiveFromServer():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NAME':
                client.send(name.encode('ascii'))
            elif(message != 'TEST'):
                print(message)
        except:
            print("An error has occured")
            client.close()
            break

def writeToServer():
    while True:
        message = '{}: {}'.format(name, input(''))
        client.send(message.encode('ascii'))

receive_from_server_thread = threading.Thread(target=receiveFromServer)
receive_from_server_thread.start()

write_to_server_thread = threading.Thread(target=writeToServer)
write_to_server_thread.start()