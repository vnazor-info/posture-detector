import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import math
from src import costume_drawing_skin
from src import drawing_spec
from src.config import get_resource_path

#Ovdje se uvoze potrebne biblioteke, uključujući MediaPipe za obradu slike i računalni vid, OpenCV za rad s kamerom i slike, te math za matematičke operacije.


class Landmark:

    def __init__(self, model_path):
        self.base_options = python.BaseOptions(model_asset_path='resources/pose_landmarker_heavy.task')
        self.options = vision.PoseLandmarkerOptions(
            base_options=self.base_options,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(self.options)

        #Inicijalizacija klase Landmark koja postavlja opcije za detekciju položaja koristeći MediaPipe Pose Landmarker model.
        #model_path parametar se koristi za specificiranje puta do modela, ali u ovom slučaju je hardkodiran unutar koda.
        
        
    
    def draw_landmarks(self, person_crop):

        detection_result = self.detector.detect(person_crop)
        self.pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = person_crop.numpy_view().copy()
        #Definiranje funkcije za iscrtavanje landmarka na slici. Funkcija prima izrezanu sliku osobe (person_crop) i koristi detektor za pronalaženje položaja.
        #Rezultat detekcije se sprema u self.pose_landmarks_list, a sl

        landmark_num =len(self.pose_landmarks_list)
        #Ako nema pronađenih landmarka (landmark_num je 0), funkcija vraća None. Inače, prolazi kroz svaki skup landmarka i iscrtava ih na slici koristeći MediaPipe drawing utilities.

        if landmark_num == 0:
            return None

        #Prolazak kroz svaki skup landmarka i iscrtavanje na slici. Za svaki skup landmarka, kreira se NormalizedLandmarkList koji se koristi za iscrtavanje na slici.
        for idx in range(landmark_num):
            pose_landmarks = self.pose_landmarks_list[idx]

            # Dodavanje landmarka u listu
            self.pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            
            self.pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            #Priprema podataka za iscrtavanje landmarka na slici.

            print("pose_landmarks 1", self.pose_landmarks_proto)
            #Linija koda iznad ispisuje listu svih tocaka na konsolu, ovo je korisno za debugiranje i provjeru da li su tocke pravilno detektirane i spremljene u self.pose_landmarks_proto.

            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                self.pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())
            #Iscrtavanje landmarka na slici koristeći MediaPipe drawing utilities. Ova funkcija koristi listu landmarka, veze između njih (POSE_CONNECTIONS) i stil iscrtavanja.    
            
            print("pose_landmarks 2", self.pose_landmarks_proto)
            #Linija koda iznad ponovo ispisuje listu svih tocaka na konsolu nakon iscrtavanja, ovo je korisno za provjeru da li se lista landmarka promijenila nakon iscrtavanja (što ne bi trebala).

        landmark_list = []
        #for idx in self.pose_landmarks_proto.landmark:
        #    landmark_list.append((idx.x, idx.y))

        #Ovaj dio koda je sluzio za pretvaranje NormalizedLandmarkList u jednostavniju listu koordinata, ali je trenutno zakomentiran. Ako bi se koristio, kreirao bi listu koordinata (x, y) za svaki landmark.
        
        self.landmark_list = landmark_list
        #Ovdje se sprema lista koordinata landmarka u self.landmark_list, ali budući da je kod za popunjavanje te liste zakomentiran, trenutno će self.landmark_list biti prazna lista.

        return annotated_image
        #Funkcija vraća sliku s iscrtanim landmarkima. Ako nije pronađen nijedan landmark, vraća None.

