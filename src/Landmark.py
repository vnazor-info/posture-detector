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
        self.nose = 0
        self.left_eye_inner = 1
        self.left_eye = 2
        self.left_eye_outer = 3
        self.right_eye_inner = 4
        self.right_eye = 5
        self.right_eye_outer = 6
        self.left_ear = 7
        self.right_ear = 8
        self.mouth_left = 9
        self.mouth_right = 10
        self.left_shoulder = 11
        self.right_shoulder = 12
        self.left_elbow = 13
        self.right_elbow = 14
        self.left_wrist = 15
        self.right_wrist = 16
        self.left_pinky = 17
        self.right_pinky = 18
        self.left_index = 19
        self.right_index = 20
        self.left_thumb = 21
        self.right_thumb = 22
        self.left_hip = 23
        self.right_hip = 24
        self.left_knee = 25
        self.right_knee = 26
        self.left_ankle = 27
        self.right_ankle = 28
        self.left_heel = 29
        self.right_heel = 30
        self.left_foot_index = 31
        self.right_foot_index = 32
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
    def calculate_angle(self, line1_name, line2_name):
        line1 = self.get_line(line1_name)
        line2 = self.get_line(line2_name)
        return self.__calculate_angle_2d(line1, line2)

    def get_line(self, name):
        if name == "shoulders":
            return [[self.pose_landmarks_list.landmark[self.left_shoulder].x, self.pose_landmarks_list.landmark[self.left_shoulder].y],
                    [self.pose_landmarks_list.landmark[self.right_shoulder].x, self.pose_landmarks_list.landmark[self.right_shoulder].y]]
        elif name == "hips":
            return [[self.pose_landmarks_list.landmark[self.left_hip].x, self.pose_landmarks_list.landmark[self.left_hip].y],
                    [self.pose_landmarks_list.landmark[self.right_hip].x, self.pose_landmarks_list.landmark[self.right_hip].y]]
        else:
            raise ValueError("Unknown line name")

    def __calculate_angle_2d(self, line1, line2):
        # line1 = [(x1, y1), (x2, y2)]
        
        # 1. Vektor prve linije (kraj - početak)
        v1_x = line1[1][0] - line1[0][0]
        v1_y = line1[1][1] - line1[0][1]
        
        # 2. Vektor druge linije (kraj - početak)
        v2_x = line2[1][0] - line2[0][0]
        v2_y = line2[1][1] - line2[0][1]
        
        # 3. Izračun kuta svakog vektora u radijanima
        angle1 = math.atan2(v1_y, v1_x)
        angle2 = math.atan2(v2_y, v2_x)
        
        # 4. Razlika u stupnjevima
        diff = abs(math.degrees(angle1 - angle2))
        
        # 5. Normalizacija na najmanji kut (oštri kut)
        # Ovo osigurava da rezultat bude između 0 i 180
        if diff > 180:
            diff = 360 - diff
            
        return min(diff, 180 - diff)
