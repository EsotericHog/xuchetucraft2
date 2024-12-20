#Archivo de configuración global
from pathlib import Path
import os
import sys
from utils.window import get_screen_dimentions, calculate_position
from decouple import config
from typing import Optional

#-----ESTRUCTURA DE DIRECTORIOS DEL PROYECTO-----
#BASE_DIR : Path = Path(__file__).resolve().parent  # Carpeta base del proyecto (desarrollo)
BASE_DIR : str = getattr(sys, '_MEIPASS', os.path.abspath('.'))  # Carpeta base del proyecto (compilado)
AUTH_DIR : str = os.path.join(BASE_DIR, 'auth')  # Carpeta de autenticación
ASSETS_DIR : str = os.path.join(BASE_DIR, 'assets')  # Carpeta de assets


#-----ESTRUCTURA DE DIRECTORIOS DE MINECRAFT-----
APPDATA : Optional[str] = os.getenv('APPDATA')
MC_BASE_DIR : str = os.path.join(APPDATA or '', '.minecraft')
MC_MODS_PATH : str = os.path.join(MC_BASE_DIR, 'mods')
MC_SHADERS_PATH : str = os.path.join(MC_BASE_DIR, 'shaderpacks')
MC_RESOURCES_PATH : str = os.path.join(MC_BASE_DIR, 'resourcepacks')
MC_DH_DATA_PATH : str = os.path.join(MC_BASE_DIR, 'PENDIENTE')  # Ruta para guardar los LOD del mapa del servidor (Distant Horizons)
MC_UNNECESSARY_MODS_FOLDER : str = 'xuchetucraft_mods_sobrantes'
MC_UNNECESSARY_MODS_PATH : str = os.path.join(MC_MODS_PATH, MC_UNNECESSARY_MODS_FOLDER)
MC_VERSIONS_PATH : str = os.path.join(MC_BASE_DIR, 'versions')
MC_SERVERS_DATA_FILE_NAME : str = "servers.dat"
MC_DH_SERVER_DATA_FOLDER : str = "Distant_Horizons_server_data"
MC_LAUNCHER_PROFILES_FILE_NAME : str = "launcher_profiles.json"
MC_LAUNCHER_PROFILE_FABRIC_NAME : str = "fabric-loader-1.20.1"


#-----PREFERENCIAS DE USUARIO-----
PREFERENCES_DIR : str = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Xuchetucraft_config')
PREFERENCES_FILE_NAME : str = 'xuchetuconfig.json'
PREFERENCES_FILE_PATH : str = os.path.join(PREFERENCES_DIR, PREFERENCES_FILE_NAME)
DEFAULT_PREFERENCES_KEY_PATH : str = "instalation_path"
DEFAULT_PREFERENCES : dict[str, str] = {DEFAULT_PREFERENCES_KEY_PATH:MC_BASE_DIR}


#-----PROPIEDADES DE APLICACIÓN-----
APP_VERSION : str = '1.0.0'
APP_NAME : str = 'Xuchetucraft 2'
APP_DESCRIPTION : str = '''
Bienvenido a mi gestor de mods. Aquí podrás:

1. Instalar la versión del modloader necesaria
2. Descargar todos los mods necesarios para acceder al servidor (shaders incluidos)
'''


#-----CUSTOM TKINTER-----
SCREEN_DIMENTIONS : dict[str, int] = get_screen_dimentions()
SCREEN_HEIGHT : int = SCREEN_DIMENTIONS["height"]
WINDOW_WIDTH : int = 900
WINDOW_HEIGHT : int = 600
WINDOW_X_POSITION : int = calculate_position(screen_dimention=SCREEN_DIMENTIONS['width'], window_dimention=WINDOW_WIDTH)
WINDOW_Y_POSITION : int = calculate_position(screen_dimention=SCREEN_DIMENTIONS['height'], window_dimention=WINDOW_HEIGHT)
WINDOW_X_RESIZABLE : bool = False
WINDOW_Y_RESIZABLE : bool = False
MENU_BUTTON_WIDTH : int = int(WINDOW_WIDTH * 0.5)
BUTTON_WIDTH : int = int(WINDOW_WIDTH * 0.3)
BUTTON_SMALL_WIDTH : int = int(WINDOW_WIDTH * 0.15)
INPUT_WIDTH : int = int(WINDOW_WIDTH * 0.6)
INPUT_HEIGHT : int = int(WINDOW_HEIGHT * 0.06)
LIST_WIDTH : int = int(WINDOW_WIDTH * 0.45)
LIST_HEIGHT : int = int(WINDOW_HEIGHT * 0.55)
PROGRESS_BAR_WIDTH : int = int(WINDOW_WIDTH * 0.9)



#-----RECURSOS-----
ICONBITMAP_PATH : str = os.path.join(ASSETS_DIR, 'panda.ico')
#LOGO_PATH : str = os.path.join(ASSETS_DIR, '')
MAIN_IMAGE_PATH : str = os.path.join(ASSETS_DIR, '')
FABRIC_LOGO_PATH : str = os.path.join(ASSETS_DIR, 'fabric_logo.png')
BANNER_PATH : str = os.path.join(ASSETS_DIR, 'Bannerv2.jpg')
LEFT_IMAGE :str = os.path.join(ASSETS_DIR, 'novaskin-wallpaper-llama_cutv2.jpg')
BACKGROUND_IMAGE : str = os.path.join(ASSETS_DIR, 'xc2_bg.jpg')


#-----Google Drive-----
SERVER_PROPS_JSON_ID : str = config('SERVER_PROPS_JSON_ID')
MODS_FOLDER_ID : str = config('MODS_FOLDER_ID')
SHADERS_FOLDER_ID : str = config('SHADERS_FOLDER_ID')
RESOURCEPACKS_FOLDER_ID : str = config('RESOURCEPACKS_FOLDER_ID')
DISTANT_HORIZONS_LOD_FOLDER_ID : str = config('DISTANT_HORIZONS_LOD_FOLDER_ID')