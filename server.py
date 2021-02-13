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


def private_message(s_client, client_recv):
    s_client.send("PRIV-MSG".encode("utf-8"))
    msg = s_client.recv(1024)
    client_recv.send(msg)


# Function to kick client from the server
def kick(s_client):
    index = clients.index(s_client)
    nickname = nicknames[index]
    nicknames.remove(nickname)
    clients.remove(s_client)
    s_client.close()
    print(f"{nickname} has left the server!")
    broadcast(f"{nickname} has left the chat!".encode("utf-8"))


# Function to listen to client's messages. If there is an error in connection, the client is removed from the server.
def client_handler(s_client):
    while True:
        try:
            msg = s_client.recv(1024).decode("utf-8")
            print(msg)
            if msg == "/exit":
                kick(s_client)
                break
            elif msg == "/private":
                s_client.send("PRIV".encode("utf-8"))
                nickname = s_client.recv(1024).decode("utf-8")
                index = nicknames.index(nickname)
                client_recv = clients[index]
                private_message(s_client, client_recv)
            else:
                broadcast(msg.encode("utf-8"))
        except:
            kick(s_client)
            break


# Function to receive connections from new clients
def receive():
    print("Server is running!")

    while True:
        s_client, address = s.accept()

        s_client.send("NICK".encode("utf-8"))
        nickname = s_client.recv(1024).decode("utf-8")
        clients.append(s_client)
        nicknames.append(nickname)

        print(f"{address} connected to the server with nickname: {nickname}")
        s_client.send("You are connected to the server!".encode("utf-8"))
        s_client.send("Here are commands that you can use:\n".encode("utf-8"))
        s_client.send(
            "/exit = leave server, /room1 = go to room 1, /room2 = go to room 2, /private = private message to user\n".encode("utf-8"))
        broadcast(f"{nickname} joined the chat!".encode("utf-8"))

        thread = threading.Thread(target=client_handler, args=(s_client,))
        thread.start()


receive()
