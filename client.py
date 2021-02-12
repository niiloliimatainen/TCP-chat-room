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

nickname = input("Choose your nickname: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname, port))


def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf-8")
            if msg == "nickname":
                s.send(nickname.encode("utf-8"))
            else:
                print(msg)
        except:
            print("Error in connection!")
            s.close()
            break


def send():
    while True:
        msg = f"{nickname} {input('')}"
        s.send(msg.encode("utf-8"))


# Threads for listening new messages and sending new messages
rcv_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

rcv_thread.start()
send_thread.start()
