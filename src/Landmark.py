import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

class Landmark:

    def __init__(self, model_path):
        self.base_options = python.BaseOptions(model_asset_path='resources/pose_landmarker_heavy.task')
        self.options = vision.PoseLandmarkerOptions(
            base_options=self.base_options,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(self.options)

    
    def draw_landmark(self, person_crop):

        # STEP 4: Detect pose landmarks from the input image.
        detection_result = self.detector.detect(person_crop)
        print(detection_result)
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = person_crop.numpy_view().copy()

        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())
        return annotated_image
            #cv2.imwrite("drawlandmarks.jpg", detection_result)
            # STEP 5: Process the detection result. In this case, visualize it.