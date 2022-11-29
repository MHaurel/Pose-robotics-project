#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: prise de données des capteurs et sauvegarde dans un fichier csv """

import cv2

from naoqi import ALProxy
import os
import time
import signal 


# MEMORY_VALUE_NAMES : liste de données souhaités.
ALMEMORY_KEY_NAMES = ["Device/SubDeviceList/RShoulderRoll/Position/Sensor/Value",
                      "Device/SubDeviceList/LShoulderRoll/Position/Sensor/Value"]

continueLoop = True

# Interceptation du signal Control+C
def handler(signum, frame):
    global continueLoop
    print("Ctrl-c was pressed !")
    continueLoop = False

signal.signal(signal.SIGINT, handler)

        
def main(IP, port):
    frameId = 0
    
    # capture d'image depuis la camera web
    camera = cv2.VideoCapture(0)
    cv2.namedWindow("Webcam")

    """ Parse command line arguments, run recordData
    and write the results into a csv file.
    """
    global continueLoop
    
    # Obtention du proxy au module ALMemory.
    memory_service = ALProxy("ALMemory", IP, port)
    output = os.path.abspath("record.csv")
    
    with open(output, "w") as fp:

        while continueLoop:
            for key in ALMEMORY_KEY_NAMES:
                value = memory_service.getData(key, True)
                fp.write("{}; ".format(value))
            fp.write("\n")
            return_value, image = camera.read()
            cv2.imwrite('img/i_{:04d}'.format(frameId)+'.png', image)
            frameId += 1
            # obtention de données à partir de la camera
            cv2.imshow("Webcam", image)
            if cv2.waitKey(5) & 0xFF == 27:
                cv2.destroyWindow("Webcam")
                continueLoop = False
            time.sleep(0.05)
            
    print ("Results written to", output)


if __name__ == "__main__":
    IP = "127.0.0.1"    # IP of the robot
    port = 60557        # Port protocole
    main(IP,port)