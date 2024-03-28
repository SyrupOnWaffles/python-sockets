import socket
import threading
import time

host = 'localhost'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if "PING" in message.decode("ascii"):
                client.send(message)
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            print(f'{nickname} disconnected')
            break
def server_console():
    while True:
        command = input("")
        if(command.lower() == "quit"):
            broadcast("closing server".encode('ascii'))
            break
def recieve():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'nickname of client is {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()


if __name__ == '__main__':
    print('server started')
    console_thread = threading.Thread(target=server_console)
    console_thread.start()
    recieve()