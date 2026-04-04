import tkinter.ttk as ttk
import ttkthemes
from src import lib
import tkinter as tk
from tkinter import _default_root
import threading
from time import sleep
import os
import cv2
from src.config import get_resource_path

#
#Ovdje smo importali potrebne biblioteke: tkinter za GUI, ttkthemes za teme, threading za višestruko izvršavanje funkcija, time za upravljanje vremenom, os za rad s operativnim sistemom i cv2 za rad s kamerom.
#

class GUI:
    def __init__(self):
        self.start_var = False
        self.save_image_var = False
        self.calculate_var = False
        self.draw_var = False
        self.app_quit_var = False 
        self.avaiable = []
        self.max_cameras = 10  
        #Inicijalizacija varijabli koje se koriste za upravljanje stanjem aplikacije, kao što su start_var, save_image_var, calculate_var, draw_var i app_quit_var. Također se inicijalizira lista avaiable za pohranu dostupnih kamera i max_cameras koja određuje maksimalni broj kamera koje će se provjeravati.  
        self.camera_checker()   
        #Pozivanje funkcije camera_checker koja provjerava dostupne kamere i popunjava listu avaiable s njihovim indeksima.

    def gui_setup(self):
        
        self.start_button = ttk.Checkbutton(
            self.root, text="Start", style="TButton", command=lambda: [self.start_var_change_positive(), self.threading(lambda: lib.test(self))], width=15
        )
        self.start_button.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        #Postavljanje start buttona koji koristi ttk.Checkbutton. Kada se klikne, poziva se funkcija start_var_change_positive koja postavlja start_var na True, a zatim pokreće funkciju lib.test u zasebnoj niti. Button je smješten u grid layoutu na poziciji (0, 0) s određenim paddingom i poravnanjem.

        self.button_stop = ttk.Button(
            self.root, text="Stop", style='TButton', command=self.start_var_change_negative, width=15
        )
        self.button_stop.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        #Postavljanje stop buttona koji koristi ttk.Button. Kada se klikne, poziva se funkcija start_var_change_negative koja postavlja start_var na False. Button je smješten u grid layoutu na poziciji (1, 0) s određenim paddingom i poravnanjem.

        self.button_save = ttk.Button(
            self.root,  text="Save Image", style='TButton', command=lambda: [self.save_image_var_change()], width=15
        )
        self.button_save.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        #Postavljanje save image buttona koji koristi ttk.Button. Kada se klikne, poziva se funkcija save_image_var_change koja postavlja save_image_var na True. Button je smješten u grid layoutu na poziciji (2, 0) s određenim paddingom i poravnanjem.

        self.button_exit = ttk.Button(
            self.root, text="Exit", style='TButton', command=self.app_quit, width=15
        )
        self.button_exit.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        #Postavljanje exit buttona koji koristi ttk.Button. Kada se klikne, poziva se funkcija app_quit koja postavlja app_quit_var na True, zatim zatvara sve OpenCV prozore, uništava glavni prozor GUI-a i izlazi iz aplikacije. Button je smješten u grid layoutu na poziciji (3, 0) s određenim paddingom i poravnanjem.
        
        self.button_calculate = ttk.Button(
            self.root, text="Calculate", style='TButton', command=self.calculate_var_change, width=15
        )
        self.button_calculate.grid(row=4, column=0, pady=5, padx=5, sticky="w")
        #Postavljanje calculate buttona koji koristi ttk.Button. Kada se klikne, poziva se funkcija calculate_var_change koja postavlja calculate_var na True. Button je smješten u grid layoutu na poziciji (4, 0) s određenim paddingom i poravnanjem.

        self.button_color_toggle = ttk.Checkbutton(
            self.root, text='Toggle Color', style='TRadiobutton', command=self.draw_var_change, width=15
        )
        self.button_color_toggle.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        #Postavljanje color toggle buttona koji koristi ttk.Checkbutton. Kada se klikne, poziva se funkcija draw_var_change koja mijenja vrijednost draw_var između True i False. Button je smješten u grid layoutu na poziciji (5, 0) s određenim paddingom i poravnanjem.

        self.image_output = ttk.Label(self.root)
        self.image_output.grid(sticky="e", row=7, column=0, padx=5, pady=5)
        #Postavljanje labela za prikaz slike koji koristi ttk.Label. Label je smješten u grid layoutu na poziciji (7, 0) s određenim paddingom i poravnanjem.  
        
        self.tutorial_label = ttk.Label(self.root, text="Dobrodosli u nas program, za pokretanje programa odaberite kameru, te pritisnite gumb Start.", style='TLabel', wraplength=300, justify="center")
        self.tutorial_label.place(relx=0.5, rely=0.03, anchor="center")
        #Postavljanje tutorial labela koji koristi ttk.Label. Label sadrži tekst dobrodošlice i uputa za pokretanje programa. Koristi se wraplength za ograničavanje širine teksta i justify za centriranje teksta. Label je postavljen na sredinu prozora koristeći place metodu s relx, rely i anchor parametrima.

        self.shoulder_angle = ttk.Label(self.root, text="Shoulder angle: ", style='TLabel', wraplength=300, justify="center")
        self.shoulder_angle.place(relx=0.5, rely=0.1, anchor="center")
        #Postavljanje shoulder angle labela koji koristi ttk.Label. Label sadrži tekst "Shoulder angle: " i koristi se wraplength za ograničavanje širine teksta i justify za centriranje teksta. Label je postavljen na sredinu prozora koristeći place metodu s relx, rely i anchor parametrima.

        self.knee_angle = ttk.Label(self.root, text="Knee angle: ", style='TLabel', wraplength=300, justify="center")
        self.knee_angle.place(relx=0.5, rely=0.15, anchor="center")
        #Postavljanje knee angle labela koji koristi ttk.Label. Label sadrži tekst "Knee angle: " i koristi se wraplength za ograničavanje širine teksta i justify za centriranje teksta. Label je postavljen na sredinu prozora koristeći place metodu s relx, rely i anchor parametrima.

        self.widgets_frame = ttk.Frame(self.root, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=6, column=0, pady=5, padx=5, sticky="w"
        )
        #Postavljanje framea za dodatne widgete koji koristi ttk.Frame. Frame je smješten u grid layoutu na poziciji (6, 0) s određenim paddingom i poravnanjem. Ovaj frame će se koristiti za smještaj menubuttona za odabir kamera.

        # Postavljanje menubuttona za odabir kamera. Koristi ttk.Menubutton koji je povezan s tk.Menu. Menu se popunjava komandama koje predstavljaju dostupne kamere, a svaka komanda poziva funkciju select_camera s odgovarajućim indeksom kamere kada se odabere. Menubutton je smješten u grid layoutu unutar widgets_frame na poziciji (0, 0) s određenim paddingom i poravnanjem.
        self.menu = tk.Menu(self.root)
        
        self.menubutton = ttk.Menubutton(
            self.widgets_frame, text="Cameras", menu=self.menu, direction="below"
        )
        self.menubutton.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        #Popunjavanje menija s dostupnim kamerama. Za svaku dostupnu kameru, dodaje se komanda u menu s tekstom "Camera {i+1}" i funkcijom koja poziva select_camera s odgovarajućim indeksom kamere.   
        for i in range(len(self.avaiable)):
            self.menu.add_command(label=f"    Camera {i+1}    ", command=lambda index=self.avaiable[i]: self.select_camera(index))

    def start_var_change_positive(self):
        self.start_var = True
        return self.start_var
        #Funkcija koja postavlja start_var na True i vraća tu vrijednost. Ova funkcija se poziva kada se klikne na Start button, što signalizira da je aplikacija spremna za pokretanje glavne funkcionalnosti, kao što je prikaz kamere i obrada slike.

    def start_var_change_negative(self):
        self.start_var = False
        sleep(0.1)
        return self.start_var
        #Funkcija koja postavlja start_var na False, zatim pauzira izvršavanje na 0.1 sekundu i vraća tu vrijednost. Ova funkcija se poziva kada se klikne na Stop button, što signalizira da aplikacija treba zaustaviti glavnu funkcionalnost, kao što je prikaz kamere i obrada slike.

    def save_image_var_change(self):
        self.save_image_var = True
        return self.save_image_var
        #Funkcija koja postavlja save_image_var na True i vraća tu vrijednost. Ova funkcija se poziva kada se klikne na Save Image button, što signalizira da aplikacija treba spremiti trenutnu sliku s kamere.

    def app_quit(self):
        self.app_quit_var = True
        cv2.destroyAllWindows()
        self.root.destroy()
        os._exit(0)
        #Funkcija koja postavlja app_quit_var na True, zatim zatvara sve OpenCV prozore, uništava glavni prozor GUI-a i izlazi iz aplikacije. Ova funkcija se poziva kada se klikne na Exit button, što signalizira da korisnik želi zatvoriti aplikaciju.

    def calculate_var_change(self):
        self.calculate_var = True
        return self.calculate_var
        #Funkcija koja postavlja calculate_var na True i vraća tu vrijednost. Ova funkcija se poziva kada se klikne na Calculate button, što signalizira da aplikacija treba izvršiti neku vrstu izračuna, kao što je analiza slike ili izračun kuteva.

    def draw_var_change(self):
        self.draw_var = not self.draw_var
        return self.draw_var
        #Funkcija koja mijenja vrijednost draw_var između True i False, a zatim vraća tu vrijednost. Ova funkcija se poziva kada se klikne na Toggle Color button, što signalizira da aplikacija treba promijeniti način prikaza slike, na primjer, između obojenog i crno-bijelog prikaza.

    def threading(self, target):
        
        print("starting thread")
        thread = threading.Thread(target=target)
        thread.start()
        #Funkcija koja prima funkciju target kao argument, zatim kreira i pokreće novu nit koja izvršava tu funkciju. Ova funkcija se koristi za pokretanje funkcija koje mogu biti dugotrajne ili zahtjevne za resurse, poput prikaza kamere ili obrade slike, bez blokiranja glavnog GUI thread-a.

    def select_camera(self, index):
        print(f"Selected camera index: {index}")
        self.cam_index_input = index
        return self.cam_index_input
        #Funkcija koja prima indeks kamere kao argument, ispisuje odabrani indeks na konzolu, postavlja cam_index_input na taj indeks i vraća tu vrijednost. Ova funkcija se poziva kada korisnik

    def camera_checker(self):
        print(f"OpenCV version: {cv2.__version__}")
        
        for i in range(self.max_cameras):
            #ponavlja petlju od 0 do max_cameras (10) kako bi provjerila dostupnost kamera. Za svaki indeks kamere, pokušava se otvoriti kamera koristeći cv2.VideoCapture(i). Ako čitanje okvira s kamere nije uspješno, ispisuje se poruka da kamera nije pronađena i nastavlja se na sljedeći indeks. Ako je kamera dostupna, njen indeks se dodaje u listu avaiable, kamera se zatvara i ispisuje se poruka da je kamera OK. Nakon provjere svih indeksa, ispisuje se lista pronađenih kamera.  
            cap = cv2.VideoCapture(i)
            
            if not cap.read()[0]:
                print(f"Camera index {i:02d} not found...")
                continue
            
            self.avaiable.append(i)
            cap.release()
            #Ako je kamera dostupna, njen indeks se dodaje u listu avaiable, kamera se zatvara i ispisuje se poruka da je kamera OK. Nakon provjere svih indeksa, ispisuje se lista pronađenih kamera.
            
            print(f"Camera index {i:02d} OK!")

        print(f"Cameras found: {self.avaiable}")

    def GUI_start(self):
        self.root = tk.Tk()
        self.root.title("")
        #Inicijalizacija glavnog prozora GUI-a koristeći tk.Tk() i postavljanje naslova prozora na prazan string. Ova funkcija se poziva za pokretanje GUI-a, gdje se kreira glavni prozor, postavlja tema, postavljaju elementi GUI-a i pokreće glavna petlja za prikaz prozora i interakciju s korisnikom.

        # Postavljanje teme
        self.root.call("source", get_resource_path("resources/Azure-ttk-theme/azure.tcl"))
        self.root.call("set_theme", "dark")
        # Pokrece GUI i postavlja elemente te ih ponavlja u integriranoj petlji
        self.gui_setup()
        self.root.mainloop()