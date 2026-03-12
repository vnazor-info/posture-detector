from matplotlib import container
from src import config as cfg
from src import lib
import numpy as np
import cv2
import mediapipe as mp
from . import Detector
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components import containers
from mediapipe.framework.formats import landmark_pb2  
from mediapipe import solutions
import math
from time import sleep
from PIL import Image, ImageTk
from . import Camera
from . import Detector
from . import Landmark
import tkinter as tk
from tkinter import ttk
import ttkthemes
# _default_root can be accessed via tk._default_root if needed
import threading
from itertools import chain
from . import GUI

#Ovdje smo inportali potrebne biblioteke i module.
#Neke trenutno nisu u upotrebi, ali se koriste u drugim dijelovima projekta.
#
#Dolje navedene funkcije trenutacno nisu u uporabi ali smo ih koristili za testiranje i mozda ce biti korisne u buducnosti.
#

def angle_3_points(a, b, c):
#Tocak b je vrh kuta
  ang = math.degrees(
    math.atan2(c[1]-b[1], c[0]-b[0]) - 
    math.atan2(a[1]-b[1], a[0]-b[0])
)
  return ang + 360 if ang < 0 else ang

#Ovo je jedna od funkcija koje smo koristili za testiranje, ali trenutno nije u uporabi. Koristi se za izračunavanje kuta između tri točke, gdje je točka b vrh kuta.
#Slicna funkcija se nalazi u Landmark modulu, ali smo ovu zadržali jer nam je bila korisna za testiranje i možda će biti korisna u budućnosti.

def percent_difference(num1, num2):
  if (num1 + num2) == 0:
    return 0 # Both are zero
  return (abs(num2 - num1) / ((num1 + num2) / 2)) * 100

#Ovo je još jedna funkcija koju smo koristili za testiranje, ali trenutno nije u uporabi. Koristi se za izračunavanje postotne razlike između dva broja.

def camera_test():
  #picam = Picamera2()
  #
  #config = picam.create_preview_configuration()
  #picam.configure(config)
  # 
  #picam.start_preview(Preview.QTGL)
  #
  #picam.start()
  #sleep(2)
  #camera_image = picam.capture_image().convert('RGB')
  #picam.close()
  #camera_image.save("output.jpg")
  print("camerat test")

#Ovu funkciju smo koristili za testiranje kamere, ali trenutno nije u uporabi. Koristili smo Picamera2 biblioteku za pristup kameri i snimanje slike, ali smo je zamijenili našom vlastitom implementacijom kamere u Camera modulu.
#Vise ne koristimo Picamera2 jer želimo da naš projekt bude kompatibilan sa različitim platformama, a ne samo sa Raspberry Pi-jem.   

def camera_class_test():
  cam = Camera.Camera()
  cam.preview(5)
  cam.capture_save()
  #cam.off()
  #Ovu funkciju smo koristili za testiranje naše implementacije kamere u Camera modulu. Napravili smo instancu kamere, pokrenuli preview, snimili sliku i spremili je. Ova funkcija nam je pomogla da testiramo funkcionalnost naše kamere prije nego što smo je integrirali u naš glavni program.

  def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

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
    #Ovu funkciju smo koristili za testiranje vizualizacije detekcije. Uzeli smo RGB sliku i rezultat detekcije, te smo nacrtali landmarke na slici koristeći Mediapipe-ove funkcije za crtanje. Ova funkcija nam je pomogla da testiramo kako se landmarki prikazuju na slici prije nego što smo je integrirali u naš glavni program.
    #Ovu funkciju smo u cijelosti prebacili u Landmark modul, ali smo je zadržali ovdje jer nam je bila korisna za testiranje i možda će biti korisna u budućnosti.

