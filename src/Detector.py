from . import config as cfg
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class Detector:
    def __init__(self, model_path):
        BaseOptions = mp.tasks.BaseOptions
        ObjectDetector = mp.tasks.vision.ObjectDetector
        ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
        VisionRunningMode = mp.tasks.vision.RunningMode


        # STEP 2: Create an ObjectDetector object.
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.ObjectDetectorOptions(base_options=base_options,
                                                score_threshold=0.5)
        self.detector = vision.ObjectDetector.create_from_options(options)
        
    def detect(self, image): #Samo osobe detektiramo
        
        detection_result = self.detector.detect(image)
        #pronalazi osobu i vraća bounding_box
        
        #bbox = detection_result.detections[0].bounding_box
        return detection_result.detections

    def crop_person(self, image, bbox):
        #obrezuje sliku na temelju bbox i vrasća ovrezanu sliku
        cropped_image = image.numpy_view()[bbox.origin_y:bbox.origin_y+bbox.height+10, bbox.origin_x-10:bbox.origin_x+bbox.width]
        cropped_image = np.array(cropped_image)
        return mp.Image(image_format=mp.ImageFormat.SRGB, data=cropped_image)
