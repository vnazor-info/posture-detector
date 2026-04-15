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
        self.available = []
        self.last_cameras = []
        self.max_cameras = 10  
        self.cam_index_input = 0
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
            self.root,  text="Spremi sliku", style='TButton', command=lambda: [self.save_image_var_change()], width=15
        )
        self.button_save.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        #Postavljanje save image buttona koji koristi ttk.Button. Kada se klikne, poziva se funkcija save_image_var_change koja postavlja save_image_var na True. Button je smješten u grid layoutu na poziciji (2, 0) s određenim paddingom i poravnanjem.

        self.button_exit = ttk.Button(
            self.root, text="Izlaz", style='TButton', command=self.app_quit, width=15
        )
        self.button_exit.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        #Postavljanje exit buttona koji koristi ttk.Button. Kada se klikne, poziva se funkcija app_quit koja postavlja app_quit_var na True, zatim zatvara sve OpenCV prozore, uništava glavni prozor GUI-a i izlazi iz aplikacije. Button je smješten u grid layoutu na poziciji (3, 0) s određenim paddingom i poravnanjem.
        
        self.button_calculate = ttk.Button(
            self.root, text="Izračunaj", style='TButton', command=self.calculate_var_change, width=15
        )
        self.button_calculate.grid(row=4, column=0, pady=5, padx=5, sticky="w")
        #Postavljanje calculate buttona koji koristi ttk.Button. Kada se klikne, poziva se funkcija calculate_var_change koja postavlja calculate_var na True. Button je smješten u grid layoutu na poziciji (4, 0) s određenim paddingom i poravnanjem.

        self.button_color_toggle = ttk.Checkbutton(
            self.root, text='Uključi/Isključi boju', style='TRadiobutton', command=self.draw_var_change, width=15
        )
        self.button_color_toggle.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        #Postavljanje color toggle buttona koji koristi ttk.Checkbutton. Kada se klikne, poziva se funkcija draw_var_change koja mijenja vrijednost draw_var između True i False. Button je smješten u grid layoutu na poziciji (5, 0) s određenim paddingom i poravnanjem.

        self.image_output = ttk.Label(self.root)
        self.image_output.grid(sticky="e", row=7, column=0, padx=5, pady=5)
        #Postavljanje labela za prikaz slike koji koristi ttk.Label. Label je smješten u grid layoutu na poziciji (7, 0) s određenim paddingom i poravnanjem.  
        
        self.tutorial_label = ttk.Label(self.root, text="Dobrodosli u nas program, za pokretanje programa odaberite kameru, te pritisnite gumb Start. Ako ne odaberete kameru automatski će se koristiti default kamera.", style='TLabel', wraplength=300, justify="center")
        self.tutorial_label.place(relx=0.5, rely=0.03, anchor="center")
        #Postavljanje tutorial labela koji koristi ttk.Label. Label sadrži tekst dobrodošlice i uputa za pokretanje programa. Koristi se wraplength za ograničavanje širine teksta i justify za centriranje teksta. Label je postavljen na sredinu prozora koristeći place metodu s relx, rely i anchor parametrima.

        self.shoulder_angle = ttk.Label(self.root, text="Kut ramena: ", style='TLabel', wraplength=300, justify="center")
        self.shoulder_angle.place(relx=0.5, rely=0.1, anchor="center")
        #Postavljanje shoulder angle labela koji koristi ttk.Label. Label sadrži tekst "Shoulder angle: " i koristi se wraplength za ograničavanje širine teksta i justify za centriranje teksta. Label je postavljen na sredinu prozora koristeći place metodu s relx, rely i anchor parametrima.

        self.knee_angle = ttk.Label(self.root, text="Kut koljena: ", style='TLabel', wraplength=300, justify="center")
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
            self.widgets_frame, text="Kamere", menu=self.menu, direction="below"
        )
        self.menubutton.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        self.menu.delete(0, "end")
        #Popunjavanje menija s dostupnim kamerama. Za svaku dostupnu kameru, dodaje se komanda u menu s tekstom "Camera {i+1}" i funkcijom koja poziva select_camera s odgovarajućim indeksom kamere.   

        self.camera_checker()
        #Nakon postavljanja menubuttona, poziva se funkcija camera_checker kako bi se provjerile dostupne kamere i popunio meni s odgovarajućim opcijama. Ovo osigurava da je meni ažuriran s trenutnim dostupnim kamerama kada se GUI pokrene.
        self.camera_appender()
        #Pozivanje funkcije camera_appender koja kontinuirano provjerava dostupnost kamera i ažurira meni s kamerama. Ova funkcija se poziva nakon postavljanja menubuttona kako bi se osiguralo da je meni ažuriran s trenutnim dostupnim kamerama kada se GUI pokrene.



    def start_var_change_positive(self):
        self.start_var = True
        if self.cam_index_input is None:
            print("No camera selected, defaulting to camera 0")
            self.cam_index_input = self.available[0]
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
        self.available = []
        #stvaranje liste available koja će se koristiti za pohranu indeksa dostupnih kamera. Ova funkcija provjerava dostupnost kamera na računalu tako što pokušava otvoriti svaku kameru od 0 do max_cameras (10) koristeći OpenCV funkciju cv2.VideoCapture. Ako kamera nije dostupna, ispisuje se poruka da kamera nije pronađena. Ako je kamera dostupna, njen indeks se dodaje u listu available, kamera se zatvara i ispisuje se poruka da je kamera OK. Nakon provjere svih indeksa, ispisuje se lista pronađenih kamera.

        for i in range(self.max_cameras):
            #ponavlja petlju od 0 do max_cameras (10) kako bi provjerila dostupnost kamera. Za svaki indeks kamere, pokušava se otvoriti kamera koristeći cv2.Videoself.capture(i). Ako čitanje okvira s kamere nije uspješno, ispisuje se poruka da kamera nije pronađena i nastavlja se na sljedeći indeks. Ako je kamera dostupna, njen indeks se dodaje u listu avaiable, kamera se zatvara i ispisuje se poruka da je kamera OK. Nakon provjere svih indeksa, ispisuje se lista pronađenih kamera.  
            self.cap = cv2.VideoCapture(i)
            
            if not self.cap.read()[0]:
                print(f"Camera index {i:02d} not found...")
                continue
            #Ako čitanje okvira s kamere nije uspješno, ispisuje se poruka da kamera nije pronađena i nastavlja se na sljedeći indeks. Ako je kamera dostupna, njen indeks se dodaje u listu avaiable, kamera se zatvara i ispisuje se poruka da je kamera OK. Nakon provjere svih indeksa, ispisuje se lista pronađenih kamera.
            
            self.available.append(i)
            cv2.destroyAllWindows()
            self.cap.release()
            #Ako je kamera dostupna, njen indeks se dodaje u listu avaiable, kamera se zatvara i ispisuje se poruka da je kamera OK. Nakon provjere svih indeksa, ispisuje se lista pronađenih kamera.
            
            print(f"Camera index {i:02d} OK!")

        try:
            self.available.append(self.cam_index_input)
        except AttributeError:
            self.available.append(0)
            #Ako se dogodi AttributeError prilikom pokušaja dodavanja cam_index_input u listu available, to znači da cam_index_input nije definiran. U tom slučaju, dodaje se indeks 0 u listu available kao zadana kamera. Ovo osigurava da barem jedna kamera bude dostupna u listi, čak i ako cam_index_input nije postavljen.
        self.available.sort()
        #Nakon što su svi dostupni indeksi kamera dodani u listu available, lista se sortira kako bi se osiguralo da su indeksi poredani od najmanjeg do najvećeg. Ovo olakšava korisniku da pronađe i odabere željenu kameru iz menija.
        for i in range(len(self.available) - 2, -1, -1):
            if self.available[i] == self.available[i + 1]:
                self.available.pop(i)
                #Nakon sortiranja liste available, provjerava se da li su susjedni elementi u listi isti. Ako jesu, to znači da je cam_index_input već dodan u listu kao duplikat. U tom slučaju, prvi element (duplikat) se uklanja iz liste pomoću pop(i). Ovo osigurava da lista available sadrži samo jedinstvene indekse kamera, bez duplikata.
      
        print(f"Cameras found: {self.available}")

    def camera_appender(self):
        if not self.start_var or self.app_quit_var:
            self.image_output.configure(image="")
            self.camera_checker()
            #Ova funkcija se koristi za kontinuirano provjeravanje dostupnosti kamera i ažuriranje menija s kamerama. Ako start_var nije postavljen na True ili ako app_quit_var nije postavljen na False, funkcija će očistiti prikaz slike, pozvati camera_checker da provjeri dostupne kamere i ažurirati meni s kamerama ako se lista dostupnih kamera promijenila. Nakon toga, funkcija će se ponovno pozvati nakon 1 sekundu kako bi se kontinuirano provjeravala dostupnost kamera.

            # Ako se lista kamera promijenila → refresh menu
            if self.available != self.last_cameras:
                self.menu.delete(0, "end")
                #Ako se lista dostupnih kamera promijenila u odnosu na prethodnu provjeru (last_cameras), meni se briše i ponovno popunjava s novom listom dostupnih kamera. Ako nema dostupnih kamera, dodaje se onemogućena komanda "No cameras found". Ako postoje dostupne kamere, za svaku kameru se dodaje komanda u meni s tekstom "Camera {i+1}" i funkcijom koja poziva select_camera s odgovarajućim indeksom kamere. Nakon ažuriranja menija, last_cameras se ažurira na trenutnu listu available kako bi se pratilo promjene u dostupnosti kamera.

                if not self.available:
                    self.menu.add_command(label="No cameras found", state="disabled")
                    #Ako nema dostupnih kamera, dodaje se onemogućena komanda "No cameras found" u meni. Ovo informira korisnika da trenutno nema dostupnih kamera za odabir.
                else:
                    for i, cam in enumerate(self.available):
                        self.menu.add_command(
                            label=f"    Kamera {i+1}    ",
                            command=lambda index=cam: self.select_camera(index)
                        )
                        #Ako postoje dostupne kamere, za svaku kameru se dodaje komanda u meni s tekstom "Camera {i+1}" i funkcijom koja poziva select_camera s odgovarajućim indeksom kamere. Ovo omogućava korisniku da odabere željenu kameru iz menija.

                self.last_cameras = self.available.copy()

        # 🔁 Ponovno pozovi funkciju svakih 1s (BITNO)
        self.root.after(1000, self.camera_appender)

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