def visualize(image,detection_result) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  #Ovo su vazni komentari koje smo ostavili u funkciji visualize, jer nam pomažu da razumijemo što funkcija radi i kako se koristi. Ova funkcija crta bounding boxove na ulaznoj slici na temelju rezultata detekcije, te vraća sliku s nacrtanim bounding boxovima. Ova funkcija nam je pomogla da testiramo vizualizaciju detekcije prije nego što smo je integrirali u naš glavni program.
  for detection in detection_result:
    # Crta bounding box
    bbox = detection.bounding_box
    start_point = (bbox.origin_x, bbox.origin_y)
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, cfg.TEXT_COLOR, 3)

    # Crta label and score
   # category = detection.categories[0]
   # category_name = category.category_name
   # probability = round(category.score, 2)
   # result_text = category_name + ' (' + str(probability) + ')'
   # text_location = (cfg.MARGIN + bbox.origin_x,
   #                  cfg.MARGIN + cfg.ROW_SIZE + bbox.origin_y)
   # cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
   #             cfg.FONT_SIZE, cfg.TEXT_COLOR, cfg.FONT_THICKNESS)

  return image
  #Ovu funkciju smo prebacili u Detector modul, ali smo je zadržali ovdje jer nam je bila korisna za testiranje i možda će biti korisna u budućnosti.
  #Ovu funkciju kao i funkciju u Detector modulu vise ne koristimo, jer smo se fokusirali na detekciju i vizualizaciju landmarka, a ne na detekciju objekata i crtanje bounding boxeva. Međutim, ove funkcije nam mogu biti korisne u budućnosti ako želimo proširiti funkcionalnost našeg programa.
  #Takoder crtanje bounding boxeva i labela znatno usporava rad programa, pa smo ih izbacili kako bismo poboljšali performanse.


def crop_image(img, origin_y, origin_x, height, width):
  crop_img = img[origin_y:origin_y+height+10, origin_x-10:origin_x+width]
  cv2.imwrite("cropped.jpg", crop_img)
  return(crop_img)
  #Ovu funkciju smo koristili za testiranje izrezivanja slike na temelju bounding boxa. Uzeli smo ulaznu sliku i koordinate bounding boxa, te smo izrezali odgovarajući dio slike i spremili ga kao novu sliku. Ova funkcija nam je pomogla da testiramo kako se slike izrezuju prije nego što smo je integrirali u naš glavni program.


def detector_showcase():
  detect = Detector.Detector(model_path='/home/infokab/Projects/posture-detector/resources/efficientdet_lite0.tflite')
  #Dodavanje varijable detector radi lakse inplementacije detektora iz Detector modula u funkciju.
  lap_cam = Camera.Camera()
  #Dodavanje varijable lap_cam radi lakse inplementacije kamere iz Camera modula u funkciju.

  while True:
    cv_image = lap_cam.capture_image()
    #otvara sliku pa detekta.
    #koristiti cv2 za open image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv_image
      )
    nested_detection_results = detect.detect(mp_image) 
    
    #Ispisuje rezultate detekcije na konzolu.
    #print("Nested detection results:", nested_detection_results)
    detected_image = visualize(cv_image, nested_detection_results)
    lap_cam.present_img(detected_image)
    
  cv2.imwrite("cropped_detection.jpg", detected_image)
#image_copy = np.copy(mp_image.numpy_view())
#annotated_image = visualize(image_copy, detection_result)
#rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
#cv2.imwrite("detection_result.jpg", rgb_annotated_image)
#colour_img= cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
#for detection in detections:
  #for category in detection.categories:
    #if category.category_name == "person":
      #print("nasao sam osobu")
    #else:
      #print("nema ljudi")


#if __name__ == "__main__":
  #print("Do some tests")

DESIRED_HEIGHT = 640

DESIRED_WIDTH = 480

RegionOfInterest = vision.InteractiveSegmenterRegionOfInterest
NormalizedKeypoint = containers.keypoint.NormalizedKeypoint

#Ovdje se nalaze varijable koje definiraju željene dimenzije slike za segmentaciju.
#

def resize_and_show(image):
  h, w = image.shape[:2]
  if h < w:
    img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
  else:
    img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
  cv2.imwrite("area.jpg",img)
  #Ovu funkciju smo koristili za testiranje prikaza slike nakon segmentacije. Funkcija mijenja veličinu slike na željene dimenzije i sprema je kao novu sliku. Ova funkcija nam je pomogla da testiramo kako se segmentirane slike prikazuju prije nego što smo je integrirali u naš glavni program.

