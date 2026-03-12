import tkinter.ttk as ttk
import ttkthemes
from src import lib
import tkinter as tk
from tkinter import _default_root
import threading
from time import sleep
import os
import cv2

class GUI:
    def __init__(self):
        self.start_var = False
        self.save_image_var = False
        self.calculate_and_save_var = False
        self.draw_var = False
        self.app_quit_var = False        

    def gui_setup(self):
        
        self.start_button = ttk.Checkbutton(
            self.root, text="Start", style="TButton", command=lambda: [self.start_var_change_positive(), self.threading(lambda: lib.test(self))], width=15
        )
        self.button_stop = ttk.Button(
            self.root, text="Stop", style='TButton', command=self.start_var_change_negative, width=15
        )

        self.button_save = ttk.Button(
            self.root,  text="Save Image", style='TButton', command=lambda: [self.save_image_var_change()], width=15
        )

        self.button_exit = ttk.Button(
            self.root, text="Exit", style='TButton', command=self.app_quit, width=15
        )

        self.button_calculate = ttk.Button(
            self.root, text="Calculate and save", style='TButton', command=self.calculate_and_save_var_change, width=15
        )

        self.button_color_toggle = ttk.Checkbutton(
            self.root, text='Toggle Color', style='TRadiobutton', command=self.draw_var_change, width=15
        )

        self.image_output = ttk.Label(self.root)

        self.tutorial_label = ttk.Label(self.root, text="Welcome to the posture detector! Please click the start button to begin.", style='TLabel', wraplength=300, justify="center")
        
        self.tutorial_label.place(relx=0.5, rely=0.03, anchor="center")

        self.image_output.grid(sticky="e", row=7, column=0, padx=5, pady=5)

        self.start_button.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        self.button_stop.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        
        self.button_save.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        
        self.button_exit.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        
        self.button_calculate.grid(row=4, column=0, pady=5, padx=5, sticky="w")
        
        self.button_color_toggle.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    def start_var_change_positive(self):
        self.start_var = True
        return self.start_var

    def start_var_change_negative(self):
        self.start_var = False
        sleep(0.1)
        return self.start_var

    def save_image_var_change(self):
        sleep(3)
        self.save_image_var = True
        return self.save_image_var

    def app_quit(self):
        self.app_quit_var = True
        cv2.destroyAllWindows()
        self.root.destroy()
        os._exit(0)

    def calculate_and_save_var_change(self):
        sleep(3)
        self.calculate_and_save_var = True
        return self.calculate_and_save_var

    def draw_var_change(self):
        self.draw_var = not self.draw_var
        return self.draw_var

    def threading(self, target):
        
        print("starting thread")
        thread = threading.Thread(target=target)
        thread.start()

    def GUI_start(self):
        self.root = tk.Tk()
        self.root.title("")

        # Simply set the theme
        self.root.call("source", "/home/infokab/Projects/posture-detector/resources/Azure-ttk-theme/azure.tcl")
        self.root.call("set_theme", "dark")
        self.gui_setup()
        self.root.mainloop()