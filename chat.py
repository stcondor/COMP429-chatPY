#Names: Steven Condor | Devin Delgado
#Date: 2022.03.19
#Application: chat
#Purpose: To create TCP connections using sockets in which users can send messages to one another

import os
import sys
import socket
import threading
import time
from Util import *

clients = []

def printList():
    if len(clients) == 0:
        print("There are no clients\n")
        return

    print("\nid: IP address      Port No.")
    i = 1;
    for client in clients:
        print(str(i) + ": " + client.addr[0] + "     " + str(client.addr[1]))
        i += 1

def isInClients(id):
    if id > 0 and id <= len(clients):
        return True
    return False


def handle_client(conn, addr):
    newConnection = clientList(conn, addr)
    clients.append(newConnection)
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
        except socket.error:
            print("\nFailed to receive message from client\n")
            continue
        # If a message does exist and is not NULL
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                terminate(clients.index(newConnection) + 1)
                print("\nTerminating connection to IP: {} , PORT: {}\n".format(addr[0],addr[1]))
                continue
            
            #conn.send("Message Received".encode(FORMAT))
            print("\nMessage received from {}\nSender's Port: {}\nMessage: {}\n".format(addr[0], addr[1], msg))
            #print(f"[{addr}] {msg}")
    
    clients.remove(newConnection)
    conn.close()

def isDuplicate(conn_ip, conn_port):
    if conn_ip == ADDR[0] and conn_port == ADDR[1]:
        return True
    for client in clients:
        if conn_ip == client.addr[0] and conn_port == client.addr[1]:
            return True
    return False

def createConnection(conn_ip, conn_port):
    if isDuplicate(conn_ip, int(conn_port)):
        print("\nEntered connection is not valid\n")
        return
    conn_addr = (conn_ip, int(conn_port))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(conn_addr)
    except socket.error:
        print("\nCould not stablish connection to specified server\n")
        return
    thread = threading.Thread(target = handle_client, args = (client, conn_addr))
    thread.start()

def sendMSG(id, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # Makes sure the message is 64 bytes long
    send_length += b' ' * (HEADER - len(send_length))
    try:
        clients[id-1].socketID.send(send_length)
        clients[id-1].socketID.send(message)
        if msg == DISCONNECT_MESSAGE:
            pass
        else:
            print("\nMessage sent to {}\n".format(clients[id-1].addr[0]))
        #print(clients[id-1].socketID.recv(2048).decode(FORMAT))
    except socket.error:
        print("\nFailed to send message\n")

def terminate(id):
    sendMSG(id, DISCONNECT_MESSAGE)

def terminateAll():
    for i in range(len(clients)):
        terminate(i+1)

def startServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(ADDR)
        server.listen()
    except socket.error:
        print(error)
        os._exit(1)
        
    print(f"\n[LISTENING] Server is listening on IP: {ADDR[0]}, PORT: {ADDR[1]}")

    while True:
        try:
            conn, addr = server.accept()
        except socket.error:
            print("\nFailed to connect to connect a client\n")
            continue
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS {threading.active_count() - 2}]")

        



if __name__ == "__main__":
    ADDR = initADDR(sys.argv)
    thread = threading.Thread(target = startServer, args = ())
    thread.start()
    print(options)
    while True:
        command = input("Please enter command:\n")
        param = command.split()
        #implement a len(param) == 1 for all single param commands
        if len(param) == 0:
            print(error3)
        elif param[0] == "exit":
            if len(param) > 1:
                print(error3)
                continue
            print("terminating all clients...\n")
            terminateAll()
            break
        elif param[0] == "help":
            if len(param) > 1:
                print(error3)
                continue
            print(options)
        elif param[0] == "myport":
            if len(param) > 1:
                print(error3)
                continue
            myPort()
        elif param[0] == "connect":
            if len(param) == 3:
                createConnection(param[1], param[2])
                continue
            print(error3)
        elif param[0] == "list":
            if len(param) > 1:
                print(error3)
                continue
            printList()
        elif param[0] == "terminate":
            if len(param) == 1 or len(param) > 2:
                print(error3)
            elif param[1].isdigit():
                if isInClients(int(param[1])):
                    terminate(int(param[1]))
                else:
                    print("Client id does not exist\n")
            else:
                print(error2)
        elif param[0] == "send":
            if len(param) <= 2:
                print(error3)
            elif param[1].isdigit():
                if isInClients(int(param[1])):
                    sendMSG(int(param[1]), " ".join(param[2:]))
                else:
                    print("Client id does not exist")
            else:
                print(error2)
        elif param[0] == "myip":
            if len(param) > 1:
                print(error3)
                continue
            print("\nCurrent IP: " + myIP())
        else:
            print(error3)
    time.sleep(3)
    os._exit(0)


