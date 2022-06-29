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
    print("Welcom to Remote shell")
    input("What would to you like to do: ")
    print("1. Send command")
    print("2. Send file")
    print("3. Receive file")
    print("4. Exit")
    option = input("Enter option: ")
    if option == '1':
        send_command()
    elif option == '2':
        send_file()
    elif option == '3':
        receive_file()
    elif option == '4':
        sock.close()
        sys.exit()
    else:
        print("Invalid option")
        choose_option()


#send command to server
def send_command():
    while(True):
        print("Enter back to go back")
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
    print("Enter back to go back")
    # Getting file details.
    file_name = input("File to send:")
    if os.path.isfile(file_name):
    
        file_size = os.path.getsize(file_name)
        sock.send(str.encode(file_name))
        sock.send(str.encode(str.format(file_size)))
        # Opening file and sending data.
        with open(file_name, "rb") as file:
            c = 0
            # Starting the time capture.
            start_time = time.time()

            # Running loop while c != file_size.
            print("Sending file...")
            while c <= file_size:
                data = file.read(1024)
                if not (data):
                    break
                sock.sendall(data)
                c += len(data)

            # Ending the time capture.
            end_time = time.time()

        print("File Transfer Complete . Total time to transfer: ", end_time - start_time)
    else:
        print ("File not exist")



#receive file from server
def receive_file():
    print("Enter back to go back")
    # Getting file details.
    file_name = input("File to receive:")
    file_size = int(sock.recv(1024))

    # Opening and reading file.
    with open("./rec/" + file_name, "wb") as file:
        c = 0
        # Starting the time capture.
        start_time = time.time()
        print("Receiving file...")
        # Running the loop while file is recieved.
        while c <= int(file_size):
            data = sock.recv(1024)
            if not (data):
                break
            file.write(data)
            c += len(data)

        # Ending the time capture.
        end_time = time.time()

    print("File received .Total time: ", end_time - start_time)




