import socket
import os
import sys
import time


sock = socket.socket()
host = ''
port = 9999

sock.connect((host, port))

def main():
    pass

def choose_option():
    pass

#send command to server
def send_command():
    while(True):
        command = input("Enter command: ")
        if command == 'back':
            choose_option()
        else:
            if len(str.encode(command))>0:
                #send the command
                sock.send(str.encode(command))
                #receive the response
                server_response = str(sock.recv(1024), 'utf-8')

                print(server_response, end="")

#send file to server
def send_file():
    # Getting file details.
    file_name = input("File Name:")
    file_size = os.path.getsize(file_name)

  
    # Opening file and sending data.
    with open(file_name, "rb") as file:
        c = 0
        # Starting the time capture.
        start_time = time.time()

        # Running loop while c != file_size.
        while c <= file_size:
            data = file.read(1024)
            if not (data):
                break
            sock.sendall(data)
            c += len(data)

        # Ending the time capture.
        end_time = time.time()

    print("File Transfer Complete . Total time to transfer: ", end_time - start_time)



#receive file from server
def receive_file():
    # Getting file details.
    file_name = input("File Name:")
    file_size = int(sock.recv(1024))

    # Opening and reading file.
    with open("./rec/" + file_name, "wb") as file:
        c = 0
        # Starting the time capture.
        start_time = time.time()

        # Running the loop while file is recieved.
        while c <= int(file_size):
            data = sock.recv(1024)
            if not (data):
                break
            file.write(data)
            c += len(data)

        # Ending the time capture.
        end_time = time.time()

    print("File transfer Complete.Total time: ", end_time - start_time)




