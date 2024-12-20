from .google_auth import GoogleDriveAuth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io
import os
from settings import SERVER_PROPS_JSON_ID
from tkinter import messagebox
import json
import threading
import queue
from utils.custom_outputs import print_err, print_done

class GoogleDriveHandler:
    '''Clase estática para acceder a los ficheros de Google Drive'''
    
    @classmethod
    def download_server_props_json(cls, file_id : str = SERVER_PROPS_JSON_ID) -> dict:

        try:
            # Autenticar
            creds = GoogleDriveAuth.authenticate()
            service = build('drive', 'v3', credentials=creds)

            # Descargar contenido del archivo
            request = service.files().get_media(fileId=file_id)
            fh : io.BytesIO = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
        
            done : bool = False
            while not done:
                status, done = downloader.next_chunk()
                #print(f"Descargado {int(status.progress() * 100)}%.")

            content : bytes = fh.getvalue()

            print_done("Propiedades del servidor descargadas con éxito")
            return json.loads(content)
        
        except HttpError as e:
            messagebox.showerror(title="Error", message=f"No se pudo completar la petición al servidor. {e}")
            print_err(f"Un error HTTP ocurrió: {e}")
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Ocurrió un error. {e}")
            print_err(f"Ocurrió un error: {e}")



    #Buscar archivos en Drive
    @classmethod
    def search_files(cls, folder_id : str) -> list:
        creds = GoogleDriveAuth.authenticate()
        service = build('drive', 'v3', credentials=creds)

        files = []
        page_token = None

        while True:
            results = service.files().list(
                q=f"'{folder_id}' in parents",
                fields="nextPageToken, files(name, id, size, mimeType)",
                pageToken=page_token
            ).execute()

            items = results.get('files', [])
            files.extend(items)

            page_token = results.get('nextPageToken')
            if not page_token:
                break

        print_done(f"Drive: Búsqueda en {folder_id} completada")
        return files
    


    #Descargar archivos
    @classmethod
    def download_files(cls, files, progress_bar, root, done_event, label_file, path : str, progress_bar_max_steps = 0):
        
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            print(f'Error al crear la carpeta: {e}')

        # Autenticación
        creds = GoogleDriveAuth.authenticate()
        service = build('drive', 'v3', credentials=creds)

        #Preparando barra de progreso
        bar_maximun = progress_bar_max_steps
        iter_step = 1 / bar_maximun
        cls.progress_step = iter_step
        update_queue = queue.Queue()

        def download_file(file, path):
            request = service.files().get_media(fileId=file['id'])
            ruta_destino_local = os.path.join(path, file['name'])

            if not os.path.exists(ruta_destino_local):
                try:
                    with io.FileIO(ruta_destino_local, 'wb') as fh:
                        buffer_size = 5 * (1024 * 1024)  # Tamaño del búfer en bytes (5MB)
                        downloader = MediaIoBaseDownload(fh, request, chunksize=buffer_size)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                            if status:
                                print(f"Descargado {int(status.progress() * 100)}%.")
                                label_file.configure(text=f"Descargando ({int(status.progress() * 100)}%) {os.path.join(path,file["name"])}")

                    return ruta_destino_local
                except Exception as e:
                    print(f"Error al descargar {file['name']}: {e}")
                    if os.path.exists(ruta_destino_local):
                        os.remove(ruta_destino_local)
                    return None

            return ruta_destino_local

        def threaded_download():
            #total_files = len(files)
            os.makedirs(path, exist_ok=True)
            downloaded_files = 0

            for index, file in enumerate(files, start=1):

                #Si el archivo es una carpeta (LODS)
                #if file['mimeType'] == 'application/vnd.google-apps.folder':
                if file.get('mimeType') == 'application/vnd.google-apps.folder':
                    # Crear ruta y carpeta para cada dimensión (overworld, nether, etc.)
                    dimention_folder_path : str = os.path.join(path, file['name'])
                    os.mkdir(dimention_folder_path)
                    # Buscar archivos de la carpeta en Drive
                    sub_files = GoogleDriveHandler.search_files(file['id'])

                    for file in sub_files:
                        result = download_file(file, dimention_folder_path)

                else:
                    result = download_file(file, path)
                
                if result:
                    downloaded_files += 1
                    print(f'Archivo descargado en: {result}')
                else:
                    print(f'Error al descargar el archivo {file["name"]}')
                

                progress_bar.set(cls.progress_step)
                cls.progress_step += iter_step
                progress_bar.update_idletasks()

                # Enqueue progress update
                #progress_value = int((index / total_files) * 100)
                update_queue.put(cls.progress_step)

            # Signal that all files are downloaded
            done_event.set()
            label_file.configure(text=f"¡Descarga completada!")


        # Start the download process in a separate thread
        threading.Thread(target=threaded_download, daemon=True).start()

        # Periodically check the queue and update the progress bar
        def check_queue():
            try:
                while True:
                    progress_value = update_queue.get_nowait()
                    progress_bar.set(progress_value)
                    root.update_idletasks()
            except queue.Empty:
                root.after(100, check_queue)  # Check again after 100ms

        root.after(100, check_queue)  # Start checking the queue