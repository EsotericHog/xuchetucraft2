import os
from tkinter import messagebox
from backend.pref_handler import PreferencesHandler
from settings import DEFAULT_PREFERENCES_KEY_PATH, MC_VERSIONS_PATH, MC_BASE_DIR
from backend.api.google_handler import GoogleDriveHandler
from utils.custom_outputs import print_warn, print_info, print_err

class Verificator():
    '''Clase para comprobar la existencia de ciertos elementos del juego, como la versión, y el perfil'''

    # Cargar preferencias de usuario
    preferences : dict = PreferencesHandler.load_preferences()
    # Cargar datos del servidor
    server_data : dict = GoogleDriveHandler.download_server_props_json()
    # Cargar datos del sistema
    system_data = "PENDIENTE"

    # Comprobar si minecraft se encuentra en la ruta por defecto.
    @classmethod
    def verificate_minecraft_default_path(cls) -> None:
        default_path : str = cls.preferences.get(DEFAULT_PREFERENCES_KEY_PATH)
        if not os.path.exists(default_path):
            messagebox.showwarning(f"Ruta no encontrada", "No se ha encontrado una ruta de instalación válida. Si instalaste minecraft en una ruta diferente, establécelo en las preferencias de usuario")
            print_warn(f"No se ha encontrado la ruta de instalación {default_path}")
        
        else:
            print_info("Ruta de instalación encontrada")


    
    # Comprobar si está instalada la versión vanilla correcta
    @classmethod
    def verificate_vanilla_installation(cls) -> None:
        default_path : str = cls.preferences.get(DEFAULT_PREFERENCES_KEY_PATH)
        version : str = cls.server_data["version"]
        file_path : str = os.path.join(default_path, "versions", version, f'{version}.jar')

        if not os.path.exists(file_path):
            messagebox.showwarning("Versión no encontrada", f"No se ha encontrado la instalación de la versión necesaria. Antes de usar el programa, instala la versión {version} vanilla.")
            print_err(f"Versión {version} no encontrada")

        else:
            print_info(f"Versión {version} instalada")

    
    # Comprobar si el modloader está instalado
    @classmethod
    def verificate_modloader_installation(cls):
        default_path : str = cls.preferences.get(DEFAULT_PREFERENCES_KEY_PATH)
        modloader_name : str = cls.server_data["launcher_profiles"]["name"]
        modloader_folder_name : str = cls.server_data["modloader_install_folder"]
        modloader_file_name : str = cls.server_data["modloader_install_file"]
        modloader_file_path : str = os.path.join(default_path, "versions", modloader_folder_name, modloader_file_name)

        if not os.path.exists(modloader_file_path):
            messagebox.showwarning("Modloader no encontrado", f"No se ha encontrado la instalación del modloader necesaria. Antes de continuar, instala {modloader_name}")
            print_warn(f"Instalación de modloader {modloader_name} no encontrada")
        else:
            print_info(f"Modloader {modloader_name} instalado")

    
    # Denegar acceso a directorio base si no existe.
    @classmethod
    def validate_game_directory(cls) -> None:
        '''Método que da error y anula cuando la ruta no existe'''
        default_path : str = cls.preferences.get(DEFAULT_PREFERENCES_KEY_PATH)
        if not os.path.exists(default_path):
            messagebox.showerror(f"Ruta no encontrada", "No se ha encontrado la ruta de instalación")
            print_err(f"No se ha encontrado la ruta de instalación {default_path}")
        
        else:
            print_info("Ruta de instalación encontrada")
            os.startfile(default_path)