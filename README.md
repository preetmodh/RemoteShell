
# Overview

This is a multi-client to server cross platform remote shell written in Python. There is still a lot of work to do, so feel free to help out or to add new features.


# How to Use

To use this Remote shell, two scripts need to be running
* You need to install two libraries in server using pip:`pip install psutil` and `pip install py-cpuinfo`
* **server.py** - runs on a public server and waits for clients to connect
* **client.py** - connects to a remote server 

***

## Server

To set up server script, simply run **server.py** using Python 3.6+

`python3 server.py`

After running will listen for connections and multiple clients can connect to server (with help of **Threading** and **Multi-Processing**)

***

## Client

In **client.py**, first change the IP address to that of the server and then run using Python 3.6+.

`python3 client.py`

After running will connect to server and enter into server's remote shell.

You can enter `list` in the shell to list out all the commands ,which are:


* **`send <filepath> <filename>`** - send file to server ;filepath is the path of file you want to send ;filename is the name you want to give
* **`receive <filepath> <filename>`** - receive file from server ;filepath is the path of file you want to receive ;filename is the name you want to give
* **`sysinfo`** - get system info from server
* **`help`** - list commandline options 
* **`exit`** - exit the shell

After connecting you can iteract with the server or target machine's command line in any way you want using the command-line commands

# Disclaimer: 
Accessing a computer network without authorization or permission is illegal. 
