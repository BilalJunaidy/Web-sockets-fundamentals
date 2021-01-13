import socket 
import threading

# This represents 64 bytes.
# This header represents the first message that our server is going to recrive from the client upon each 
# interaction sent from the client to the server. This header message will be 64 bytes long and will be followed by the actual 
# message that has been sent from the client to the server. 
# The reason for this is because we want to know what the size of our "actual" message from the client is and the 64 bytes header will give us that information,
# allowing us to determine the size of the "actual" message. 
# This size is an argument to the conn.recv() method that we are using below and hence we need the size of the "actual" message. 
HEADER = 64


PORT = 5050
# The following represents my local IP address, not my modems public IP address. 
# The reason for using this is because I am trying to run a server from my local machine.
SERVER = "192.168.0.105"

# An alternative approach here would be to actually let python dynamically determine your IPc4 address 
# of the machine that is being used to run the server.
# We can do this using the following methods of the socket library
SERVER = socket.gethostbyname(socket.gethostname())

# Over here we are simply creating a tuple which we will be used below when we are binding the socket object to the server and the port we are using.
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"

# The following lone of code is simply helping us create a socket object.
# The first argument here is the family type of sockets we want to use. We have gone ahead and used the family that works 
# over the internet. 
# The second argument here is also the standard argument to be passed here which represent the type of socket to use. 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This is us binding the server and port to the socket object. 
# Therefore, anything that connects to this server and port will connect to this socket.
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.") 
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # The following is us simply us cleaning closing our sockets connection to the server. 
            if msg == DISCONNECT_MESSAGE:
                connected = False 
            
            print(f"{addr} {msg}")

    conn.close()



# This function will be used to help the server listen in for connections from clients and then 
# once a connection has been found, it will call the handle_client function above to handle that client.
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # conn here represents a socket object.
        # addr represents the ip address as well as the port of the client that has just connected to the server.
        conn, addr = server.accept()
        
        # Basically what we are doing below is that whenever we have a new connection that has been able to successfully connect to our server,
        # we will create a new thread. 
        # This thread will be executing an "instance" of the client_handle function for each newly established connection.  
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(F"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting")
start()

