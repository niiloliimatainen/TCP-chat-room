#########################################
# Niilo Liimatainen
# 12.02.2021
# Sources:
# https://www.neuralnine.com/tcp-chat-in-python/
#
#########################################
import socket
import threading
import sys

# host address and port number (local)
hostname = "127.0.0.1"
port = 1234

nickname = input("Choose your nickname: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname, port))

# Function to receive messages from the server
def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf-8")
            if msg == "NICK":
                s.send(nickname.encode("utf-8"))

            else:
                print(msg)
        except:
            print("You have left the chat!")
            s.close()
            sys.exit()
            break


# Function to send client's messages
def send():
    while True:
        msg = input("")
        if msg == "/exit":
            s.send(msg.encode("utf-8"))
            s.close()
            sys.exit()

        elif msg == "/room1":
            s.send(msg.encode("utf-8"))

        elif msg == "/room2":
            s.send(msg.encode("utf-8"))

        elif msg == "/default":
            s.send(msg.encode("utf-8"))

        elif msg[:4] == "/pm-":
            split = msg.split(":", 1)
            msg = split[0] + ":(private)" + nickname + ":" + split[1]
            s.send(msg.encode("utf-8"))

        else:
            msg = nickname + ": " + msg
            s.send(msg.encode("utf-8"))

# Threads for listening new messages and sending new messages
rcv_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

rcv_thread.start()
send_thread.start()
