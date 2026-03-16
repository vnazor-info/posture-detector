from time import sleep
from PIL import Image
import cv2 as cv2
from src import lib
#Ovdje smo importali potrebne biblioteke: time za upravljanje vremenom, PIL za rad s slikama i cv2 za rad s kamerom i video zapisima.

#
#Napomenna: Neke od navedenih klasi se ne koriste u ovom kodu, ali su možda planirane za buduću upotrebu ili su ostaci iz prethodnih verzija koda. Zato nisu izbrisane. Iako nisu korištene, njihova prisutnost ne utječe na funkcionalnost trenutnog koda.
#
class Camera:
    def __init__(self):
        print("Hello Camera!")
        
        #self.picam = Picamera2()
        #self.config = self.picam.create_preview_configuration()
        #self.picam.configure(self.config)

#Par linija koda iznad je izkomentirano jer se odnosi na Picamera2 biblioteku koja je specifična za Raspberry Pi kamere. Umjesto toga, koristi se OpenCV za rad s kamerom.

        self.win_name = "Test suite"
        #Imenovanje prozora za prikaz kamere.
        self.cam_index = int(lib.cam_index_input)
        #Indeks kamere koji se koristi za inicijalizaciju. Obično 0
        self.cam = cv2.VideoCapture(self.cam_index)
        print(self.cam_index)
        #Inicijalizacija kamere pomoću OpenCV-a.

        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #Dobivanje širine i visine okvira kamere.
        #Postavljanje kodeka i stvaranje objekta VideoWriter za snimanje videa.
        
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter('output.mp4', self.fourcc, 30, (self.frame_width, self.frame_height))
        #Postavljanje kodeka na 'mp4v' za MP4 format, stvaranje VideoWriter objekta s nazivom datoteke 'output.mp4', brzinom od 30 fps i dimenzijama okvira kamere.

        print(self.frame_width, self.frame_height)
        #Ispisivanje dimenzija okvira kamere na konzolu.
        

    def on(self):
        print("camera on")
        #self.picam.start()#
        #Define the codec and create VideoWriter object

        #Funkcija za uključivanje kamere. U ovom slučaju, samo ispisuje poruku na konzolu. Linija koda za pokretanje Picamera2 je izkomentirana jer se koristi OpenCV.
        #Trenutmo ne postoji funkcionalnost za uključivanje kamere jer je kamera već inicijalizirana u konstruktoru klase.
        

    def preview(self, time):

        record = False
        #Postavljanje varijable record na False, što znači da se trenutno ne snima video.
    
        while True:
            print("camera preview")

            ret, frame = self.cam.read()
            #Čitanje okvira s kamere. ret je boolean vrijednost koja označava je li čitanje bilo uspješno, a frame je sam okvir slike.

            if record == True:
                #Ako je varijabla record postavljena na True, zapisujemo trenutni okvir u video datoteku.
                self.out.write(frame)
            cv2.imshow('Camera', frame)
            #Prikazivanje okvira u prozoru nazvanom 'Camera'.

            if cv2.waitKey(10) == ord('s'):
                record = not record
            #self.picam.start_preview(Preview.QTGL)
            #self.picam.start()
            #sleep(time)
            #self.picam.stop_preview()
            #self.picam.stop()

    #Par linija koda iznad je izkomentirano jer se odnosi na Picamera2 biblioteku koja je specifična za Raspberry Pi kamere. Umjesto toga, koristi se OpenCV za rad s kamerom i video zapisima.
            
            elif cv2.waitKey(10) == ord('q'):
                cv2.destroyWindow("Camera")
                break
                #Ako je pritisnuto slovo 'q', zatvaramo prozor kamere i izlazimo iz petlje.
                   


    def off(self):
        print("camera off")
        #self.picam.close()
        #Funkcija za isključivanje kamere. U ovom slučaju, samo ispisuje poruku na konzolu. Linija koda za zatvaranje Picamera2 je izkomentirana jer se koristi OpenCV.

    def capture_save(self):
        ret, frame = self.cam.read()
        #Čitanje okvira s kamere za snimanje slike.

        if ret:
            cv2.imshow("Captured", frame)         
            cv2.imwrite("captured_image.png", frame)  
            cv2.waitKey(1)                      
            cv2.destroyWindow("Captured")     
            #Ako je čitanje okvira bilo uspješno, prikazujemo okvir u prozoru nazvanom "Captured", spremamo ga kao "captured_image.png", čekamo na pritisak tipke i zatvaramo prozor.

        else:
            print("Failed to capture image.")
            #Ako čitanje okvira nije bilo uspješno, ispisujemo poruku o pogrešci na konzolu.

        self.cam.release() 
        print("camera capture and save")
        #camera_image = self.picam.capture_image().convert('RGB')
        #camera_image.save("output.jpg")

    #Linije koda iznad su izkomentirane jer se odnose na Picamera2 biblioteku koja je specifična za Raspberry Pi kamere. Umjesto toga, koristi se OpenCV za rad s kamerom i spremanje slike.
        
        #
        #Linije koda ispod se koriste u trenutnom kodu za hvatanje i spremanje slike s kamere koristeći OpenCV.
        #
    
    def capture_image(self):
        ret, frame = self.cam.read()
        #Čitanje okvira s kamere za hvatanje slike.

        #return self.picam.capture_image().convert('RGB')

        return frame
        #Funkcija za hvatanje slike s kamere. Vraća trenutni okvir kao sliku.

    def open_window(self):
        cv2.namedWindow(self.win_name, cv2.WINDOW_AUTOSIZE)
        #Funkcija za otvaranje prozora s imenom definiranom u konstruktoru klase. Prozor je postavljen na automatsko prilagođavanje veličine.

    def present_img(self, image):
        cv2.imshow("Presented Image", image)
        #Funkcija za prikaz slike u prozoru nazvanom "Presented Image".

        if cv2.waitKey(10) == ord('q'):
            cv2.destroyWindow("Presented Image")
            #Ako je pritisnuto slovo 'q', zatvaramo prozor s prikazanom slikom.