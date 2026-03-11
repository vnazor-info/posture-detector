##classes
from src import lib
from src import Camera
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
##model

#Pokretanje različitih testova i demonstracija iz lib modula.
  
#lib.detector_showcase()
#lib.person_detect()
#lib.stickfigure_videotest()
#lib.camera_test()
#lib.camera_class_test()
#lib.tktinker_test()
#lib.playground()
#lib.test()
lib.GUI_test()

#
#U main.py datoteci pokrećemo različite testove i demonstracije koje smo implementirali u lib modulu.
#Trenutno je aktivan samo tktinker_test() poziv, dok su ostali pozivi komentirani.
#Ovo nam omogućava da lako prebacujemo između različitih testova bez brisanja koda.
#