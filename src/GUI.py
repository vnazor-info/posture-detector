import tkinter.ttk as ttk
import ttkthemes
from src import lib
from tkinter import *
from tkinter import _default_root
import threading
import cv2
from time import sleep
import mediapipe as mp
from . import Camera
from . import Landmark
from PIL import Image, ImageTk

class GUI:
    def __init__(self):
        self.start_var = False
        self.save_image_var = False
        self.calculate_and_save_var = False
        self.toggle_button_state_var = False
        self.app_quit_var = False
        

    def setup(self):
        
        if not hasattr(self, "root"):
            self.root = Tk()
            self.root.call("source", "/home/infokab/Projects/posture-detector/resources/Azure-ttk-theme/azure.tcl")
            self.root.call("set_theme", "dark")

        button_start = ttk.Button(self.root, text="Start", width=7, command=lambda: [self.start_var_change_positive(), self.threading(lambda: lib.test(self))], style='Accent.TButton')
        button_stop = ttk.Button(self.root, text="Stop", width=7, command=self.start_var_change_negative, style='Accent.TButton')
        button_save = ttk.Button(self.root, text="Save Image", width=12, command=self.save_image_var, style='Accent.TButton')
        button_exit = ttk.Button(self.root, text="Exit", width=6, command=self.app_quit, style='Accent.TButton')
        button_calculate = ttk.Button(self.root, text="Calculate and save", width=18, command=self.calculate_and_save_var, style='Accent.TButton')
        button_color_toggle = ttk.Checkbutton(self.root, text='Toggle button', style='Toggle.TButton', command=self.toggle_button_state_var)

        button_start.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        button_stop.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        button_save.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        button_exit.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        button_calculate.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        button_color_toggle.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        self.root.mainloop()

    def start_var_change_positive(self):
        self.start_var = True
        return self.start_var

    def start_var_change_negative(self):
        self.start_var = False
        return self.start_var

    def save_image_var(self):
        self.save_image_var = True
        sleep(3)
        self.save_image_var = False
        return self.save_image_var

    def app_quit(self):
        self.app_quit_var = True
        cv2.destroyAllWindows()
        self.root.destroy()
        quit()

    def calculate_and_save_var(self):
        self.calculate_and_save_var = True
        sleep(0.1)
        self.calculate_and_save_var = False
        return self.calculate_and_save_var

    def toggle_button_state_var(self):
        self.toggle_button_state_var = not self.toggle_button_state_var
        return self.toggle_button_state_var

    def threading(self, target):
        
        print("starting thread")
        thread = threading.Thread(target=target)
        thread.start()