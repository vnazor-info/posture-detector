import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import math

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

        for lm in range(len(self.pose_landmarks)):
            actual_lm = self.pose_landmarks[lm]
            self.pose_landmarks_list = landmark_pb2.NormalizedLandmarkList()
            self.pose_landmarks_list.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in actual_lm
            ])

        #OVO MORA BITI TU JER KAD IMAMO LISTU ONA JE NESTED, SA OVIME MOZEMO VADITI LANDMARK
        #INACE JE OVAKO [[x1,y1,z1]], NAMA TREBA [x1,y1,z1]
        #NAGLASAK NA ZAGRADE

        if not detect.pose_landmarks:
            self.pose_landmarks = None
            detected = False
        
        right_shoulder = self.pose_landmarks_list.landmark[12]
        left_hip = self.pose_landmarks_list.landmark[23]
        right_hip = self.pose_landmarks_list.landmark[24]
        left_knee = self.pose_landmarks_list.landmark[25]
        right_knee = self.pose_landmarks_list.landmark[26]
        right_elbow = self.pose_landmarks_list.landmark[14]
        left_elbow = self.pose_landmarks_list.landmark[13]
        left_shoulder = self.pose_landmarks_list.landmark[11]
        self.dictionary = {
            "left_shoulder": (left_shoulder.x, left_shoulder.y),
            "right_shoulder": (right_shoulder.x, right_shoulder.y),  
            "left_hip": (left_hip.x, left_hip.y),
            "right_hip": (right_hip.x, right_hip.y),
            "left_knee": (left_knee.x, left_knee.y),
            "right_knee": (right_knee.x, right_knee.y),
            "left_elbow": (left_elbow.x, left_elbow.y),
            "right_elbow": (right_elbow.x, right_elbow.y),
            }

        self.left_arm = {
            "left_shoulder" : (left_shoulder.x, left_shoulder.y),
            "left_elbow": (left_elbow.x, left_elbow.y),
            }
        self.right_arm = {
            "right_shoulder": (right_shoulder.x, right_shoulder.y),
            "right_elbow": (right_elbow.x, right_elbow.y),
            }
        self.left_leg = {
            "left_hip": (left_hip.x, left_hip.y),
            "left_knee": (left_knee.x, left_knee.y),
            }
        self.right_leg = {
            "right_hip": (right_hip.x, right_hip.y),
            "right_knee": (right_knee.x, right_knee.y),
            }
        self.dict_parts = {
            "left_arm" : self.left_arm,
            "right_arm" : self.right_arm,
            "left_leg" : self.left_leg,
            "right_leg" : self.right_leg
            }

        return detected

    def get_landmarks(self):
        return self.pose_landmarks

    def draw_landmarks(self, image):
        annotated_image = image.numpy_view().copy()
        #OVO PRETVARA SLIKU U NUMPY ARRAY DA BI SE MOGLA ISCRTAVATI
        
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            self.pose_landmarks_list,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
            #OVO ISCRTAVA LANDMARKE NA SLIKU
        image = annotated_image 
        return image
        #VRATI SLIKU SA ISCRTANIM LANDMARKIMA

    def racunanje (self, a, b, c):
        ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) - 
        math.atan2(a[1]-b[1], a[0]-b[0])
    )
        return ang + 360 if ang < 0 else ang