#
#Ovdje krece klasa Detective koja se koristi za detekciju osobe i rad s landmarkima. Ova klasa ima funkcije za detekciju osobe, dobivanje landmarka, iscrtavanje landmarka na slici i izračunavanje kuta između linija definiranih landmarkima.
#Sav kod ispod se trenutmeno koristi za detekciju i rad s landmarkima, ali se može proširiti i prilagoditi ovisno o potrebama projekta.
#

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
        self.shoulder_threshold = 5.0
        self.knee_threshold =5.0
        
        #Ovdje se definiraju indeksi za različite landmarke tijela, što omogućava lakši pristup tim landmarkima u funkcijama koje rade s njima. Na primjer, self.left_shoulder se koristi za pristup lijevom ramenu, self.right_knee za pristup desnom koljenu, itd. Ovi indeksi su standardni za MediaPipe Pose Landmarker model i omogućavaju nam da lako dohvatimo koordinate specifičnih dijelova tijela kada su detektirani na slici. Također, postavljen je prag (threshold) koji se koristi za detekciju lošeg držanja na temelju kuta između linija definiranih landmarkima.

        #Inicijalizacija klase Detective koja postavlja indekse za različite landmarke tijela. Ovi indeksi se koriste za pristup specifičnim landmarkima u listi landmarka koju vraća detektor.
        self.base_options = python.BaseOptions(model_asset_path=get_resource_path('resources/pose_landmarker_heavy.task'))
        self.options = vision.PoseLandmarkerOptions(
            base_options=self.base_options,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(self.options)

        #Napravljena lista indeksa za različite dijelove tijela, kao što su nos, oči, uši, ramena, laktovi, zapešća, kukovi, koljena, gležnjevi i stopala. Ova lista omogućava lakši pristup specifičnim landmarkima kada se detektiraju na slici.
        #Lista je prazna kako ne bi zauzimala memoriju, a indeksi se koriste direktno u funkcijama koje rade s landmarkima.
        self.pose_landmarks = None
        
    def person_detected(self, person_crop):
        detected = True
        detect = self.detector.detect(person_crop)
        self.pose_landmarks = detect.pose_landmarks
        #Ovdje se koristi detektor za pronalaženje položaja na izrezanoj slici osobe (person_crop). Rezultat detekcije se sprema u self.pose_landmarks. Ako nema pronađenih landmarka, funkcija postavlja self.pose_landmarks na None i vraća False, inače vraća True.

        for lm in range(len(self.pose_landmarks)):
            actual_lm = self.pose_landmarks[lm]
            self.pose_landmarks_list = landmark_pb2.NormalizedLandmarkList()
            self.pose_landmarks_list.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in actual_lm
            ])
            
            #Ovdje se prolazi kroz svaki skup landmarka pronađenih na slici i sprema se u self.pose_landmarks_list kao NormalizedLandmarkList. Ova lista se koristi za daljnju obradu, poput iscrtavanja landmarka na slici ili izračunavanja kuteva između linija definiranih landmarkima.

        #OVO MORA BITI TU JER KAD IMAMO LISTU ONA JE NESTED, SA OVIME MOZEMO VADITI LANDMARK
        #INACE JE OVAKO [[x1,y1,z1]], NAMA TREBA [x1,y1,z1]
        #NAGLASAK NA ZAGRADE

        if not detect.pose_landmarks:
            self.pose_landmarks = None
            detected = False
        return detected
        #Sprijecava kod da se pokrene dalje ako nije detektirana osoba, postavljanjem self.pose_landmarks na None i vraćanjem False. Ako je osoba detektirana, vraća True.

    def get_landmarks(self):
        return self.pose_landmarks
        #Funkcija za dobivanje landmarka. Vraća self.pose_landmarks, koji sadrži informacije o položaju različitih dijelova tijela detektirane osobe.

    def drawing_all_landmarks(self, image):
        annotated_image = image.numpy_view().copy()
        #OVO PRETVARA SLIKU U NUMPY ARRAY DA BI SE MOGLA ISCRTAVATI
        
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            self.pose_landmarks_list,
            solutions.pose.POSE_CONNECTIONS,
            costume_drawing_skin.get_default_pose_landmarks_style(),
            drawing_spec.DrawingNeutral()
            )
            #OVO ISCRTAVA LANDMARKE NA SLIKU

        image = annotated_image 
        return image
        #VRATI SLIKU SA ISCRTANIM LANDMARKIMA

    def calculate_angle(self, line1_name, line2_name):
        line1 = self.get_line(line1_name)
        line2 = self.get_line(line2_name)
        return self.__calculate_angle_2d(line1, line2)
        #Funkcija za izračunavanje kuta između dvije linije definiranih landmarkima. Prima imena linija (line1_name i line2_name), dobiva koordinate tih linija koristeći funkciju get_line, i zatim koristi privatnu funkciju __calculate_angle_2d za izračunavanje kuta između tih linija u 2D prostoru.

    def get_line(self, name):
        if name == "shoulders":
            return [[self.pose_landmarks_list.landmark[self.left_shoulder].x, self.pose_landmarks_list.landmark[self.left_shoulder].y],
                    [self.pose_landmarks_list.landmark[self.right_shoulder].x, self.pose_landmarks_list.landmark[self.right_shoulder].y]]
        elif name == "hips":
            return [[self.pose_landmarks_list.landmark[self.left_hip].x, self.pose_landmarks_list.landmark[self.left_hip].y],
                    [self.pose_landmarks_list.landmark[self.right_hip].x, self.pose_landmarks_list.landmark[self.right_hip].y]]
        elif name == "knees":
            return [[self.pose_landmarks_list.landmark[self.left_knee].x, self.pose_landmarks_list.landmark[self.left_knee].y],
                    [self.pose_landmarks_list.landmark[self.right_knee].x, self.pose_landmarks_list.landmark[self.right_knee].y]]
        else:
            raise ValueError("Unknown line name")
            #Funkcija za dobivanje koordinata linije definirane landmarkima. Prima ime linije (name) i vraća koordinate početne i završne točke te linije kao listu. Podržane linije su "shoulders" (ramena), "hips" (kukovi) i "knees" (koljena). Ako je ime linije nepoznato, funkcija baca ValueError.   

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

        #Ovu funkciju koristimo za izračunavanje kuta između dvije linije u 2D prostoru. Funkcija prima dvije linije definirane kao liste koordinata početne i završne točke.
        #Koristi VEKTORSKU matematiku za izračun kuta između linija
        #Naglasak na vektorsku jer se linije ne sijeku niti na jednoj tocki prikazanoj na slici
    
    def odstupanja(self, angle, threshold):
        if angle > threshold:
            print("Odstupanje detektirano! Kut: ", angle)
        else:
            print("Držanje je u redu. Kut: ", angle)
        #Funkcija za provjeru odstupanja kuta od određenog praga (threshold). Prima izračunati kut (angle) i prag (threshold), i vraća True ako je kut veći od praga, inače vraća False. Ova funkcija se koristi za detekciju lošeg držanja na temelju kuta između linija definiranih landmarkima. Ako je kut veći od praga, ispisuje poruku o detekciji odstupanja, inače ispisuje poruku da je držanje u redu.

    def drawing_landmarks_corectly(self, image):
        annotated_image = image.numpy_view().copy()
        #Ovo pretvara sliku u numpy array da bi se mogla iscrtavati, a zatim koristi MediaPipe drawing utilities za iscrtavanje landmarka na slici. Nakon iscrtavanja, vraća sliku s iscrtanim landmarkima. Ova funkcija je slična draw_landmarks, ali se koristi za iscrtavanje landmarka na slici. Prima sliku, pretvara je u numpy array, iscrtava landmarke koristeći MediaPipe drawing utilities, i vraća sliku s iscrtanim landmarkima.
        
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            self.pose_landmarks_list,
            solutions.pose.POSE_CONNECTIONS,
            costume_drawing_skin.get_default_pose_landmarks_style(),
            drawing_spec.DrawingGreen()
            )
        #Ovdje se koristi drugačiji stil iscrtavanja (DrawingGreen) kako bi se razlikovalo od funkcije draw_landmarks. Ova funkcija se koristi za iscrtavanje landmarka na slici, ali također uključuje logiku za detekciju lošeg držanja na temelju kuta između linija definiranih landmarkima. Ako je kut veći od određenog praga, određeni dijelovi tijela (ramena i koljena) će biti označeni kao loše držanje.
        #Crta zelenu boju za sve landmarke, ali ako se detektira loše držanje, određeni dijelovi tijela će biti označeni crvenom bojom (DrawingRed) u funkciji draw_landmarks. Ova funkcija se koristi za iscrtavanje landmarka na slici, ali također uključuje logiku za detekciju lošeg držanja na temelju kuta između linija definiranih landmarkima. Ako je kut veći od određenog praga, određeni dijelovi tijela (ramena i koljena) će biti označeni kao loše držanje.

        #Ovdje se koristi funkcija calculate_angle za izračunavanje kuta između linija definiranih landmarkima (ramena i kukovi, koljena i kukovi). Ako je kut veći od određenog praga, određeni dijelovi tijela će biti označeni kao loše držanje. Na kraju, funkcija vraća sliku s iscrtanim landmarkima i označenim dijelovima tijela koji imaju loše držanje.
        if Detective.__calculate_angle_2d(self, self.get_line("shoulders"), self.get_line("hips")) > self.shoulder_threshold:
            self.incorecrt_posture_shoulders = ([(11, 12)])
        else:
            self.incorecrt_posture_shoulders = ([(0, 0)])
            #Ako funkcija calculate_angle vrati kut veci od praga za ramena, onda se ti landmarki (11 i 12) oznace kao loše držanje, inace se oznace kao normalno (0, 0) sto znaci da se nece iscrtavati crvenom bojom.
            
        if Detective.__calculate_angle_2d(self, self.get_line("knees"), self.get_line("hips")) > self.knee_threshold:
            self.incorecrt_posture_knees = ([(23, 25), (24, 26)])
        else:
            self.incorecrt_posture_knees = ([(0, 0)])
            #Ako funkcija calculate_angle vrati kut veci od praga za koljena, onda se ti landmarki (23, 25 i 24, 26) oznace kao loše držanje, inace se oznace kao normalno (0, 0) sto znaci da se nece iscrtavati crvenom bojom.

        self.incorecrt_posture = self.incorecrt_posture_shoulders + self.incorecrt_posture_knees
        #Zbrajanje dvaju 'tupleova' koji sadrze indekse landmarka koji su oznaceni kao loše držanje, kako bi se dobila jedna lista svih landmarka koji su oznaceni kao loše držanje. Ova lista se koristi u funkciji draw_landmarks za iscrtavanje tih landmarka crvenom bojom (DrawingRed) kako bi se vizualno istaknuli dijelovi tijela koji imaju loše držanje.

        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            self.pose_landmarks_list,
            self.incorecrt_posture,
            costume_drawing_skin.get_default_pose_landmarks_style(),
            drawing_spec.DrawingRed()
            )
        #Ovdje se koristi funkcija draw_landmarks za iscrtavanje landmarka koji su označeni kao loše držanje (self.incorecrt_posture) crvenom bojom (DrawingRed) na slici. Ova funkcija se koristi za iscrtavanje landmarka na slici, ali također uključuje logiku za detekciju lošeg držanja na temelju kuta između linija definiranih landmarkima. Ako je kut veći od određenog praga, određeni dijelovi tijela (ramena i koljena) će biti označeni kao loše držanje.


        image = annotated_image 
        return image
        #Funkcija vraća sliku s iscrtanim landmarkima i označenim dijelovima tijela koji imaju loše držanje. Ova funkcija se koristi za iscrtavanje landmarka na slici, ali također uključuje logiku za detekciju lošeg držanja na temelju kuta između linija definiranih landmarkima. Ako je kut veći od određenog praga, određeni dijelovi tijela (ramena i koljena) će biti označeni kao loše držanje.