import socket
from termcolor import colored

port = 5000

s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)

s.bind(('', port))

print(colored("Server is ready", 'green', attrs=['bold']))

has_been_connected = False
while not has_been_connected:
    s.listen(1) # Allow a maximum of 1 unaccepted connection before closing the socket
    
    c, addr = s.accept() # Accept the connection from an entering device
    print(f"CONNECTION FROM: {str(addr)}") # Printing the new connection

    # Receive the messages
    received_data = c.recv(1024)

    # TODO : decode properly the byte data
    print(int.from_bytes(received_data, 'big'))

    # TODO : read both values

    # TODO : send values to the array

    

    