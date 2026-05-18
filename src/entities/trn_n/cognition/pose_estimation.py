"""
====================================================================
[MediaPipe-based Pose Estimator]

This code utilizes Google's MediaPipe Vision library to analyze 
and visualize human poses in images.

<Key Features>
1. Landmark Detection: Detects 33 key body joints (eyes, nose, 
   shoulders, knees, etc.) and extracts their (x, y) coordinates.
2. Pose Alignment (align_person): Calculates the alignment of the 
   shoulders and hips to rotate the image, ensuring the person 
   stands vertically straight.
3. Visibility Estimation (estimate_visibility): Checks whether each 
   detected joint is within the visible image boundary (0.0 to 1.0).
4. Visualization (draw_landmarks): Overlays the detected landmarks (dots), 
   keypoint names, and skeleton connections onto the original image.

(Generated with the assistance of Gemini 3.1 Pro)
====================================================================
"""

import math
import os
import cv2
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision.core import image as mp_image

# List of 33 pose landmark names detected by MediaPipe.
POSE_KEYPOINT_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer", "right_eye_inner", 
    "right_eye", "right_eye_outer", "left_ear", "right_ear", "mouth_left", 
    "mouth_right", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow", 
    "left_wrist", "right_wrist", "left_pinky_1", "right_pinky_1", "left_index_1", 
    "right_index_1", "left_thumb_2", "right_thumb_2", "left_hip", "right_hip", 
    "left_knee", "right_knee", "left_ankle", "right_ankle", "left_heel", 
    "right_heel", "left_foot_index", "right_foot_index",
]

# Definition of landmark connections to draw the skeleton lines.
POSE_CONNECTIONS = vision.PoseLandmarksConnections.POSE_LANDMARKS

class PoseLandmarksWrapper:
    """A simple wrapper class to encapsulate landmark data."""
    def __init__(self, landmarks):
        self.landmark = landmarks

class PoseEstimatorResult:
    """A data class to store the final pose estimation results."""
    def __init__(self, pose_landmarks, visibility=None, aligned_image=None):
        self.pose_landmarks = pose_landmarks  # Detected coordinates
        self.visibility = visibility or []    # Visibility status of each joint
        self.aligned_image = aligned_image    # Pose-corrected (rotated) image

