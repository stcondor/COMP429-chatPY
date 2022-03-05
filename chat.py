import os
import sys
import socket
import threading
import time


class clientList:
    def __init__(self, socketID, addr):
        self.socketID = socketID
        self.addr = addr


def myPort():
    print("Your port number is: " + str(PORT) + "\n")

def myIP():
    return socket.gethostbyname(socket.gethostname())


options = "Options:\n\nhelp                                  Command manual\nmyip                                  Display the IP address\nmyport                                Display current port\nconnect <destination> <port no>       Establishes a new TCP connection\nlist                                  Display a list of all connections\nterminate <connection id.>            Terminate specified connection(connection id. from list command)\nsend <connection id.> <message>       Send a message to specified connection(connection id. from list command)\nexit                                  Terminates application\n";
error = "You need to provide a port number for the TCP connection\nPlease try:\n./chat <port number>\n"
error2 = "Please enter a valid id\nRefer to the connection by typing \"list\"\n"
clients = []

#Initialize server
HEADER = 64
SERVER = myIP()
if len(sys.argv) > 2:
    print(error)
    quit()

if sys.argv[1].isdigit():
    PORT = int(sys.argv[1]);
    myPort()
else:
    print(error)
    quit()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def printList():
    if len(clients) == 0:
        print("There are no clients\n")
        return

    print("\nid: IP address      Port No.")
    i = 1;
    for client in clients:
        print(str(i) + ": " + client.addr[0] + "     " + str(client.addr[1]))
        i += 1

def isInClient(id):
    if len(clients) == 0:
        return False
    elif id > 0 and id <= len(clients):
        return True
    return False


def handle_client(conn, addr):
    newConnection = clientList(conn, addr)
    clients.append(newConnection)
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # If a message does exist and is not NULL
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                sendMSG(clients.index(newConnection) + 1, DISCONNECT_MESSAGE)
            
            #conn.send("Message Received".encode(FORMAT))
            print(f"[{addr}] {msg}")
    
    clients.remove(newConnection)
    conn.close()

def createConnection(conn_ip, conn_port):
    conn_addr = (conn_ip, int(conn_port))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(conn_addr)
    thread = threading.Thread(target = handle_client, args = (client, conn_addr))
    thread.start()

def sendMSG(id, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # Makes sure the message is 64 bytes long
    send_length += b' ' * (HEADER - len(send_length))
    clients[id-1].socketID.send(send_length)
    clients[id-1].socketID.send(message)
    #print(clients[id-1].socketID.recv(2048).decode(FORMAT))

def terminate(id):
    sendMSG(id, DISCONNECT_MESSAGE)
    #clients[id-1].socketID.close()
    #del clients[id-1]

def terminateAll():
    for i in range(len(clients)):
        terminate(i+1)

def startServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    # See what IP address the server is running on
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS {threading.active_count() - 2}]")
        

if __name__ == "__main__":
    thread = threading.Thread(target = startServer, args = ())
    thread.start()
    print(options)
    while True:
        command = input("Please enter command:\n")
        param = command.split()
        if(param[0] == "exit"):
            print("terminating all clients...\n")
            terminateAll()
            break
        elif param[0] == "help":
            print(options)
        elif param[0] == "myport":
            myPort()
        elif param[0] == "connect":
            createConnection(param[1], param[2])
        elif param[0] == "list":
            printList()
        elif param[0] == "terminate":
            if len(param) > 2:
                print("You can only terminate one connection at a time\n")
            elif param[1].isdigit():
                if isInClient(int(param[1])):
                    terminate(int(param[1]))
                else:
                    print("Client id does not exist\n")
            else:
                print(error2)
        elif param[0] == "send":
            if param[1].isdigit():
                if isInClient(int(param[1])):
                    if len(param) > 3:
                        sendMSG(int(param[1]), " ".join(param[2:]))
                    else:
                        sendMSG(int(param[1]), param[2])
                    
                else:
                    print("Client id does not exist")
            else:
                print(error2)
        elif param[0] == "myip":
            print("\nCurrent IP: " + myIP())
        else:
            print("\nInvalid command\nType \"help\" for command manual\n")
    time.sleep(5)
    os._exit(0)


