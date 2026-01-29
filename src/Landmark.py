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
        
        
    
    def draw_landmarks(self, person_crop):

        # STEP 4: Detect pose landmarks from the input image.
        detection_result = self.detector.detect(person_crop)
        self.pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = person_crop.numpy_view().copy()

        # Loop through the detected poses to visualize.
        landmark_num =len(self.pose_landmarks_list)
        if landmark_num == 0:
            return None
        for idx in range(landmark_num):
            pose_landmarks = self.pose_landmarks_list[idx]
            # Draw the pose landmarks.
            self.pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            
            self.pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            print("pose_landmarks 1", self.pose_landmarks_proto)
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                self.pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())
            print("pose_landmarks 2", self.pose_landmarks_proto)
        landmark_list = []
        #for idx in self.pose_landmarks_proto.landmark:
        #    landmark_list.append((idx.x, idx.y))
        
        self.landmark_list = landmark_list
        return annotated_image
            #cv2.imwrite("drawlandmarks.jpg", detection_result)
            # STEP 5: Process the detection result. In this case, visualize it.




class Detective:    
    def __init__(self):
        self.base_options = python.BaseOptions(model_asset_path='resources/pose_landmarker_heavy.task')
        self.options = vision.PoseLandmarkerOptions(
            base_options=self.base_options,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(self.options)
        self.pose_landmarks = None

    def person_detected(self, person_crop):
        detected = True
        detect = self.detector.detect(person_crop)
        self.pose_landmarks = detect.pose_landmarks

        if not detect.pose_landmarks:
            self.pose_landmarks = None
            detected = False
        return detected

    def get_landmarks(self):
        return self.pose_landmarks

    def draw_landmarks(self, image):
        for landmark in self.pose_landmarks:
            print(landmark)
            solutions.drawing_utils.draw_landmarks(
                image,
                landmark,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())
        return annotated_image
            #cv2.imwrite("drawlandmarks.jpg", detection_result)
            # STEP 5: Process the detection result. In this case, visualize it.