"""
Descarga los datos originales de Amazon Mining Watch (licencia CC BY 4.0).
Fuente: https://github.com/earthrise-media/mining-detector
"""
from pathlib import Path
import urllib.request

# Carpeta donde se guardarán los archivos: tarea_3/datos/originales/
RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "datos" / "originales"
DESTINO.mkdir(parents=True, exist_ok=True)

# Parte de la dirección web que comparten los dos archivos
BASE = "https://raw.githubusercontent.com/earthrise-media/mining-detector/main/data/public"

# Lista de archivos:  "nombre con el que se guarda": "dirección web"
ARCHIVOS = {
    "amw_areas_por_jurisdiccion.csv": f"{BASE}/mined_areas_by_jurisdiction.csv",
    "amw_ilegalidad_por_jurisdiccion.csv": f"{BASE}/illegality_analysis_by_jurisdiction.csv",
        "peru_departamental.geojson": "https://raw.githubusercontent.com/juaneladio/peru-geojson/master/peru_departamental_simple.geojson",
}

# Descargar cada archivo de la lista
for nombre, url in ARCHIVOS.items():
    ruta = DESTINO / nombre
    print("Intentando:", url)
    urllib.request.urlretrieve(url, ruta)
    print("Descargado:", nombre)