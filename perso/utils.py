from mediapipe.python.solutions.drawing_styles import DrawingSpec
from mediapipe.python.solutions.pose import PoseLandmark

NEW_POSE_CONNECTIONS = frozenset([
  (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), (11, 23), (23, 24), (12, 24)
])

_POSE_CONNECTIONS = frozenset([
    (11, 12), (11, 13),
    (12, 14), (14, 16), (13, 15),
    (11, 23), (12, 24), (23, 24)])

_RADIUS = 5
_RED = (48, 48, 255)
_GREEN = (48, 255, 48)
_BLUE = (192, 101, 21)
_YELLOW = (0, 204, 255)
_GRAY = (128, 128, 128)
_PURPLE = (128, 64, 128)
_PEACH = (180, 229, 255)
_WHITE = (224, 224, 224)
_THICKNESS_POSE_LANDMARKS = 2
_POSE_LANDMARKS_LEFT = frozenset([
    PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_ELBOW,
    PoseLandmark.LEFT_WRIST, PoseLandmark.LEFT_HIP
])

_POSE_LANDMARKS_RIGHT = frozenset([
    PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_ELBOW, 
    PoseLandmark.RIGHT_WRIST, PoseLandmark.RIGHT_HIP,
])

def get_new_pose_landmarks_style():
    pose_landmark_style = {}
    left_spec = DrawingSpec(
        color=(0, 138, 255), thickness=_THICKNESS_POSE_LANDMARKS)
    right_spec = DrawingSpec(
        color=(231, 217, 0), thickness=_THICKNESS_POSE_LANDMARKS)
    for landmark in _POSE_LANDMARKS_LEFT:
        pose_landmark_style[landmark] = left_spec
    for landmark in _POSE_LANDMARKS_RIGHT:
        pose_landmark_style[landmark] = right_spec
    # pose_landmark_style[PoseLandmark.NOSE] = DrawingSpec(
    #     color=_WHITE, thickness=_THICKNESS_POSE_LANDMARKS)
    return pose_landmark_style