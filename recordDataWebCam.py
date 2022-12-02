#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: prise de données des capteur et sauvegarde dans un fichier csv """

import cv2

from naoqi import ALProxy
import os
import argparse
import os
import time
import signal 
from PIL import Image

def getTimeInMS():
    return round(time.time()*1000)

continueLoop = True

# Interceptation du signal Control+C
def handler(signum, frame):
    global continueLoop
    print("Ctrl-c was pressed !")
    continueLoop = False

signal.signal(signal.SIGINT, handler)

        
def main(IP, port, dataDir):
    global continueLoop

    frameId = 0    
    naoqiExpVarID = "IDMC_exp_cond"
    naoqiExpVarValue = ""

    # MEMORY_VALUE_NAMES : liste de données souhaités.
    ALMEMORY_KEY_NAMES = ["Device/SubDeviceList/RShoulderRoll/Position/Sensor/Value",
                          "Device/SubDeviceList/LShoulderRoll/Position/Sensor/Value"]
    
    # capture d'image depuis la camera web
    camera = cv2.VideoCapture(0)
    
    """ Parse command line arguments, run recordData
    and write the results into a csv file.
    """
    global continueLoop
    
    # Obtention du proxy au module ALMemory.
    memory_service = ALProxy("ALMemory", IP, port)
    
    print("Data recorder launched")
    
    print("Waiting for experiment to start ...")
    # waiting for the experiment to begin
    while continueLoop and naoqiExpVarValue == "":
        try :
            naoqiExpVarValue = memory_service.getData(naoqiExpVarID)
        except BaseException as err:
            continue
        time.sleep(0.05)
    
    expCond = naoqiExpVarValue
    dataDir += '/' + naoqiExpVarValue
    output = os.path.abspath(dataDir + "/robotJoints.csv")
    
    loopCount = 0
    
    if continueLoop :
        cv2.namedWindow("Webcam")
        
        with open(output, "w") as fp:
            t0 = getTimeInMS()
            t1 = t0
            while continueLoop and not naoqiExpVarValue == "":
                t1 = getTimeInMS()
                fp.write("{}; ".format(t1-t0))
                t0 = t1
                for key in ALMEMORY_KEY_NAMES:
                    value = memory_service.getData(key, True)
                    fp.write("{}; ".format(value))
                fp.write("\n")
                return_value, image = camera.read()
                cv2.imwrite(dataDir + '/x{:04d}'.format(frameId)+'.png', image)
                frameId += 1
                # obtention de données à partir de la camera
                cv2.imshow("Webcam", image)
                if cv2.waitKey(5) & 0xFF == 27:
                    cv2.destroyWindow("Webcam")
                    continueLoop = False
                time.sleep(0.05)
                naoqiExpVarValue = memory_service.getData(naoqiExpVarID)
                loopCount += 1
            
    if (loopCount == 0):
        print ("No data was capture for experiment condition : {}".format(expCond))
    else:
        print ("Experiment data saved to : '{}'".format(dataDir))
            

if __name__ == "__main__":
    IP = "169.254.248.220"
    IP = "192.168.137.147"
    #IP = "192.168.137.147"
    port = 9559
    baseDir = 'Exp_data'
    
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)
    for expCond in ['A','B','C','D']:
        dataDir = "{}/{}".format(baseDir,expCond)
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)
    main(IP,port,baseDir)
