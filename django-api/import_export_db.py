import os
from dotenv import load_dotenv
from django.core.management import call_command
import django
load_dotenv('./.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# funciones
def exportar_datos(ruta_carpeta:str, nombre_app:str, nombre_base_datos:str='production',exclude_fields:list=None,):
    """
    Exporta los datos de la base de datos especificada a un archivo .json.

    Args:
    - ruta_carpeta: Nombre de la carpeta en la que se guardarán los archivos .json sin barra al final.
    - nombre_app: Nombre de la app de la que se exportarán los datos.
    - nombre_base_datos: Nombre de la base de datos de la que se exportarán los datos. Por defecto es 'production'.
    - eliminar_carpeta: Indica si se debe eliminar la carpeta si ya existe. Por defecto es True.
    """
    try:
        # formatear ruta de carpeta quitando posiblemente barra al final
        ruta_carpeta = ruta_carpeta.rstrip('/')
        output = f"{ruta_carpeta}/{nombre_app}.json"
        # Miro si hay valores por excluir
        exclude = ','.join(exclude_fields) if exclude_fields else ''
        # Exporta los datos de la base de datos especificada a un archivo .json
        call_command('dumpdata', nombre_app, database=nombre_base_datos, output=output)
        print(f"Datos exportados exitosamente desde la base de datos '{nombre_base_datos}' a {ruta_carpeta}/{nombre_app}.json.")
        return output
    except Exception as e:
        print(f"Error al exportar datos desde la base de datos '{nombre_base_datos}': {e}")
        return f"\n{str(e)}"

def cargar_datos_json(ruta_archivo:str, nombre_base_datos:str='default'):
    """
    Carga datos desde un archivo JSON a la base de datos especificada.

    Args:
    - ruta_archivo: Ruta al archivo .json que contiene los datos a cargar.
    - nombre_base_datos: Nombre de la base de datos a la que se cargarán los datos. Por defecto es 'default'.
    """
    try:
        call_command('loaddata', ruta_archivo, database=nombre_base_datos)
        print(f"Datos cargados exitosamente desde {ruta_archivo} a la base de datos '{nombre_base_datos}'.")
    except Exception as e:
        print(f"Error al cargar datos desde {ruta_archivo}: {e}")

def convertir_a_utf8(ruta_archivo_origen, ruta_archivo_destino=None):
    """
    Lee un archivo y lo guarda con codificación UTF-8.

    Args:
    - ruta_archivo_origen: La ruta del archivo original.
    - ruta_archivo_destino: La ruta del archivo de destino en UTF-8. Si se omite, sobrescribe el archivo original.
    """
    # Si no se proporciona una ruta de archivo de destino, sobrescribe el archivo original.
    if ruta_archivo_destino is None:
        ruta_archivo_destino = ruta_archivo_origen

    # Abre el archivo original y lee su contenido.
    with open(ruta_archivo_origen, 'rb') as archivo_original:
        contenido = archivo_original.read()

    # Decodifica el contenido, asumiendo que está en la codificación original correcta.
    # Si estás seguro de la codificación original, reemplaza 'latin-1' con la codificación correcta.
    # 'latin-1' es solo un ejemplo y a menudo funciona con archivos que contienen caracteres occidentales acentuados.
    contenido_decodificado = contenido.decode('latin-1') # import chardet por si las moscas

    # Vuelve a codificar el contenido en UTF-8 y guarda el archivo.
    with open(ruta_archivo_destino, 'w', encoding='utf-8') as archivo_destino:
        archivo_destino.write(contenido_decodificado)

    print(f"Archivo convertido a UTF-8 y guardado en: {ruta_archivo_destino}")

# apps a exportar
apps_exportar = ['core_user','core_post', 'core_comment' ] # nombre app o label de app
dababases= {"export":"postgres_local", "import":"default"}

for app in apps_exportar:
    ruta_exp=exportar_datos('export', app, dababases["export"]) # importo de esa BD
    if ruta_exp:
      convertir_a_utf8(ruta_exp) # convertir a utf-8
      cargar_datos_json(ruta_exp, dababases["import"]) # exporto a esa BD
      continue
    print(f"Error al cargar datos en la base de datos: {ruta_exp}")