def person_detect():
  #Stvara segmenter za osobu koristeći MediaPipe biblioteku.
  base_options = python.BaseOptions(model_asset_path='/home/infokab/Projects/posture-detector/resources/efficientdet_lite0.tflite')
  options = vision.ImageSegmenterOptions(base_options=base_options, output_category_mask=True)
  IMAGE_FILENAMES = ['/home/infokab/Projects/posture-detector/resources/man-standing.jpg']

  with vision.InteractiveSegmenter.create_from_options(options) as segmenter:
  
    for image_file_name in IMAGE_FILENAMES:
      BG_COLOR = (0, 0, 0) # gray
      MASK_COLOR = (255, 255, 255) # white
      images = {name: cv2.imread(name) for name in IMAGE_FILENAMES}

      image = mp.Image.create_from_file(image_file_name)

        # Dohvati maske za segmentiranu sliku.

      roi = RegionOfInterest(format=RegionOfInterest.Format.KEYPOINT,
                           keypoint=NormalizedKeypoint(DESIRED_HEIGHT/2, DESIRED_WIDTH/2))
      segmentation_result = segmenter.segment(image,roi)
      category_mask = segmentation_result.category_mask

      # Generiraj jednobojne slike za prikaz izlazne maske segmentacije.
      image_data = image.numpy_view()
      fg_image = np.zeros(image_data.shape, dtype=np.uint8)
      fg_image[:] = MASK_COLOR
      bg_image = np.zeros(image_data.shape, dtype=np.uint8)
      bg_image[:] = BG_COLOR

      condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.2
      output_image = np.where(condition, fg_image, bg_image)

      print(f'Segmentation mask of {image}:')
      resize_and_show(output_image)
      #Ispisuje segmentacijsku masku na konzolu i prikazuje segmentiranu sliku koristeći funkciju resize_and_show. Ova funkcija nam je pomogla da testiramo kako se segmentacija osobe izvodi prije nego što smo je integrirali u naš glavni program.


def stickfigure_videotest():
  stick_figure = Landmark.Landmark("resources/pose_landmarker_heavy.task")
  detect = Detector.Detector(cfg.MODEL_PATH)
  cam = Camera.Camera()
  #dodavanje varijabli stick_figure, detect i cam radi lakse inplementacije stick figure-a, detektora i kamere iz Landmark, Detector i Camera modula u funkciju.

  while True:
    cv_image = cam.capture_image()
    np_image = np.array(cv_image)
    whole_img = mp.Image(
      image_format=mp.ImageFormat.SRGB,
      data=np_image
    )
    #dobivanje slike s kamere i pretvaranje u format koji Mediapipe može koristiti.
    detect_result = detect.detect(whole_img)
    show_img=whole_img
    print("detect_result", detect_result)
    for result in detect_result:
      show_img = stick_figure.draw_landmark(person_crop=whole_img)
      if result.categories[0].category_name != "person":
        break
      cv2.imshow("landmarks", show_img)
    #popravljanje errora u kojem program prekida sa radom je ne postoji detektirana osoba. Ako detektor ne detektira osobu, program neće pokušavati crtati landmarke i neće prekidati sa radom. Također, ako se detektira osoba, prikazat će se slika s nacrtanim landmarkima.
    #
      right_shoulder = stick_figure.pose_landmarks_proto.landmark[12]
      left_hip = stick_figure.pose_landmarks_proto.landmark[23]
      right_hip = stick_figure.pose_landmarks_proto.landmark[24]
      left_knee = stick_figure.pose_landmarks_proto.landmark[25]
      right_knee = stick_figure.pose_landmarks_proto.landmark[26]
      right_elbow = stick_figure.pose_landmarks_proto.landmark[14]
      left_elbow = stick_figure.pose_landmarks_proto.landmark[13]
      left_shoulder = stick_figure.pose_landmarks_proto.landmark[11]
      dictionary = {
        "left_shoulder": (left_shoulder.x, left_shoulder.y),
        "right_shoulder": (right_shoulder.x, right_shoulder.y),  
        "left_hip": (left_hip.x, left_hip.y),
        "right_hip": (right_hip.x, right_hip.y),
        "left_knee": (left_knee.x, left_knee.y),
        "right_knee": (right_knee.x, right_knee.y),
        "left_elbow": (left_elbow.x, left_elbow.y),
        "right_elbow": (right_elbow.x, right_elbow.y),
      }

      left_arm = {
        "left_shoulder" : (left_shoulder.x, left_shoulder.y),
        "left_elbow": (left_elbow.x, left_elbow.y),
      }
      right_arm = {
        "right_shoulder": (right_shoulder.x, right_shoulder.y),
        "right_elbow": (right_elbow.x, right_elbow.y),
      }
      left_leg = {
        "left_hip": (left_hip.x, left_hip.y),
        "left_knee": (left_knee.x, left_knee.y),
      }
      right_leg = {
        "right_hip": (right_hip.x, right_hip.y),
        "right_knee": (right_knee.x, right_knee.y),
      }
      dict_parts = {
        "left_arm" : left_arm,
        "right_arm" : right_arm,
        "left_leg" : left_leg,
        "right_leg" : right_leg
      }
  
    if cv2.waitKey(1) == ord('p'):
      print("left_shoulder"), print (dictionary["left_shoulder"])
      print("right_shoulder"), print(dictionary["right_shoulder"])
      print("left_hip"), print(dictionary["left_hip"])
      print("right_hip"), print(dictionary["right_hip"])
      print("left_knee"), print(dictionary["left_knee"])
      print("right_knee"), print(dictionary["right_knee"])
      print("left_elbow"), print(dictionary["left_elbow"])
      print("right_elbow"), print(dictionary_parts["left_hand"])

    #
    #Dodavanje varijabli za posejdinu tocku na tijelu 
    #Implementacija rijecnika(dictionary) koji sadrzi koordinate svih bitnih tocki na tijelu, kao i rijecnika(dict_parts) koji sadrzi koordinate bitnih tocki za svaki dio tijela (ruke i noge).
    #




  

  # Racunanje kuta između lijevog ramena, lijevog lakta i desnog ramena. Lijevo rame je vrh kuta, a lijevi lakat i desno rame su krajnje točke kuta.
  # Koristimo funkciju angle_3_points za izračunavanje kuta između tri točke, gdje je lijevo rame vrh kuta, a lijevi lakat i desno rame su krajnje točke kuta.
  # Ovo je bila jedna faza testiranja koda                              
      p1 = (dict_parts["left_arm"]["left_elbow"])             
      p_center = (dict_parts["left_arm"]["left_shoulder"])
      p2 = (dict_parts["right_arm"]["right_shoulder"])
      final_angel = angle_3_points(p2, p_center, p1)
        

      if cv2.waitKey(1) == ord('q'):
        p1 = (dict_parts["left_arm"]["left_elbow"])
        p_center = (dict_parts["left_arm"]["left_shoulder"])
        p2 = (dict_parts["right_arm"]["right_elbow"])
        cv2.imwrite("final_landmarks.jpg", show_img)
        cv2.destroyAllWindows()
        break
        #Omogucavanje izlaza iz petlje pritiskom na tipku 'q' i spremanje slike s nacrtanim landmarkima kao "final_landmarks.jpg".

      if cv2.waitKey(1) == ord('a'):
        print(f"Angle: {angle_3_points(p2, p_center, p1):.2f} degrees") 
        print(f"Percent Difference: {percent_difference(90, final_angel):.2f}%")
        #Omogucavanje ispisa kuta i postotne razlike pritiskom na tipku 'a'.

