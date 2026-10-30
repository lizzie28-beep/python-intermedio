"""
Limpieza y organización de los datos de Amazon Mining Watch para el Perú.
"""
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ORIGINALES = RAIZ / "datos" / "originales"
PROCESADOS = RAIZ / "datos" / "procesados"
PROCESADOS.mkdir(parents=True, exist_ok=True)

# 1. Cargar los datos
df = pd.read_csv(ORIGINALES / "amw_areas_por_jurisdiccion.csv")
print("Filas totales:", len(df))

# 2. Quedarse solo con el Perú
peru = df[df["country"] == "Peru"].copy()
print("Filas del Perú:", len(peru))

# 3. Eliminar duplicados (misma jurisdicción y mismo periodo)
antes = len(peru)
peru = peru.drop_duplicates(subset=["id", "admin_year"])
print("Duplicados eliminados:", antes - len(peru))

# 4. Separar año y trimestre:  202503 -> año 2025, trimestre 3
peru["anio"] = peru["admin_year"] // 100
peru["trimestre"] = peru["admin_year"] % 100

# 5. Traducir al español los tipos de jurisdicción
tipos = {
    "national_admin": "País",
    "subnational_admin": "Departamento",
    "protected_areas": "Área protegida",
    "indigenous_territories": "Territorio indígena",
}
peru["tipo"] = peru["type"].map(tipos)

print(peru[["tipo", "name", "admin_year", "anio", "trimestre"]].head(10))
# 6. Etiqueta legible del periodo: "2024" o "2025-T3"
peru["periodo"] = peru["anio"].astype(str)
trimestral = peru["trimestre"] > 0
peru.loc[trimestral, "periodo"] = (
    peru["anio"].astype(str) + "-T" + peru["trimestre"].astype(str)
)

# 7. Limpiar los nombres: "MADRE DE DIOS" -> "Madre de Dios"
peru["nombre"] = peru["name"].str.title()
peru["nombre"] = peru["nombre"].str.replace(" - Buffer", " (zona de amortiguamiento)")

# Conectores en minúscula
for palabra in ["De", "Del", "Y"]:
    peru["nombre"] = peru["nombre"].str.replace(f" {palabra} ", f" {palabra.lower()} ")

# Tildes que faltan en la fuente original
tildes = {"Huanuco": "Huánuco", "San Martin": "San Martín",
          "Jose": "José", "Peru": "Perú"}
for sin_tilde, con_tilde in tildes.items():
    peru["nombre"] = peru["nombre"].str.replace(sin_tilde, con_tilde)

# 8. Renombrar las columnas de área a español
peru = peru.rename(columns={
    "intersected_area_ha": "nuevo_ha",
    "intersected_area_ha_cumulative": "acumulado_ha",
})

# 9. Validación: la suma de lo nuevo debe ser igual al acumulado final
suma_nuevos = peru.groupby("id")["nuevo_ha"].sum()
acumulado_final = peru.sort_values("admin_year").groupby("id")["acumulado_ha"].last()
diferencia = (suma_nuevos - acumulado_final).abs().max()
print("Diferencia máxima en la validación:", round(diferencia, 2), "ha")

# 10. Guardar la serie por periodo
columnas = ["tipo", "id", "nombre", "admin_year", "anio", "trimestre",
            "periodo", "nuevo_ha", "acumulado_ha"]
peru = peru[columnas].sort_values(["tipo", "nombre", "admin_year"])
peru.to_csv(PROCESADOS / "serie_periodos.csv", index=False)

# 11. Serie anual: suma los trimestres de 2025 y 2026
anual = peru.groupby(["tipo", "nombre", "anio"]).agg(
    nuevo_ha=("nuevo_ha", "sum"),
    acumulado_ha=("acumulado_ha", "last"),
).reset_index()
anual.to_csv(PROCESADOS / "serie_anual.csv", index=False)

print("Archivos guardados en datos/procesados/")