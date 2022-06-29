import socket
import sys



#create a socket
def create_socket():
    try:
        global host
        global port
        global s
        host=''
        port=9999
        s = socket.socket()

    except socket.error as error_messsage:
        print("Error creating socket: " + str(error_messsage))
        sys.exit()

#bind the socket to the port and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port: " + str(port))
        s.bind((host,port))
        s.listen(3)

    except socket.error as error_messsage:
        print("Error binding the port: " + str(error_messsage) + "\n" + "Retrying...")
        bind_socket()