#
#SAV KOD OVDJE JE KOD KOJI JE SLUZAO ZA TESTIRANJE RAZLICITIH DIJELOVA PROJEKTA
#ODAVDE POCINJE DIO KODA KOJI SE TRENUTMNO KORISTI U PROJEKTU
#
#

break_var = 1
save_var = 0
racunanje_var = 0
postotak = 0.0
postotak2 = 0.0
kut = 0.0
switch_state = False

#Dodavanje globalnih varijabli koje se koriste za kontrolu toka programa i spremanje rezultata izračuna.

#root = tk.Tk()
#Create a style
#root.call("source", "/home/infokab/Projects/posture-detector/resources/Azure-ttk-theme/azure.tcl")
#root.call("set_theme", "dark")
def tktinker_test():

  global postotak
  print("tkinter test")
  global root
  #Pokretanje glavnog prozora i postavljanje naslova.

  #Postavljanje naslova glavnog prozora.
  label =  ttk.Label(root, text="Posture Detector", style='Card.TFrame')
  label.pack(pady=10)

  #Dodavanje gumba i njihovih funkcija.
  button = ttk.Button(root, text="Start", width=7, command=thread, style='Accent.TButton')
  button1 = ttk.Button(root, text="Stop", width=6, command=close_window, style='Accent.TButton')
  button2 = ttk.Button(root, text="Save Image", width=12, command=save_image, style='Accent.TButton')
  button3 = ttk.Button(root, text="Exit", width=6, command=root_quit, style='Accent.TButton')
  button4 = ttk.Button(root, text="Calculate and save", width=18, command=calculate_and_save, style='Accent.TButton')
  toggle_button = ttk.Checkbutton(root, text='Toggle button', style='Toggle.TButton', command=toggle_button_state)
  #Dodavanje uputa za korisnika.
  l = ttk.Label(root, text = "Program pokrecete pritiskom na Start\nZaustavljate pritiskom na Stop\nSpremate sliku pritiskom na Save Image\nIzlaz iz programa pritiskom na Exit",style='Accent.TButton')
  l1 = ttk.Label(root, text = "Kako bi program radio najbolje, preporučuje se da se nalazite na udaljenosti od kamere od 1.5 do 2 metra\nTakođer, preporučuje se da se nalazite u dobro osvijetljenoj prostoriji\nZa najbolje rezultate, preporučuje se da se nalazite ispred kamere, a ne sa strane",style='Accent.TButton')


  #Dodavanje tekstovnih elemenata na glavni prozor.
  l.pack()
  l1.pack()

  #Dodavanje gumba na glavni prozor.
  button.pack(anchor=tk.W, pady=5)
  button1.pack(anchor=tk.W, pady=5)
  button2.pack(anchor=tk.W, pady=5)
  button3.pack(anchor=tk.W, pady=5)     
  button4.pack(anchor=tk.W, pady=5)
  toggle_button.pack(anchor=tk.W, pady=5)
  #Pokretanje glavne petlje prozora.
  root.mainloop()

