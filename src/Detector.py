from . import config as cfg
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
#Detector klasa koristi MediaPipe za detekciju objekata na slikama.
#Koristi se ObjectDetector iz MediaPipe Vision modula za prepoznavanje objekata.

#
#Dolje navedeni kod se mne koristi u trenutnoj implementaciji, ali je zadržan radi budućih referenci.
#Ako se odlučimo koristiti drugačiji model ili dodati dodatne funkcionalnosti, možda će biti potreban.
#Ovaj dio nismo koristili jer oduzima resurse i usporava izvođenje programa.
#

class Detector:
    def __init__(self, model_path):
        BaseOptions = mp.tasks.BaseOptions
        ObjectDetector = mp.tasks.vision.ObjectDetector
        ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
        #Inicijalizacija potrebnih klasa iz MediaPipe biblioteke.


        # Postavljanje opcija za detektor objekata, uključujući put do modela i prag povjerenja za detekciju.
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
