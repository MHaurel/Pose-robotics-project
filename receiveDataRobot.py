import socket
from termcolor import colored
import argparse
import qi
import sys
import time
from naoqi import ALProxy
import numpy as np

parser = argparse.ArgumentParser()
ip_robot = "127.0.0.1"
robot_port = 54826
parser.add_argument("--ip", type=str, default=ip_robot,
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
parser.add_argument("--port", type=int, default=robot_port,
                        help="Naoqi port number")
args = parser.parse_args()
session = qi.Session()

try:
    session.connect("tcp://" + args.ip + ":" + str(args.port))
    print(colored("Robot connected on port " + str(args.port) + " with ip " + args.ip, "green"))
except RuntimeError:
    print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
    sys.exit(1)

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
    print("CONNECTION FROM: ", str(addr)) # Printing the new connection

    # Receive the messages
    # try:
    try:
        aLeftShoulderNorm = float(c.recv(1024))
    

    # TODO : decode properly the byte data
    # print(float(received_data))
        print(aLeftShoulderNorm, type(aLeftShoulderNorm))

    # TODO : read both values

    # TODO : send values to the robot
        motion_service = session.service("ALMotion")

        try:
            motion_service.setAngles("LShoulderRoll", aLeftShoulderNorm, 0.15)
        except BaseException as be:
            print(be)
    except ValueError as ve:
        print(colored("Could not convert string to float", 'red'))

    

    