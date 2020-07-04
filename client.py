import socket
from threading import Thread
name=input('Please tell us your name: ')
host='127.0.0.1'
port=12345
# everything above is same as server.py
# setup client socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# we need to connect client with the server at the specified port and host
client.connect((host,port))

def manager():
    while True:
        # we will try to connect client with server in case of error print an error message
        try:
            message=client.recv(1024).decode('ascii')
            # if message asks name
            if message=='NAME':
                client.send(name.encode('ascii'))
            # if it is sending other client's message
            else:
                print(message)
        except:
            # raise error
            print('An error occurred!')
            client.close()
            break
# text function to send own message
def text():
    while True:
        txt=input()
        message=f'{name} : {txt}'.encode('ascii')
        client.send(message)
# we will need two threads one to handle manage function for each client and other to handle text function for each client 
managing_thread=Thread(target=manager)
managing_thread.start()
text_thread=Thread(target=text)
text_thread.start()
