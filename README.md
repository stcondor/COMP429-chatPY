# COMP429-chatPY
Contributors:
 - Devin Delgado: He wrote the TCP connection code between the server and the client, which
   allows for the binding between them. This includes handling the individual connection between the client and the server, and new connections and where they need to go. He also tested the program for any bugs that might have occurred.
 - Steven Condor: He implemented multithreading support, which allows the same application to
   behave as client and server. This includes handling multiple clients at the same time. He also developed the user interface which allows users to run commands such as help, myip, myport, connect, list, send, terminate, and exit. He also worked alongside Devin in the debugging process.

Running the chat application:
 - Prerequisites: Having the latest version of python installed
 - Run the following command: 
 `python chat.py <port #>`
 - where `<port #>` is the listening port for the server