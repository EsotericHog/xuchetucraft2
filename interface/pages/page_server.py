import customtkinter as ctk
from interface.components import create_title_page, create_back_button, create_button
from settings import LIST_WIDTH, LIST_HEIGHT, WINDOW_HEIGHT, DEFAULT_PREFERENCES_KEY_PATH
from interface.text import TEXT_SERVER_TITLE, TEXT_BTN_ADD
from tkinter import messagebox
from utils.custom_outputs import print_done
import os
from backend.verifications import Verificator
from backend.tasks import add_server_to_game


class PageAddServer(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(height=WINDOW_HEIGHT)

        self.title : ctk.CTkLabel = create_title_page(master=self, text=TEXT_SERVER_TITLE, relx=0.5)
        self.subtitle : ctk.CTkLabel = ctk.CTkLabel(master=self, text=f"Información del Servidor")
        self.subtitle.place(relx=0.5, rely=0.12, anchor="center")

        # Crear un frame para contener la información del servidor
        self.frame_info = ctk.CTkScrollableFrame(master=self, width=LIST_WIDTH, height=LIST_HEIGHT, orientation="vertical", fg_color="#252525")
        self.frame_info.place(relx=0.5, rely=0.425, anchor="center")

        # Ruta de instalación local para los archivos
        preferences = Verificator.preferences
        self.local_folder_path = preferences.get(DEFAULT_PREFERENCES_KEY_PATH)

        self.server_data = Verificator.server_data

        self.show_info()

        self.add_button : ctk.CTkButton = create_button(master=self, text=TEXT_BTN_ADD, command=self.execute, relx=0.7415, rely=0.875, fg_color="green", hover_color="lightgreen")
        self.back_button : ctk.CTkButton = create_back_button(master=self, command=lambda: controller.show_frame("PageHome"))  



    # Mostrar información del server
    def show_info(self):
        #Nombre del server
        self.label_name = ctk.CTkLabel(master=self.frame_info, text=f"Nombre: {self.server_data["name"]}")
        self.label_name.pack(pady=5, padx=5, anchor="w")
        #IP del server
        self.label_address = ctk.CTkLabel(master=self.frame_info, text=f"IP: {self.server_data["ip_address"]}")
        self.label_address.pack(pady=5, padx=5, anchor="w")
        #Puerto
        self.label_port = ctk.CTkLabel(master=self.frame_info, text=f"Puerto: {self.server_data["port"]}")
        self.label_port.pack(pady=5, padx=5, anchor="w")
        #Versión
        self.label_version = ctk.CTkLabel(master=self.frame_info, text=f"Versión: {self.server_data["version"]}")
        self.label_version.pack(pady=5, padx=5, anchor="w")
        #Modloader
        self.label_modloader = ctk.CTkLabel(master=self.frame_info, text=f"Modloader: {self.server_data["modloader_install_folder"]}")
        self.label_modloader.pack(pady=5, padx=5, anchor="w")

    

    #Agregar servidor al juego
    def execute(self):
        if messagebox.askokcancel("Confirmación", f"Se agregará {self.server_data["name"]} al modo multijugador de Minecraft. ¿Deseas continuar?"):
            add_server_to_game(self.local_folder_path, self.server_data)
            messagebox.showinfo("Tarea completada", "Servidor agregado con éxito.")
            self.controller.show_frame("PageHome")