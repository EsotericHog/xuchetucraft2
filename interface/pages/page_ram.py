import customtkinter as ctk
from interface.text import TEXT_BTN_SAVE, TEXT_RAM_TITLE, TEXT_RAM_AVAILABLE, TEXT_RAM_REQUIRED_1, TEXT_RAM_REQUIRED_2, TEXT_RAM_REQUIRED_3
from interface.components import create_title_page, create_back_button, create_subtitle_page, create_button
from tkinter import messagebox
from settings import INPUT_WIDTH, DEFAULT_PREFERENCES_KEY_PATH, MC_LAUNCHER_PROFILES_FILE_NAME, LIST_WIDTH
from backend.verifications import Verificator
from backend.tasks import get_total_memory_system_gb, load_json_launcher_profile, get_current_memory_launcher_profile, save_json_launcher_profile
import os


class PageRam(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title : ctk.CTkLabel = create_title_page(master=self, text=TEXT_RAM_TITLE, relx=0.5)

        # Frame para mostrar información de la RAM
        self.frame_info = ctk.CTkScrollableFrame(master=self, width=LIST_WIDTH, height=200, orientation="vertical", fg_color="#252525")
        self.frame_info.place(relx=0.5, rely=0.3, anchor="center")

        # Carga de datos
        preferences = Verificator.preferences
        mc_base_folder = preferences.get(DEFAULT_PREFERENCES_KEY_PATH)
        self.local_file_path = os.path.join(mc_base_folder, MC_LAUNCHER_PROFILES_FILE_NAME)
        self.server_data = Verificator.server_data
        self.system_data = Verificator.system_data

        self.subtitle : ctk.CTkLabel = create_subtitle_page(master=self, text="", relx=0.5, rely=0.55)
        self.subtitle_2 : ctk.CTkLabel = create_subtitle_page(master=self, text="Memoria actual asignada al juego:", relx=0.35, rely=0.65)

        self.input_ram : ctk.CTkEntry = ctk.CTkEntry(master=self, width=INPUT_WIDTH)
        self.input_ram.place(relx = 0.5, rely = 0.71, anchor="center")

        self.show_info()

        self.button_save : ctk.CTkButton = create_button(master=self, text=TEXT_BTN_SAVE, fg_color="green", hover_color="green", relx=0.7, rely=0.875, command=self.save_ram)
        self.button_back : ctk.CTkButton = create_back_button(master=self, command=lambda: controller.show_frame("PageHome"))


    # Mostrar información de ram
    def show_info(self):
        self.ram_system = get_total_memory_system_gb()
        self.launcher_profiles = load_json_launcher_profile(path=self.local_file_path)
        if self.launcher_profiles:
            mc_current_ram = get_current_memory_launcher_profile(self.launcher_profiles)
            self.input_ram.insert(0, mc_current_ram)
        else:
            messagebox.showerror("Archivo no encontrado", "No se encontró el archivo de configuración de perfiles del lanzador. No es posible obtener ni modificar la ram asignada al juego.")

        self.ram_minimun_only_mods = self.server_data["ram"]["ram_minimun_only_mods"]
        self.ram_minimun_full_set = self.server_data["ram"]["ram_minimun_full_set"]
        self.ram_recommended_full_set = self.server_data["ram"]["ram_recommended_full_set"]

        # Sistema
        self.label_system_ram = ctk.CTkLabel(master=self.frame_info, text=f"{TEXT_RAM_AVAILABLE}:  {self.ram_system:.2f} GB")
        self.label_system_ram.pack(pady=5, padx=5, anchor="w")
        # RAM minima requerida (mods)
        self.label_min_ram_1 = ctk.CTkLabel(master=self.frame_info, text=f"{TEXT_RAM_REQUIRED_1}:  {self.ram_minimun_only_mods} GB")
        self.label_min_ram_1.pack(pady=5, padx=5, anchor="w")
        # RAM mínima requerida (mods + Distant Horizons)
        self.label_version = ctk.CTkLabel(master=self.frame_info, text=f"{TEXT_RAM_REQUIRED_2}:  {self.ram_minimun_full_set} GB")
        self.label_version.pack(pady=5, padx=5, anchor="w")
        # RAM recomendada
        self.label_version = ctk.CTkLabel(master=self.frame_info, text=f"{TEXT_RAM_REQUIRED_3}:  {self.ram_recommended_full_set} GB o superior")
        self.label_version.pack(pady=5, padx=5, anchor="w")

        self.show_subtitle()


    # Método para determinar qué mensaje se va a mostrar sobre el input
    def show_subtitle(self):
        sub_text = ""
        if int(self.ram_system) >= int(self.ram_recommended_full_set) or (int(self.ram_system)+1) >= int(self.ram_recommended_full_set):
            sub_text = f'''Cuando asignes más memoria, asegúrate de dejar al menos 2gb libres para el sistema. 
            Ej: Si tienes 16gb, puedes asignar 14gb (aprox.) y dejar 2gb libres. Sin embargo, 
            con la RAM recomendada es suficiente ({self.ram_recommended_full_set} GB)'''

        elif int(self.ram_system) >= int(self.ram_minimun_full_set) or (int(self.ram_system)+1) >= int(self.ram_minimun_full_set):
            sub_text = f'''Tu equipo cumple con los requisitos mínimos para jugar con el modpack. Sin embargo, 
            es posible que tengas problemas de rendimiento si intentas usar Distant Horizons. 
            Al asignar más ram, te recomiendo que dejes al menos 2gb para el sistema. Ej: Si 
            tienes 6gb, asigna 4gb y deja 2gb libres.'''

        else:
            self.button_save.configure(state="disabled")
            sub_text = f'''Lamentablemente, tu equipo no cumple con los requisitos de sistema mínimos 
            para jugar con el modpack. Experimentarás problemas de rendimiento.'''
            messagebox.showinfo("No disponible", "Tu equipo no cumple con los requisitos de sistema mínimos para jugar con el modpack")

        self.subtitle.configure(text=sub_text)


    def save_ram(self):
        if not self.launcher_profiles:
            messagebox.showerror("Archivo no encontrado", "No es posible realizar esta operación. Archivo de configuración no encontrado.")

        else:
            if messagebox.askokcancel("Confirmar cambios", "¿Estás seguro de que deseas realizar estos cambios?"):
                if not int(self.ram_system) >= int(self.input_ram.get()):
                    messagebox.showerror("Valor incorrecto", "No es posible asignar este valor.")

                else:
                    save_json_launcher_profile(self.local_file_path, self.input_ram.get())