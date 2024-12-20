import os
import json
from settings import PREFERENCES_DIR, PREFERENCES_FILE_PATH, DEFAULT_PREFERENCES, DEFAULT_PREFERENCES_KEY_PATH
from utils.custom_outputs import print_done
from tkinter import messagebox

class PreferencesHandler():
    '''Clase para gestionar la configuración local de la aplicación'''

    #Crear archivo de configuración
    @classmethod
    def create_preferences_file(cls) -> None:
        if not os.path.exists(PREFERENCES_DIR):
            os.makedirs(PREFERENCES_DIR)

        if not os.path.exists(PREFERENCES_FILE_PATH):
            with open(PREFERENCES_FILE_PATH, 'w') as file:
                json.dump(DEFAULT_PREFERENCES, file, indent=4)


    #Leer archivo de configuración
    @classmethod
    def load_preferences(cls, file_path : str = PREFERENCES_FILE_PATH) -> dict:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                preferences : dict = json.load(file)
                print_done("Preferencias cargadas correctamente")
                return preferences
        else:
            return {}
        

    # Guardar nuevos ajustes
    @classmethod
    def save_preferences(cls, path: str) -> None:
        preferences : dict[str, str] = {DEFAULT_PREFERENCES_KEY_PATH:path}
        with open(PREFERENCES_FILE_PATH, 'w') as file:
            json.dump(preferences, file, indent=4)
            messagebox.showinfo("Datos actualizados", "Se han guardado los cambios. La aplicación se reiniciará.")
            print_done("Se han cambiado las preferencias de usuario")