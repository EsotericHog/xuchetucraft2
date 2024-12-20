import os
from .api.google_handler import GoogleDriveHandler
from settings import MC_UNNECESSARY_MODS_FOLDER
import shutil
from utils.custom_outputs import print_info, print_done, print_err
import nbtlib

class LocalHandler():

    MODS_REQUIRED = []

    @classmethod
    #Obtener lista de archivos de google drive (requeridos)
    def get_missing_files(cls, cloud_folder_id : str, local_folder_path : str):
        missing_files = []
        required_files = GoogleDriveHandler.search_files(cloud_folder_id)
        cls.MODS_REQUIRED = required_files

        for file in required_files:
            file_path = os.path.join(local_folder_path, file['name'])

            if not os.path.exists(file_path):
                # Maneja los casos donde el archivo es una carpeta)
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    print_info(f'Archivo "{file["name"]}" es una carpeta')
                    lod_files = GoogleDriveHandler.search_files(file['id'])
                    file_size = 0
                    for lod in lod_files:
                        file_size += int(lod['size'])
                    missing_files.append({'id': file['id'], 'name': file['name'], 'size': file_size, 'mimeType':file['mimeType']})

                else:
                    missing_files.append({'id': file['id'], 'name': file['name'], 'size': file['size'], 'mimeType':file['mimeType']})
        

        print_done("Búsqueda de archivos requeridos completada")
        return missing_files
    

    @classmethod
    def get_excess_files(cls, local_folder_path : str):
        excess_files = []
        raw_required_files = cls.MODS_REQUIRED
        required_files = []

        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)
            
        #Obtener lista de archivos existentes en el cliente y excluir las carpetas
        raw_local_files = os.listdir(local_folder_path)
        exist_files = [file for file in raw_local_files if not os.path.isdir(os.path.join(local_folder_path, file))]

        for file in raw_required_files:
            required_files.append(file['name'])


        for file in exist_files:
            if not file in required_files:
                excess_files.append(file)
        
        print_done("Búsqueda de archivos innecesarios completada")
        return excess_files
    

    @classmethod
    def move_files(cls, list, origin_folder_path):
        if len(list) > 0:
            path = os.path.join(origin_folder_path, MC_UNNECESSARY_MODS_FOLDER)
            if not os.path.exists(path):
                cls.create_folder(path)
                
            for file in list:
                file_path = os.path.join(origin_folder_path, file)
                destination_file_path = os.path.join(path, file)

                if os.path.exists(file_path):
                    shutil.move(file_path, destination_file_path)
                    print(f"Archivo '{file}' movido a {path}")

                else:
                    print(f"El archivo '{file}' no existe en la ubicación original.")
                    pass


    @classmethod
    def delete_files(cls, list, origin_folder_path):
        if len(list) > 0:
            for file in list:
                file_path = os.path.join(origin_folder_path, file)

                if os.path.exists(file_path):
                    os.remove(file_path)
                    print_done(f"Archivo '{file}' eliminado")
                else:
                    print_info(f"El archivo '{file}' no existe en la ubicación original.")
                    pass


    @classmethod
    def create_folder(cls, path):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            #print(f'Error al crear la carpeta: {e}')
            pass

    
    # Crea archivo de servidores del juego (vacío)
    @classmethod
    def create_nbt_file(cls, path) -> None:

        # Lista vacía de servidores
        server_list = nbtlib.List[nbtlib.Compound]()

        # Crear archivo
        nbt_file = nbtlib.File({'servers': server_list})

        try:
            #Guardar archivo
            nbt_file.save(path)
            print_done("Archivo de configuración de servidores vacío creado.")
        except Exception as e:
            print_err(f"No se pudo crear el archivo de configuración de servidores: {e}")