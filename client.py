#########################################
# Niilo Liimatainen
# 12.02.2021
# Sources:
# https://www.neuralnine.com/tcp-chat-in-python/
#
#########################################
import socket
import threading
import time

# host address and port number (local)
hostname = "127.0.0.1"
port = 1234

nickname = input("Choose your nickname: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname, port))


def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf-8")
            if msg == "NICK":
                s.send(nickname.encode("utf-8"))
            elif msg == "PRIV":
                s.send(input("Give nickname for private message: ").encode("utf-8"))
                msg = input("Write private message: ")
            elif msg == "PRIV-MSG":
                time = get_time()
                s.send(time + " " + nickname + msg.encode("utf-8"))
            else:
                print(msg)
        except:
            print("You have left the chat!")
            s.close()
            break


def send():
    while True:
        msg = input("")
        if msg == "/exit":
            s.send(msg.encode("utf-8"))
        elif msg == "/private":
            s.send(msg.encode("utf-8"))
        else:
            time = get_time()
            msg = time + " " + nickname + ": " + msg
            s.send(msg.encode("utf-8"))


def get_time():
    t = time.localtime()
    current = time.strftime("%H:%M:%S", t)
    return current


# Threads for listening new messages and sending new messages
rcv_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

rcv_thread.start()
send_thread.start()