#
#Funkcije za rukovanje gumbima u Tkinter sučelju.
#

def root_quit():
  print("exit")
  global break_var
  break_var = 0
  root.quit()
  #Funkcija za izlaz iz programa. Poziva se kada korisnik pritisne gumb "Exit" u Tkinter sučelju.

def thread():
  t = threading.Thread(target=start_window)
  t.start()
  #Pokretanje funkcije start_window u zasebnoj niti kako bi se izbjeglo blokiranje glavnog Tkinter sučelja.

def start_window():
  print("start window")
  global break_var
  break_var = 1
  #Postavljanje varijable break_var na 1 kako bi se pokrenula glavna petlja u funkciji playground.
  playground()
  #Pokretanje glavne petlje za obradu slike i detekciju položaja tijela.

def close_window():
  print("close window")
  global break_var
  break_var = 0
  #Postavljanje varijable break_var na 0 kako bi se zaustavila glavna petlja u funkciji playground.
    
def save_image():  
  sleep(3)
  #Pauza od 3 sekunde prije spremanja slike.
  print("save image")
  global save_var
  save_var = 1
  #Postavljanje varijable save_var na 1 kako bi se spremila trenutna slika u funkciji playground.

def calculate_and_save():
  global racunanje_var
  racunanje_var = 1
  #Postavljanje varijable racunanje_var na 1 kako bi se izračunali kutovi u funkciji playground.

def toggle_button_state():
  global switch_state
  switch_state = True
  print("toggle button")
  #Ova funkcija se poziva kada korisnik klikne na toggle gumb. Trenutno samo ispisuje poruku na konzolu, ali se može proširiti da mijenja stanje nekih funkcionalnosti u programu.

