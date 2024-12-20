import customtkinter as ctk
from interface.components import create_title_page, create_back_button, create_button
from settings import LIST_WIDTH, LIST_HEIGHT, WINDOW_HEIGHT, PROGRESS_BAR_WIDTH, MODS_FOLDER_ID, DEFAULT_PREFERENCES_KEY_PATH
from interface.text import TEXT_MODS_TITLE, TEXT_MODS_CHECK_1, TEXT_MODS_CHECK_2, TEXT_BTN_DOWNLOAD, TEXT_BTN_HANDLE_UNNECESSARY_MODS
from backend.local_handler import LocalHandler
from backend.api.google_handler import GoogleDriveHandler
from backend.verifications import Verificator
from tkinter import messagebox
import threading
from utils.custom_outputs import print_done
from interface.components import CustomCheckBox
import os


class PageMods(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(height=WINDOW_HEIGHT)

        self.title : ctk.CTkLabel = create_title_page(master=self, text=TEXT_MODS_TITLE, relx=0.5)

        # Lista para almacenar los estados de los checkboxes
        self.checkboxes : list = []

        # Crear un frame para contener los registros faltantes
        self.frame_list_missing = ctk.CTkScrollableFrame(master=self, width=LIST_WIDTH, height=LIST_HEIGHT, orientation="vertical", fg_color="#252525")
        self.frame_list_missing.place(relx=0.02, rely=0.425, anchor="w")
        
        self.count_size_missing : int = 0 # Peso de los archivos faltantes
        self.total_files_missing : int = 0 # Cantidad de archivos faltantes
        self.label_total_files : ctk.CTkLabel = ctk.CTkLabel(master=self, text=f"{self.total_files_missing} archivos faltantes ({self.count_size_missing} MB)")
        self.label_total_files.place(relx=0.1, rely=0.1)

        # Crear un frame para contener los registros sobrantes
        self.frame_list_unnecessary = ctk.CTkScrollableFrame(master=self, width=LIST_WIDTH, height=LIST_HEIGHT, orientation="vertical", fg_color="#252525")
        self.frame_list_unnecessary.place(relx=0.5, rely=0.425, anchor="w")
        self.total_files_unnecessary : int = 0 # Cantidad de archivos faltantes
        self.label_total_files_2 : ctk.CTkLabel = ctk.CTkLabel(master=self, text=f"{self.total_files_unnecessary} archivos sobrantes")
        self.label_total_files_2.place(relx=0.65, rely=0.1)

        #Sección de radiobuttons para elegir qué hacer con lo sobrante
        self.radio_control = ctk.StringVar(value="move")
        # Radiobutton 1
        self.radio1 = ctk.CTkRadioButton(self, text=TEXT_MODS_CHECK_1, variable=self.radio_control, value="move", )
        self.radio1.place(relx=0.1, rely=0.875, anchor="center")
        # Radiobutton 2
        self.radio2 = ctk.CTkRadioButton(self, text=TEXT_MODS_CHECK_2, variable=self.radio_control, value="delete")
        self.radio2.place(relx=0.3, rely=0.875, anchor="center")

        # Ruta de instalación local para los archivos
        preferences = Verificator.preferences
        pref_mc_base_dir = preferences.get(DEFAULT_PREFERENCES_KEY_PATH)
        self.local_folder_path = os.path.join(pref_mc_base_dir, "mods")

        self.reload_data_missing()
        self.reload_data_unnecessary()

        self.quantity_checkboxes_checked = self.count_checked_boxes()
        self.download_file_list = [] # Mods seleccionados a descargar

        self.download_button : ctk.CTkButton = create_button(master=self, text=f"{TEXT_BTN_DOWNLOAD} ({self.quantity_checkboxes_checked})", command=self.execute_download, relx=0.7415, rely=0.875, fg_color="green", hover_color="lightgreen")
        self.download_button.configure(state="disabled") if self.quantity_checkboxes_checked == 0 else self.download_button.configure(state="normal")
        
        self.handle_unnecessary_mods_button : ctk.CTkButton = create_button(master=self, text=TEXT_BTN_HANDLE_UNNECESSARY_MODS, command=self.handle_unnecessary_mods, relx=0.55, rely=0.875)
        self.handle_unnecessary_mods_button.configure(state="disabled") if len(self.unnecessary_mods) == 0 else self.handle_unnecessary_mods_button.configure(state="normal")
        self.back_button : ctk.CTkButton = create_back_button(master=self, command=lambda: controller.show_frame("PageHome"))

        # Label para mostrar qué archivo se está descargando
        self.label_file_downloading = ctk.CTkLabel(master=self, text="")
        self.label_file_downloading.place(relx=0.02, rely=0.75, anchor="w")

        # Barra de progreso
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


        self.missing_mods = LocalHandler.get_missing_files(cloud_folder_id=MODS_FOLDER_ID, local_folder_path=self.local_folder_path)

        for file in self.missing_mods:

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



    # Recargar registros sobrantes
    def reload_data_unnecessary(self):
        for widget in self.frame_list_unnecessary.winfo_children():
            widget.destroy()

        total_files : int = 0

        self.unnecessary_mods = LocalHandler.get_excess_files(self.local_folder_path)

        for file in self.unnecessary_mods:

            label = ctk.CTkLabel(master=self.frame_list_unnecessary, text=file)
            label.pack(pady=5, padx=5, anchor="w")

            total_files += 1
        
        self.total_files_unnecessary = total_files
        self.label_total_files_2.configure(text=f"{self.total_files_unnecessary} archivo/s sobrante/s")
        

    
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
            self.handle_unnecessary_mods_button.configure(state="disabled")
            self.back_button.configure(state="disabled")

            self.progress_bar.set(0)
            self.done_event = threading.Event()  # Evento

            for item in self.checkboxes:
                checkbox = item['checkbox']
                if checkbox._variable.get() != "0":
                    self.download_file_list.append({"id":checkbox._variable.get(), "name":item["name"]})
            
            GoogleDriveHandler.download_files(files=self.download_file_list, progress_bar=self.progress_bar, root=self, done_event=self.done_event, progress_bar_max_steps=len(self.download_file_list), label_file = self.label_file_downloading, path=self.local_folder_path)

            self.after(100, self.check_done_event)  # Start checking the done event


    
    def handle_unnecessary_mods(self):
        # Mover mods innecesarios
        if self.radio_control.get() == "move":
            if messagebox.askokcancel("Mover mods", "¿Estás seguro de que quieres mover los mods innecesarios a otra ubicación?"):
                LocalHandler.move_files(list=self.unnecessary_mods, local_folder_path=self.local_folder_path)
                messagebox.showinfo("Archivos movidos", "Archivos innecesarios movidos con éxito")
        # Eliminar mods innecesarios
        elif self.radio_control.get() == "delete":
            if messagebox.askokcancel("Eliminar mods", "¿Estás seguro de que deseas eliminar los mods innecesarios"):
                LocalHandler.delete_files(self.unnecessary_mods, local_folder_path=self.local_folder_path)
                messagebox.showinfo("Archivos eliminados", "Archivos innecesarios eliminados con éxito")
        
        self.reload_data_unnecessary()
        self.handle_unnecessary_mods_button.configure(state="disabled") if len(self.unnecessary_mods) == 0 else self.handle_unnecessary_mods_button.configure(state="normal")
            


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
            self.handle_unnecessary_mods_button.configure(state="disabled") if len(self.unnecessary_mods) == 0 else self.handle_unnecessary_mods_button.configure(state="normal")
            self.back_button.configure(state="normal")
        else:
            self.after(100, self.check_done_event)  # Check again after 100ms