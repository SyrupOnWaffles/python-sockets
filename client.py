import socket
import threading
import time
import os

nickname = input('enter nickname ')

host = 'localhost'
port = 5555
shutdown = False
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect((host,port))

cur_time = 0

def recieve():
    while True:
        global cur_time
        try:
            message = client.recv(1024).decode('ascii')
            if(message == 'NICK'):
                client.send(nickname.encode('ascii'))
            elif("PING" in message):
                ping = round(time.time() * 1000) - int((message.split()[1]))
                print(f'ping : {str(ping)}')
                cur_time = 0
            else:
                pass
        except:
            print('an error occured')
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {"yep"}'
        client.send(message.encode('ascii'))
def ping():
    global cur_time
    while True:
        time.sleep(1)
        if(cur_time == 0):
            cur_time = round(time.time() * 1000)
            client.send(f'PING {cur_time}'.encode('ascii'))



recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

#write_thread = threading.Thread(target=write)
#write_thread.start()

ping_thread = threading.Thread(target=ping)
ping_thread.start()