def playground():
  #code for testing new stuff
  global break_var
  global save_var
  global racunanje_var
  global postotak
  global postotak2
  global kut
  global root
  #Dodavanje globalnih varijabli koje se koriste unutar funkcije.

  T = ttk.Label(root, style='Accent.TButton', width=50, text=f"Kut: {postotak:.2f} degrees")
  T.pack()
  T1 = ttk.Label(root, style='Accent.TButton', width=50, text=f"Kut Koljena: {postotak2:.2f}%")
  T1.pack()
  #Dodavanje tekstovnih elemenata na glavni prozor za prikaz izračunatih kutova.

  lap_cam = Camera.Camera()
  detect = Landmark.Detective()
  #Dodavanje varijabli lap_cam i detect radi lakse inplementacije kamere iz Camera modula i detektora iz Landmark modula u funkciju.
  #Ulazimo u glavnu petlju koja će se vrtjeti dok god je varijabla break_var postavljena na 1.
  while True:
    
    still_image = lap_cam.capture_image()
    #Dobivanje slike s kamere.

    whole_img = mp.Image(
      image_format=mp.ImageFormat.SRGB,
      data=still_image
    )
    #Pretvaranje slike u format koji Mediapipe može koristiti.
  
    if detect.person_detected(whole_img):
      landmark_img = detect.drawing_landmarks(whole_img)
      #Provjera je li osoba detektirana na slici. Ako jest, crtaju se landmarki na slici.
    
    lap_cam.present_img(landmark_img)
    #Prikaz slike s nacrtanim landmarkima.

    if break_var == 0:
      print("breaking loop")
      cv2.destroyAllWindows()
      #Ako je varijabla break_var postavljena na 0, izlazimo iz petlje i zatvaramo sva OpenCV prozore.
      break
      #Omogućavanje izlaza iz petlje kada korisnik pritisne gumb "Stop" u Tkinter sučelju.

    if save_var == 1:
      cv2.imwrite("landmark_image.jpg", landmark_img)
      #Spremanje trenutne slike s landmarkima kao "landmark_image.jpg".
      print("image saved")
      save_var = 0
      #Ako je varijabla save_var postavljena na 1, spremamo trenutnu sliku s landmarkima kao "landmark_image.jpg" i resetiramo varijablu save_var na 0.

    if racunanje_var == 1:
      sleep(3)
      kut1 = detect.calculate_angle("shoulders", "hips")
      kut2 = detect.calculate_angle("hips", "knees")
      detect.odstupanja(kut1, 5)
      detect.odstupanja(kut2, 5)
      #Definiranje varijabli kut1 i kut2 koje se izračunavaju pomoću funkcije calculate_angle iz Landmark modula. Kut1 predstavlja kut između ramena i kukova, a kut2 predstavlja kut između kukova i koljena.

      postotak = kut1
      postotak2 = kut2
      #Postavljanje varijabli postotak i postotak2 na izračunate kutove kako bi se mogli prikazati u Tkinter sučelju.

      racunanje_var = 0
      #Ako je varijabla racunanje_var postavljena na 1, izračunavamo kutove, postavljamo ih u varijable postotak i postotak2, te resetiramo varijablu racunanje_var na 0.

      T.config(text=f"Kut: {postotak:.2f} degrees")
      T1.config(text=f"Kut Koljena: {postotak2:.2f} degrees")
      #Ažuriranje tekstovnih elemenata u Tkinter sučelju s izračunatim kutovima.
  T.destroy()
  T1.destroy()
  #Nakon izlaska iz petlje, uništavamo tekstovne elemente u Tkinter sučelju.

def GUI_test():
  gui = GUI.GUI()
  gui.GUI_start()
  #Ova funkcija se koristi za testiranje Tkinter sučelja. Stvara instancu klase GUI i poziva metodu setup koja postavlja sučelje i pokreće glavnu petlju. Ova funkcija nam je pomogla da testiramo funkcionalnost našeg Tkinter sučelja prije nego što smo ga integrirali u naš glavni program.

def test(gui):
    print("test")

    lap_cam = Camera.Camera()
    detect = Landmark.Detective()

    while True:
        if not gui.start_var or gui.app_quit_var: 
            sleep(0.1)
            gui.image_output.configure(image="")
            if gui.save_image_var:
                print("image cannot be saved because the program is not running")
                gui.save_image_var = False
            continue
          
        print("looping")

        still_image = lap_cam.capture_image()

        whole_img = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=still_image
        )

        detect.person_detected(whole_img)

        if not gui.draw_var:
          landmark_img = detect.drawing_all_landmarks(whole_img)
          #lap_cam.present_img(landmark_img)

          b,g,r = cv2.split(landmark_img)
          img = cv2.merge((r,g,b))

          im = Image.fromarray(img)
          imgtk = ImageTk.PhotoImage(image=im) 

          gui.image_output.configure(image=imgtk)
          gui.image_output.image = imgtk
      
        elif gui.draw_var:
          landmark_img = detect.drawing_landmarks_corectly(whole_img)

          b,g,r = cv2.split(landmark_img)
          img = cv2.merge((r,g,b))

          im = Image.fromarray(img)
          imgtk = ImageTk.PhotoImage(image=im) 

          gui.image_output.configure(image=imgtk)
          gui.image_output.image = imgtk 

        if gui.save_image_var:
            cv2.imwrite("landmark_image.jpg", landmark_img)
            print("image saved")
            gui.save_image_var = False
            continue

        if gui.calculate_and_save_var:
            kut1 = detect.calculate_angle("shoulders", "hips")
            kut2 = detect.calculate_angle("hips", "knees")
            detect.odstupanja(kut1, 5)
            detect.odstupanja(kut2, 5)

            postotak = kut1
            postotak2 = kut2

            gui.calculate_and_save_var = False
            continue
        