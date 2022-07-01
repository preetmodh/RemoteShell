import socket
import os
import sys
import time

from numpy import choose


sock = socket.socket()
host = '192.168.112.248'
port = 9999

sock.connect((host, port))


def choose_command(client_currentWD):
    shell_name="<"+host+"> " + client_currentWD
    command = input(shell_name)


    if "send" in ''.join(command[:5]).lower():
        send_file(command)
    elif "receive" in ''.join(command[:9]).lower():
        receive_file(command)
    elif "exit" in ''.join(command[:5]).lower():
        sock.close()
        sys.exit()
    else:
        client_currentWD=send_command(command)
    choose_command(client_currentWD)
    


#send command to server
def send_command(command):
    if len(str.encode(command))>0:
            #send the command
            sock.send(str.encode(command))
            #receive the response
            server_response = str(sock.recv(2147483647//2), 'utf-8')
            client_currentWD = server_response[:server_response.find("> ")+2]
            output_response = server_response[server_response.find("> ")+2:]
            print(output_response, end="")
    return client_currentWD

#send file to server
def send_file(command):
    file_info_list = command.strip(' ') # remove trailing spaces
    file_info_list = list(map(int,input().split()))
    file_path = file_info_list[1] # 0th element is the command, 1st element is the file path
    if os.path.isfile(file_path):
        
        file_size = os.path.getsize(file_path)
        sock.send(str.encode(str(file_size)))
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
                sock.sendall(data)
                c += len(data)

            # Ending the time capture.
            end_time = time.time()

        print("File Transfer Complete . Total time to transfer: ", end_time - start_time)
    else:
        print ("File path does not exist")
    return None



#receive file from server
def receive_file(command):
    file_info_list = command.strip(' ') # remove trailing spaces
    file_info_list = list(map(int,input().split()))
    file_name = file_info_list[2] # 0th element is the command, 2nd element is the file name
    file_path = file_info_list[1] # 1st element is  the file  path 
    # Getting file details.
    sock.send(str.encode(str(file_path)))
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
    return None



def main():
    print("Welcome to " + host + "'s " + "shell")
    client_currentWD = str(sock.recv(1024), 'utf-8')
    choose_command(client_currentWD)

main()