#########################################
# Niilo Liimatainen
# 12.02.2021
# Sources:
# https://www.neuralnine.com/tcp-chat-in-python/
#
#########################################
import socket
import threading

# define client class
class Client:
    def __init__(self, socket, nickname):
        self.s = socket
        self.nickname = nickname
        self.room = 0


# host address and port number (local)
hostname = "127.0.0.1"
port = 1234

# all clients in the server
clients = []

# room spesific clients
clients_default = []
clients_room1 = []
clients_room2 = []

# socket to listen the chosen port from host address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen()


# send private message
def private_message(msg, nickname):
    for index, client in enumerate(clients):
        if (client.nickname == nickname):
            break
        else:
            index = -1
    if index != -1:
        clients[index].s.send(msg.encode("utf-8"))
        return 1
    return 0


# broadcast messages to different rooms
def broadcast(msg, room):
    if room == 0:
        for c in clients_default:
            c.s.send(msg)
    elif room == 1:
        for c in clients_room1:
            c.s.send(msg)
    elif room == 2:
        for c in clients_room2:
            c.s.send(msg)


# Function to kick client from the server
def kick(client):
    room = client.room
    nickname = client.nickname
    remove_from_room(client)
    clients.remove(client)
    client.s.close()
    print(f"{nickname} has left the server!")
    broadcast(f"{nickname} has left the chat!".encode("utf-8"), room)


# Function to remove client from room's list
def remove_from_room(client):
    if client.room == 0:
        clients_default.remove(client)

    elif client.room == 1:
        clients_room1.remove(client)

    elif client.room == 2:
        clients_room2.remove(client)


# Function to listen to client's messages. If there is an error in connection, the client is removed from the server.
def client_handler(client):
    while True:
        try:
            msg = client.s.recv(1024).decode("utf-8")
            if msg == "/exit":
                kick(client)
                break

            elif msg[:4] == "/pm-":
                split = msg.split(":", 1)
                nickname = split[0][4:]
                msg = split[1]
                if not private_message(msg, nickname):
                    client.s.send("Invalid username!".encode("utf-8"))

            elif msg == "/room1":
                remove_from_room(client)
                clients_room1.append(client)
                client.room = 1
                client.s.send("You joined room1!".encode("utf-8"))
                broadcast(
                    f"{client.nickname} joined the room!".encode("utf-8"), client.room)

            elif msg == "/room2":
                remove_from_room(client)
                clients_room2.append(client)
                client.room = 2
                client.s.send("You joined room2!".encode("utf-8"))
                broadcast(
                    f"{client.nickname} joined the room!".encode("utf-8"), client.room)

            elif msg == "/default":
                remove_from_room(client)
                clients_default.append(client)
                client.room = 0
                client.s.send("You joined the default room!".encode("utf-8"))
                broadcast(
                    f"{client.nickname} joined the chat!".encode("utf-8"), client.room)
            else:
                broadcast(msg.encode("utf-8"), client.room)
        except:
            kick(client)
            break


# Function to receive connections from new clients
def receive_client():
    print("Server is running!")

    while True:
        s_client, address = s.accept()

        s_client.send("NICK".encode("utf-8"))
        nickname = s_client.recv(1024).decode("utf-8")
        client = Client(s_client, nickname)
        clients.append(client)
        clients_default.append(client)

        print(f"{address} connected to the server with nickname: {nickname}")
        print(f"Active connections: {len(clients)}")
        s_client.send("You are connected to the server!".encode("utf-8"))
        s_client.send("Here are commands that you can use:\n".encode("utf-8"))
        s_client.send(
            "/exit = leave server, /default = go to default room, /room1 = go to room 1, /room2 = go to room 2, /pm-'nickname': = private message to user\n".encode("utf-8"))
        broadcast(f"{nickname} joined the chat!".encode("utf-8"), client.room)

        thread = threading.Thread(target=client_handler, args=(client,))
        thread.start()


receive_client()
