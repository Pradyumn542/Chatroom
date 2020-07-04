# import modules to be used
import socket
from threading import Thread

# setup server socket
# socket takes in 2 parameters first being family of socket
# second parameter determines type ( in this case stream server using TCP protocol)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# we are using a local host
host='127.0.0.1'
# now declare a port that is not already occupied like port 80
port=12345
# now we will bind server with provided host and port
server.bind((host,port))
# we must set server to listen to incoming client request
server.listen()
# two empty lists to save all client sockets and names of clients
client_sockets=[]
client_names=[]
# now here comes our first function to distribute message to every client
def distribute(message):
    for client in client_sockets:
        client.send(message)
# now the function to manage the messages came to server
def manager(client):
    while True:
        try:
            message=client.recv(1024)
            distribute(message)
            # if the try block fails and client is not connected anymore we need to remove it from the list
        except:
            clnt_indx=client_sockets.index(client)
            name=client_names[clnt_indx]
            broadcast(f'{name} has left the chat.'.encode('ascii'))
            # remove client from both lists
            client_names.remove(client)
            client_sockets.remove(client)
            break
# in case we have a new client waiting to connect
def new_client():
    while True:
        # save client socket and address
        client,address=server.accept()
        print(f'{address} is now connected')
        # now we must ask client his name
        client.send('NAME'.encode('ascii'))
        name=client.recv(1024).decode('ascii')
        client_names.append(name)
        client_sockets.append(client)

        distribute(f'{name} has joined the chat.'.encode('ascii'))
        client.send('You are now connected !'.encode('ascii'))
        # the thread for managing the client needs to be triggered
        thread=Thread(target=manager,args=(client,))
        thread.start()

# call the function
new_client()
