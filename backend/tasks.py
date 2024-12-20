import webbrowser
from tkinter import messagebox
import os
from backend.local_handler import LocalHandler
from settings import MC_SERVERS_DATA_FILE_NAME, MC_LAUNCHER_PROFILE_FABRIC_NAME, MC_LAUNCHER_PROFILES_FILE_NAME
import nbtlib
from backend.verifications import Verificator
from utils.custom_outputs import *
import psutil
import json
import re


#-----MÓDULO PARA LA LÓGICA DE LA APLICACIÓN-----

# Descargar Fabric Loader
def option_1() -> None:
    # Obtener enlace de Fabric desde Drive
    server_data = Verificator.server_data
    #server_data = json.loads(server_data_bytes)
    print(type(server_data))

    #Descargar binario de Fabric
    url : str = server_data['modloader_url']

    webbrowser.open(url)
    messagebox.showinfo("Información", "Abre el ejecutable y continúa la instalación")



# Agregar servidor al juego
def add_server_to_game(folder_path, data) -> None:
    path = os.path.join(folder_path, MC_SERVERS_DATA_FILE_NAME)
    if not os.path.exists(path):
        print_err(f'Archivo "{MC_SERVERS_DATA_FILE_NAME}" no encontrado')
        LocalHandler.create_nbt_file(path)

    #Cargar archivo NBT
    nbt_file = nbtlib.load(path)
    print_info(f"Archivo NBT cargado: {nbt_file}")

    # Obtener lista de servidores
    servers_list = nbt_file['servers']

    # Definición de la estructura del archivo NBT
    name = data["name"]
    address = data["ip_address"]

    new_server = nbtlib.Compound({
        'name': nbtlib.String(name),
        'ip': nbtlib.String(address),
        'hidden': nbtlib.Byte(0)
    })

    # Añadir servidor
    servers_list.append(new_server)

    # Guardar cambios
    nbt_file.save(path)
    print_done("Servidor agregado correctamente.")


#Eliminar archivos globales descargados incorrectamente
def clean_all_incomplete_files(path):
    mods_folder = os.path.join(path, 'mods')
    shaderpacks_folder = os.path.join(path, 'shaderpacks')
    resourcepacks_folder = os.path.join(path, 'resourcepacks')
    
    clean_incomplete_files(mods_folder) if os.path.exists(mods_folder) else print_info('Directorio "mods" no encontrado')
    clean_incomplete_files(shaderpacks_folder) if os.path.exists(shaderpacks_folder) else print_info('Directorio "shaderpacks" no encontrado')
    clean_incomplete_files(resourcepacks_folder) if os.path.exists(resourcepacks_folder) else print_info('Directorio "resourcepacks" no encontrado')


def clean_incomplete_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and os.path.getsize(filepath) == 0:
            os.remove(filepath)
            print_info(f"{filename} ha sido eliminado")



# Obtener la memoria ram del sistema
def get_total_memory_system_gb() -> float:
    # Obtén la RAM total en bytes
    total_memory = psutil.virtual_memory().total

    # Convierte a GB
    total_memory_gb = total_memory / (1024 ** 3)

    return total_memory_gb



# Obtener RAM asignada actualmente al perfil de fabric
def get_current_memory_launcher_profile(json_parsed) -> str:
    try:
        profile = json_parsed['profiles'][MC_LAUNCHER_PROFILE_FABRIC_NAME]

        java_args = profile['javaArgs']

        # Buscar el valor de la RAM usando expresión regular
        match = re.search(r'-Xmx(\d+)G', java_args)

        if match:
            current_ram_value = match.group(1)
            print_info(f"RAM asignada actualmente al juego: {current_ram_value} GB")
            return current_ram_value
        else:
            print_warn(f"RAM asignada al juego desconocida")
            return "Desconocido"
    except Exception as e:
        print(e)
    

# Cargar json con perfiles del launcher
def load_json_launcher_profile(path : str) -> dict:
    data : dict = {}

    if os.path.exists(path):
        with open(path, 'r') as file:
            data = json.load(file)
    else:
        print_err(f'Archivo "{MC_LAUNCHER_PROFILES_FILE_NAME}" no encontrado')

    return data


# Guardar RAM
def save_json_launcher_profile(path : str, value : str) -> None:
    new_value = value #10
    data = load_json_launcher_profile(path)
    profile = data['profiles']['fabric-loader-1.20.1']
    profile['javaArgs'] = re.sub(r'-Xmx\d+G', f'-Xmx{new_value}G', profile['javaArgs'])

    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
        messagebox.showinfo("Cambios guardados", "Se ha actualizado la memoria RAM asignada al juego.")
        print_done("Memoria ram actualizada.")
