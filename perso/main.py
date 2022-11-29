import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from utils import get_new_pose_landmarks_style, NEW_POSE_CONNECTIONS, _POSE_CONNECTIONS
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

points = [
  mp_pose.PoseLandmark.LEFT_SHOULDER,   # 11
  mp_pose.PoseLandmark.RIGHT_SHOULDER,  # 12
  mp_pose.PoseLandmark.LEFT_ELBOW,      # 13  
  mp_pose.PoseLandmark.RIGHT_ELBOW,     # 14
  mp_pose.PoseLandmark.LEFT_WRIST,      # 15
  mp_pose.PoseLandmark.RIGHT_WRIST,     # 16
  mp_pose.PoseLandmark.LEFT_HIP,        # 23
  mp_pose.PoseLandmark.RIGHT_HIP,       # 24
]

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

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    landmark_subset = landmark_pb2.NormalizedLandmarkList(
      landmark = [
        results.pose_landmarks.landmark[point] for point in points
      ]
    )

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        # landmark_subset,
        mp_pose.POSE_CONNECTIONS,
        # NEW_POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        # landmark_drawing_spec=get_new_pose_landmarks_style()
    )

    # Print values landmarks
    # for point in points:
    #     print(f"{point} : {[results.pose_landmarks.landmark[point].x, results.pose_landmarks.landmark[point].y, results.pose_landmarks.landmark[point].z]}")

    

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()