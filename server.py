import socket
import sys

#create a socket
def create_socket():
    try:
        #global variable so that we can access these variables in other functions
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
        s.listen(3) #listen for 3 connections at once (max)

    except socket.error as error_messsage:
        print("Error binding the port: " + str(error_messsage) + "\n" + "Retrying...")
        bind_socket() #call the function again to try binding again

#accept a connection with a server when socket is listening
def accept_connection():
    connection, address = s.accept()
    print("Connection has been established! | " + "IP " + address[0] + " | Port " + str(address[1]))
    #do something with the connection
    connection.close()
