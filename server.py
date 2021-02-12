#########################################
# Niilo Liimatainen
# 12.02.2021
# Sources:
# https://www.neuralnine.com/tcp-chat-in-python/
#
#########################################
import socket
import threading

# host address and port number (local)
hostname = "127.0.0.1"
port = 1234

clients = []
nicknames = []

# socket to listen the chosen port from host address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen()


# broadcast messages to every client
def broadcast(msg):
    for c in clients:
        c.send(msg)


# Function to listen to client's messages. If there is an error in connection, the client is removed from the server.
def client_handler(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = clients.index(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            clients.remove(client)
            client.close()
            print(f"{address} {nickname} has left the server!")
            broadcast(f"{nickname} has left the chat!".encode("utf-8"))
            break


# Function to receive connections from new clients
def receive():
    print("Server is running!")

    while True:
        s_client, address = s.accept()

        s_client.send("nickname".encode("utf-8"))
        nickname = s_client.recv(1024).decode("utf-8")
        clients.append(s_client)
        nicknames.append(nickname)

        print(f"{address} connected to the server with nickname: {nickname}")
        s_client.send("You are connected to the server!".encode("utf-8"))
        broadcast(f"{nickname} joined the chat!".encode("utf-8"))

        thread = threading.Thread(target=client_handler, args=(s_client,))
        thread.start()


receive()
