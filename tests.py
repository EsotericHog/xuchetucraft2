#import nbtlib
#
## Ruta al archivo servers.dat
#file_path = r"C:\Users\juanc\AppData\Roaming\.minecraft\servers.dat"
#
## Carga el archivo NBT
#nbt_file = nbtlib.load(file_path)
#
## Imprime el contenido del archivo para revisión
#print(nbt_file)

import json
import re

# Cargar el JSON desde un archivo o una cadena
json_data = '''
{
  "profiles" : {
    "fabric-loader-1.20.1" : {
      "created" : "2024-08-12T15:00:49.000Z",
      "icon" : "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACABAMAAAAxEHz4AAAAGFBMVEUAAAA4NCrb0LTGvKW8spyAem2uppSakn5SsnMLAAAAAXRSTlMAQObYZgAAAJ5JREFUaIHt1MENgCAMRmFWYAVXcAVXcAVXcH3bhCYNkYjcKO8dSf7v1JASUWdZAlgb0PEmDSMAYYBdGkYApgf8ER3SbwRgesAf0BACMD1gB6S9IbkEEBfwY49oNj4lgLhA64C0o9R9RABTAvp4SX5kB2TA5y8EEAK4pRrxB9QcA4QBWkj3GCAMUCO/xwBhAI/kEsCagCHDY4AwAC3VA6t4zTAMj0OJAAAAAElFTkSuQmCC",
      "javaArgs" : "-Xmx8G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M",
      "lastUsed" : "2024-08-18T15:45:04.992Z",
      "lastVersionId" : "fabric-loader-0.16.0-1.20.1",
      "name" : "fabric-loader-1.20.1",
      "type" : "custom"
    }
  },
  "settings" : {
    "crashAssistance" : true,
    "enableAdvanced" : false,
    "enableAnalytics" : true,
    "enableHistorical" : false,
    "enableReleases" : true,
    "enableSnapshots" : false,
    "keepLauncherOpen" : false,
    "profileSorting" : "ByLastPlayed",
    "showGameLog" : false,
    "showMenu" : false,
    "soundOn" : false
  },
  "version" : 3
}
'''

# Parsear el JSON
data = json.loads(json_data)

# Acceder al perfil específico
profile = data['profiles']['fabric-loader-1.20.1']

# Obtener el valor de "javaArgs"
java_args = profile['javaArgs']

# Buscar el valor de la RAM usando una expresión regular
match = re.search(r'-Xmx(\d+)G', java_args)
if match:
    ram_value = match.group(1)
    print(f"El valor de la RAM es: {ram_value} GB")
else:
    print("No se encontró el valor de la RAM.")


print(int(15.80))