import customtkinter as ctk
from interface.components import create_title_page, create_back_button, create_button
from settings import LIST_WIDTH, LIST_HEIGHT, WINDOW_HEIGHT, PROGRESS_BAR_WIDTH, SHADERS_FOLDER_ID, DEFAULT_PREFERENCES_KEY_PATH
from interface.text import TEXT_SHADERS_TITLE, TEXT_BTN_DOWNLOAD
from backend.local_handler import LocalHandler
from backend.api.google_handler import GoogleDriveHandler
from tkinter import messagebox
import threading
from utils.custom_outputs import print_done
from interface.components import CustomCheckBox
import os
from backend.verifications import Verificator


class PageShaders(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(height=WINDOW_HEIGHT)

        self.title : ctk.CTkLabel = create_title_page(master=self, text=TEXT_SHADERS_TITLE, relx=0.5)

        # Lista para almacenar los estados de los checkboxes
        self.checkboxes : list = []

        # Crear un frame para contener los registros faltantes
        self.frame_list_missing = ctk.CTkScrollableFrame(master=self, width=LIST_WIDTH, height=LIST_HEIGHT, orientation="vertical", fg_color="#252525")
        self.frame_list_missing.place(relx=0.5, rely=0.425, anchor="center")
        
        self.count_size_missing : int = 0 # Peso de los archivos faltantes
        self.total_files_missing : int = 0 # Cantidad de archivos faltantes
        self.label_total_files : ctk.CTkLabel = ctk.CTkLabel(master=self, text=f"{self.total_files_missing} archivos faltantes ({self.count_size_missing} MB)")
        self.label_total_files.place(relx=0.5, rely=0.1, anchor="center")

        # Ruta de instalación local para los archivos
        preferences = Verificator.preferences
        pref_mc_base_dir = preferences.get(DEFAULT_PREFERENCES_KEY_PATH)
        self.local_folder_path = os.path.join(pref_mc_base_dir, "shaderpacks")

        self.reload_data_missing()

        self.quantity_checkboxes_checked = self.count_checked_boxes()
        self.download_file_list = [] # Mods seleccionados a descargar

        self.download_button : ctk.CTkButton = create_button(master=self, text=f"{TEXT_BTN_DOWNLOAD} ({self.quantity_checkboxes_checked})", command=self.execute_download, relx=0.7415, rely=0.875, fg_color="green", hover_color="lightgreen")
        self.download_button.configure(state="disabled") if self.quantity_checkboxes_checked == 0 else self.download_button.configure(state="normal")
        self.back_button : ctk.CTkButton = create_back_button(master=self, command=lambda: controller.show_frame("PageHome"))

        #Label para mostrar qué archivo se está descargando
        self.label_file_downloading = ctk.CTkLabel(master=self, text="")
        self.label_file_downloading.place(relx=0.02, rely=0.75, anchor="w")

        #Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(master=self, orientation="horizontal", width=PROGRESS_BAR_WIDTH, progress_color="green")
        self.progress_bar.set(0)
        self.progress_bar.place(relx=0.02, rely=0.78, anchor="w")
        



    # Recargar registros faltantes
    def reload_data_missing(self):
        for widget in self.frame_list_missing.winfo_children():
            widget.destroy()

        self.checkboxes = []
        count_size : int = 0
        total_files : int = 0

        self.missing_shaders = LocalHandler.get_missing_files(cloud_folder_id=SHADERS_FOLDER_ID, local_folder_path=self.local_folder_path)

        for file in self.missing_shaders:

            var = ctk.StringVar(value=str(file['id']))
            size_mb = round(int(file.get('size', 0)) / (1024 * 1024), 2) # Convertir el tamaño a MB

            frame = ctk.CTkFrame(master=self.frame_list_missing)
            frame.pack(pady=5, padx=5, fill="x")

            checkbox : CustomCheckBox = CustomCheckBox(master=frame, text=f"{file["name"]} ({size_mb} MB)", variable=var, onvalue=str(file["id"]), offvalue="0", extra_attribute=file["name"])
            checkbox.pack(anchor="w", pady=2)

            # Usar la variable checkbox en el lambda
            checkbox.configure(command=lambda cb=checkbox: self.checkbox_callback(cb))
            
            self.checkboxes.append({'checkbox': checkbox, 'name': file['name'], 'var': var}) # Guardar la referencia al checkbox y al archivo

            count_size += int(file["size"])
            total_files += 1
        
        self.count_size_missing = round(int(count_size) / (1024 * 1024), 2)
        self.total_files_missing = total_files
        self.label_total_files.configure(text=f"{self.total_files_missing} archivo/s faltante/s ({self.count_size_missing} MB)")
        

    
    # Contar los mods marcados
    def count_checked_boxes(self) -> int:
        count = 0
        for checkbox in self.checkboxes:
            if checkbox['var'].get() != "0":  # Verificar si el valor no está marcado
                count += 1
        return count



    def checkbox_callback(self, checkbox):
        #self.count_checked_boxes = 0
        print(f"{checkbox.extra_attribute}: {'Seleccionado' if checkbox._variable.get() != "0" else 'No seleccionado'}")
        
        if checkbox._variable.get() != "0":
            self.quantity_checkboxes_checked += 1
        else:
            self.quantity_checkboxes_checked -= 1
            
        self.download_button.configure(text=f"{TEXT_BTN_DOWNLOAD} ({self.quantity_checkboxes_checked})")
        self.download_button.configure(state="disabled") if self.quantity_checkboxes_checked == 0 else self.download_button.configure(state="normal")

    

    def execute_download(self):
        if messagebox.askokcancel("Confirmar descarga", f"Se han seleccionado {self.quantity_checkboxes_checked} fichero/s ¿Desea continuar?"):

            #Desactivar botones
            self.download_button.configure(state="disabled")
            self.back_button.configure(state="disabled")

            self.progress_bar.set(0)
            self.done_event = threading.Event()  # Evento
            

            for item in self.checkboxes:
                checkbox = item['checkbox']
                if checkbox._variable.get() != "0":
                    self.download_file_list.append({"id":checkbox._variable.get(), "name":item["name"]})
            
            GoogleDriveHandler.download_files(files=self.download_file_list, progress_bar=self.progress_bar, root=self, done_event=self.done_event, progress_bar_max_steps=len(self.download_file_list), label_file = self.label_file_downloading, path=self.local_folder_path)

            self.after(100, self.check_done_event)  # Start checking the done event



    # Función para monitorear el evento de completado
    def check_done_event(self):
        if self.done_event.is_set():
            print_done("Archivos descargados e instalados con éxito")
            messagebox.showinfo("Descarga completa", "Se han descargado todos los archivos necesarios")
            
            self.reload_data_missing()
            self.download_file_list = []
            self.checkboxes = []
            self.quantity_checkboxes_checked = 0

            self.download_button.configure(text=f"{TEXT_BTN_DOWNLOAD} ({self.quantity_checkboxes_checked})")
            self.download_button.configure(state="disabled") if self.quantity_checkboxes_checked == 0 else self.download_button.configure(state="normal")
            self.back_button.configure(state="normal")
        else:
            self.after(100, self.check_done_event)  # Check again after 100ms