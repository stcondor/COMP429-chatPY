import socket

options = "\nOptions:\n\nhelp                                  Command manual\nmyip                                  Display the IP address\nmyport                                Display current port\nconnect <destination> <port no>       Establishes a new TCP connection\nlist                                  Display a list of all connections\nterminate <connection id.>            Terminate specified connection(connection id. from list command)\nsend <connection id.> <message>       Send a message to specified connection(connection id. from list command)\nexit                                  Terminates application\n";
error = "\nYou need to provide a valid port number for the TCP connection\nPlease try:\npython chat.py <port number>\n"
error2 = "\nPlease enter a valid id\nRefer to the connection by typing \"list\"\n"
error3 = "\nInvalid command\nType \"help\" for command manual\n"
HEADER = 64
PORT = None
SERVER = None
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class clientList:
    def __init__(self, socketID, addr):
        self.socketID = socketID
        self.addr = addr

def myPort():
    print("Your port number is: " + str(PORT) + "\n")

def initPort(argv):
    global PORT
    if len(argv) == 2 and argv[1].isdigit():
        PORT = int(argv[1])
        return
    print(error)
    quit()

def myIP():
    return socket.gethostbyname(socket.gethostname())

def initADDR(argv):
    global SERVER
    SERVER = myIP()
    initPort(argv)
    return (SERVER, PORT)