class PoseEstimator:
    """Main class to run pose estimation and process images using MediaPipe."""
    def __init__(self, model_path=None, running_mode='IMAGE'):
        # If no model path is provided, find 'pose_landmarker.task' in the current directory.
        if model_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, 'pose_landmarker.task')

        self.model_path = model_path
        self.previous_landmarks = None  # Cache for previous frame landmarks to align the pose

        # Check if the model file exists and initialize the landmarker.
        if os.path.exists(model_path):
            self.running_mode = getattr(vision.VisionRunningMode, running_mode, vision.VisionRunningMode.IMAGE)
            
            # Configure MediaPipe Pose Landmarker options
            self._options = vision.PoseLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=self.model_path),
                running_mode=self.running_mode,
                num_poses=1,                           # Max number of poses to detect
                min_pose_detection_confidence=0.5,     # Min confidence for person detection
                min_pose_presence_confidence=0.5,      # Min confidence for pose landmarks
                min_tracking_confidence=0.5,           # Min confidence for tracking
            )
            # Create the landmarker instance
            self.landmarker = vision.PoseLandmarker.create_from_options(self._options)
            self.model_loaded = True
        else:
            self.landmarker = None
            self.model_loaded = False
            print(
                f"Warning: PoseLandmarker model not found at {model_path}. "
                "Pose estimation will be disabled until a valid model is provided."
            )

    def process_image(self, image):
        """Processes the input image to estimate pose and returns the results."""
        if not self.model_loaded:
            return PoseEstimatorResult(None, visibility=[], aligned_image=image)

        # Convert OpenCV's BGR image to MediaPipe's RGB format.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image_obj = mp_image.Image(image_format=mp_image.ImageFormat.SRGB, data=rgb_image)

        aligned_image = image
        # If landmarks from the previous frame exist, rotate the image to align the person vertically.
        if self.previous_landmarks is not None:
            aligned_image = self.align_person(image, self.previous_landmarks)
            mp_image_obj = mp_image.Image(image_format=mp_image.ImageFormat.SRGB, data=cv2.cvtColor(aligned_image, cv2.COLOR_BGR2RGB))

        # Perform landmark detection using MediaPipe
        result = self.landmarker.detect(mp_image_obj)
        visibility = []

        # If a pose is detected, parse and return the results.
        if result.pose_landmarks and len(result.pose_landmarks) > 0:
            landmarks = result.pose_landmarks[0]
            wrapped = PoseLandmarksWrapper(landmarks)
            visibility = self.estimate_visibility(landmarks)  # Check if landmarks are inside the frame
            self.previous_landmarks = landmarks              # Cache the current landmarks for the next frame
            return PoseEstimatorResult(wrapped, visibility=visibility, aligned_image=aligned_image)

        return PoseEstimatorResult(None, visibility=visibility, aligned_image=aligned_image)

    def estimate_visibility(self, landmarks):
        """Checks if each landmark (joint) is within the visible image area (0.0 to 1.0)."""
        visibility = []
        for lm in landmarks:
            # Returns True if x and y are within the normalized image boundaries [0, 1]
            visible = 0.0 <= lm.x <= 1.0 and 0.0 <= lm.y <= 1.0
            visibility.append(visible)
        return visibility

    def align_person(self, image, landmarks):
        """Rotates the image to align the person's torso straight up based on shoulders and hips."""
        # Check if required tracking joints (shoulders and hips) are available
        if len(landmarks) <= max(23, 24, 11, 12):
            return image

        left_hip = landmarks[23]
        right_hip = landmarks[24]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        # Calculate the midpoints of the hips and shoulders.
        mid_hip = ((left_hip.x + right_hip.x) / 2.0, (left_hip.y + right_hip.y) / 2.0)
        mid_shoulder = ((left_shoulder.x + right_shoulder.x) / 2.0, (left_shoulder.y + right_shoulder.y) / 2.0)
        
        # Calculate the delta distances between mid-shoulder and mid-hip.
        dx = mid_shoulder[0] - mid_hip[0]
        dy = mid_shoulder[1] - mid_hip[1]
        
        # Calculate the rotation angle and offset by 90 degrees to align it vertically.
        angle = math.degrees(math.atan2(dy, dx)) - 90

        # Rotate the image using an affine transformation matrix.
        height, width = image.shape[:2]
        center = (int(mid_hip[0] * width), int(mid_hip[1] * height))  # Set rotation center at the mid-hip
        rot = cv2.getRotationMatrix2D(center, angle, 1.0)
        aligned = cv2.warpAffine(image, rot, (width, height), flags=cv2.INTER_LINEAR)

        return aligned

    def draw_landmarks(self, image, results):
        """Draws detected landmarks, joint names, and skeleton lines onto the image."""
        if not results or not results.pose_landmarks:
            return image

        landmarks = results.pose_landmarks.landmark
        height, width = image.shape[:2]

        # 1. Draw individual joint points (dots) and overlay their names.
        for idx, landmark in enumerate(landmarks):
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            cv2.circle(image, (x, y), 3, (0, 255, 0), -1)  # Draw a green dot
            if idx < len(POSE_KEYPOINT_NAMES):
                # Put the text label for the joint name
                cv2.putText(image, POSE_KEYPOINT_NAMES[idx], (x + 2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

        # 2. Connect the joints with lines to draw the skeleton structure.
        for connection in POSE_CONNECTIONS:
            start = landmarks[connection.start]
            end = landmarks[connection.end]
            start_point = (int(start.x * width), int(start.y * height))
            end_point = (int(end.x * width), int(end.y * height))
            cv2.line(image, start_point, end_point, (0, 255, 0), 2)  # Draw a green connecting line

        return image

    def close(self):
        """Releases the MediaPipe Landmarker resources to free up memory."""
        if self.landmarker is not None:
            self.landmarker.close()