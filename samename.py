import sys
import os
import re
import mimetypes

# Variables
argumentos = sys.argv
extensiones_subtitulos = ('.srt', '.sub', '.idx')
carpeta: str = ''
subtitulos = []


def salir_con_error(mensaje):
    print(mensaje)
    sys.exit(1)


# Validación de argumentos
if len(argumentos) > 2:
    salir_con_error('\nSólo se admite un argumento (carpeta de los archivos)')

try:
    carpeta = argumentos[1] if len(argumentos) == 2 else os.getcwd()
except FileNotFoundError:
    salir_con_error('No existe la carpeta')


# Funciones


def extraer_episodio(file_name: str):
    episode_regex = re.compile(r'(s\d+e\d+)|(\d+x\d+)', flags=re.IGNORECASE)
    busqueda = episode_regex.search(file_name)
    if busqueda != None:
        coincidencia = busqueda.group()
        # print('35', coincidencia, file_name)
        return [i for i in re.findall(r'\d+\d+', coincidencia)]
    else:
        print('\nNo hay archivos con el formato adecuado')
        sys.exit(1)


lista_videos = [os.path.splitext(f)[0] for f in os.listdir(
    carpeta) if 'video' in mimetypes.guess_type(f)[0]]

print(lista_videos)


def extraer_nombre_video(subtitulo: str, video: str):
    if extraer_episodio(video) == extraer_episodio(subtitulo):
        return video
    else:
        return 0


# Cambio de nombres
os.chdir(carpeta)
for index, f in enumerate(os.listdir()):
    file_name, file_ext = os.path.splitext(f)
    if file_ext in extensiones_subtitulos and len(lista_videos) > 0:
        for video in lista_videos:
            nombre_video = extraer_nombre_video(f, video)
            print('62:', f, video)
            if nombre_video and nombre_video != file_name:
                print('renombrar', file_name, 'con', nombre_video)
                nuevo_nombre = f'{nombre_video}{file_ext}'
                os.rename(f, nuevo_nombre)
                lista_videos.remove(video)
                print(f'renombrado {nuevo_nombre}', len(lista_videos))
