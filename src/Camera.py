from picamera2 import Picamera2, Preview
from time import sleep
from PIL import Image

class Camera:
    def __init__(self):
        print("Hello Camera!")

        self.picam = Picamera2()

        self.config = self.picam.create_preview_configuration()
        self.picam.configure(self.config)


    def on(self):
        print("camera on")
        self.picam.start()

    def preview(self, time):
        print("camera preview")
        self.picam.start_preview(Preview.QTGL)
        self.picam.start()
        sleep(time)
        self.picam.stop_preview()
        self.picam.stop()

    def off(self):
        print("camera off")
        self.picam.close()

    def capture_save(self):
        print("camera capture and save")
        camera_image = self.picam.capture_image().convert('RGB')
        camera_image.save("output.jpg")

    def capture_image(self):
        print("camera capture")
        return self.picam.capture_image().convert('RGB')