#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 18:42:49 2022

@author: hfchame
"""

import cv2
import mediapipe as mp
import numpy as np 
import time
from numpy import linalg
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

landMarkLabels = ['nose',\
                  'left_eye_inner', 
                  'left_eye', 
                  'left_eye_outer',
                  'right_eye_inner', 
                  'right_eye', 
                  'right_eye_outer',
                  'left_ear',
                  'right_ear',
                  'mouth_left',
                  'mouth_right',
                  'left_shoulder',
                  'right_shoulder',
                  'left_elbow',
                  'right_elbow',
                  'left_wrist',
                  'right_wrist',
                  'left_pinky',
                  'right_pinky',
                  'left_index',
                  'right_index',
                  'left_thumb',
                  'right_thumb',
                  'left_hip',
                  'right_hip',
                  'left_knee',
                  'right_knee',
                  'left_ankle',
                  'right_ankle',
                  'left_heel',
                  'right_heel',
                  'left_foot_index',
                  'right_foot_index']

useful_landmarks = [
  'left_shoulder',
  'right_shoulder',
  'left_elbow',
  'right_elbow',
  'left_hip',
  'right_hip',
]
      
## Doc API https://google.github.io/mediapipe/solutions/pose.html
def getTimeInMS():
    return round(time.time()*1000)

def vecteur(p1, p2):
    return[p2.x-p1.x, p2.y-p1.y]

def angle(v1, v2):
    return math.degrees(np.arccos(np.dot(v1, v2) / (linalg.norm(v1) * linalg.norm(v2))))

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    t1 = getTimeInMS()
    
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # ²
        
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    
    t2 = getTimeInMS()
    # print("Loop time in ms : {}".format(t2 - t1))
    
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
        cv2.destroyWindow('MediaPipe Pose')
        break
      
    # Left and right shoulder angle calculations
    xr = vecteur(results.pose_landmarks.landmark[12], results.pose_landmarks.landmark[14])
    yr = vecteur(results.pose_landmarks.landmark[12], results.pose_landmarks.landmark[24])
    xl = vecteur(results.pose_landmarks.landmark[11], results.pose_landmarks.landmark[13])
    yl = vecteur(results.pose_landmarks.landmark[11], results.pose_landmarks.landmark[23])

    aShoulderRest = 12.3
    aShoulderExtension = 76
    aRightShoulder = angle(xr, yr)
    aLeftShoulder = angle(xl, yl)

    print("aLeftShoulder : " + str(aLeftShoulder) + ", aRightShoulder : " + str(aRightShoulder))

    aRightShoulderNorm = (aRightShoulder - aShoulderRest) / (aShoulderExtension - aShoulderRest)
    aLeftShoulderNorm = (aLeftShoulder - aShoulderRest) / (aShoulderExtension - aShoulderRest)

cap.release()
