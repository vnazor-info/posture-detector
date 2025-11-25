from time import sleep
from PIL import Image
import cv2 as cv2

class Camera:
    def __init__(self):
        print("Hello Camera!")
        
        #self.picam = Picamera2()

        #self.config = self.picam.create_preview_configuration()
        #self.picam.configure(self.config)
        self.cam = cv2.VideoCapture(0)
        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter('output.mp4', self.fourcc, 30, (self.frame_width, self.frame_height))
        


    def on(self):
        print("camera on")
        #self.picam.start()#
        #Define the codec and create VideoWriter object
        

    def preview(self, time):

        record = False
    
        while True:
            print("camera preview")

            ret, frame = self.cam.read()

            if record == True:
                self.out.write(frame)
            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) == ord('s'):
                record = not record
            #self.picam.start_preview(Preview.QTGL)
            #self.picam.start()
            #sleep(time)
            #self.picam.stop_preview()
            #self.picam.stop()
            if cv2.waitKey(1) == ord('q'):
                break

    def off(self):
        print("camera off")
        #self.picam.close()

    def capture_save(self):
        print("camera capture and save")
        #camera_image = self.picam.capture_image().convert('RGB')
        #camera_image.save("output.jpg")
        
    def capture_image(self):
        print("camera capture")
        #return self.picam.capture_image().convert('RGB')