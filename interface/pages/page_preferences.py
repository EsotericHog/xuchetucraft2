import customtkinter as ctk
from interface.text import TEXT_PREFERENCES_TITLE, TEXT_PREFERENCES_SUBTITLE, TEXT_BTN_SEARCH, TEXT_BTN_SAVE
from interface.components import create_title_page, create_back_button, create_subtitle_page, create_button
from tkinter import filedialog, messagebox
from settings import INPUT_WIDTH, DEFAULT_PREFERENCES_KEY_PATH
from backend.verifications import Verificator
from backend.pref_handler import PreferencesHandler
import sys
import subprocess
import os

class PagePref(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title : ctk.CTkLabel = create_title_page(master=self, text=TEXT_PREFERENCES_TITLE, relx=0.5)
        self.subtitle : ctk.CTkLabel = create_subtitle_page(master=self, text=TEXT_PREFERENCES_SUBTITLE, relx=0.5, rely=0.3)

        preferences = Verificator.preferences
        self.local_folder_path = preferences.get(DEFAULT_PREFERENCES_KEY_PATH)


        self.input_path : ctk.CTkEntry = ctk.CTkEntry(master=self, width=INPUT_WIDTH)
        self.input_path.insert(0, self.local_folder_path)
        self.input_path.place(relx = 0.39, rely = 0.4, anchor="center")
        self.button_search : ctk.CTkButton = create_button(master=self, text=TEXT_BTN_SEARCH, relx=0.8, rely=0.4, command=self.select_directory)

        self.button_save : ctk.CTkButton = create_button(master=self, text=TEXT_BTN_SAVE, fg_color="green", hover_color="green", relx=0.7, rely=0.875, command=self.save_preferences)
        self.button_back : ctk.CTkButton = create_back_button(master=self, command=lambda: controller.show_frame("PageHome"))

    
    def select_directory(self):
        # Abrir el cuadro de diálogo para seleccionar una carpeta
        directory = filedialog.askdirectory(title="Seleccionar Carpeta")
        if directory:
            self.input_path.delete(0, 'end')
            self.input_path.insert(0, directory)


    def save_preferences(self):
        if not self.local_folder_path == self.input_path.get():
            if messagebox.askokcancel("Reiniciar", "Para aplicar los cambios, es necesario reiniciar la aplicación. ¿Desea continuar?"):
                PreferencesHandler.save_preferences(path=self.input_path.get())
                self.restart_app()


    def restart_app(self):
        # Reiniciar la aplicación
        if getattr(sys, 'frozen', False):
            # PyInstaller crea un ejecutable, se usa subprocess para reiniciar
            subprocess.call([sys.executable] + sys.argv)
        else:
            # En caso de no estar ejecutando desde PyInstaller
            python = sys.executable
            os.execl(python, python, *sys.argv)