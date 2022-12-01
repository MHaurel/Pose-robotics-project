import socket
import time
  
# take the server name and port name
port = 5000
  
# create a socket at client side
# using TCP / IP protocol
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)
  
# connect it to server and port
# number on local computer.
s.connect(('127.0.0.1', port))
  
while True:
    msg = b"hello"
    s.send(msg)
    
    s.close()

    time.sleep(1)