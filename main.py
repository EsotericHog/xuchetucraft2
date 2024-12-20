from interface.ctk_root import App
from backend.pref_handler import PreferencesHandler
from backend.verifications import Verificator
from backend.tasks import clean_all_incomplete_files
from settings import DEFAULT_PREFERENCES_KEY_PATH
import os

#Crear archivo de configuración si no existe
PreferencesHandler.create_preferences_file()

#Comprobar si minecraft está instalado (ruta por defecto)
Verificator.verificate_minecraft_default_path()

#Comprobar si la versión correcta está instalada
Verificator.verificate_vanilla_installation()

#Eliminar archivos descargados incorrectamente
clean_all_incomplete_files(Verificator.preferences.get(DEFAULT_PREFERENCES_KEY_PATH))

#Arrancar instancia customtkinter
ctk_root = App()
ctk_root.mainloop()