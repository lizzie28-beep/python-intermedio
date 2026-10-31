"""
Para calcular indicadores claves (KPIs) y hallazgos
"""
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
PROCESADOS = RAIZ / "datos" / "procesados"

serie = pd.read_csv(PROCESADOS / "serie_periodos.csv")
ultimo = serie["admin_year"].max()          # 202603 = 2026-T3

pais = serie[serie["tipo"] == "País"]
dep = serie[serie["tipo"] == "Departamento"]

# ---------- HALLAZGO 1: la minería no se detiene y continúa avanzando en el 2026 ----------

# KPI 1: huella minera acumulada al último periodo
total = pais.loc[pais["admin_year"] == ultimo, "acumulado_ha"].iloc[0]

# KPI 2: crecimiento desde la línea base 2018
base = pais.loc[pais["admin_year"] == 201800, "acumulado_ha"].iloc[0]
crecimiento_pct = (total - base) / base * 100

# KPI 3: minería nueva de enero a setiembre, 2026 frente a 2025
ene_set_2026 = pais.loc[pais["anio"] == 2026, "nuevo_ha"].sum()
ene_set_2025 = pais.loc[(pais["anio"] == 2025) & (pais["trimestre"] <= 3), "nuevo_ha"].sum()
variacion_pct = (ene_set_2026 - ene_set_2025) / ene_set_2025 * 100

# KPI 4: departamento con más minería y su participación
dep_ultimo = dep[dep["admin_year"] == ultimo].sort_values("acumulado_ha", ascending=False)
top = dep_ultimo.iloc[0]
participacion_top = top["acumulado_ha"] / total * 100

print(f"KPI 1. Huella acumulada: {total:,.0f} ha")
print(f"KPI 2. Crecimiento desde 2018: {crecimiento_pct:.1f} %")
print(f"KPI 3. Ene-set 2026: {ene_set_2026:,.0f} ha vs. 2025: {ene_set_2025:,.0f} ha ({variacion_pct:+.1f} %)")
print(f"KPI 4. {top['nombre']} concentra el {participacion_top:.1f} %")

# ---------- HALLAZGO 2: la minería se expande fuera de Madre de Dios ----------
nuevos = dep[dep["anio"] >= 2019].copy()
nuevos["zona"] = "Otros departamentos"
nuevos.loc[nuevos["nombre"] == "Madre de Dios", "zona"] = "Madre de Dios"

por_anio = nuevos.pivot_table(index="anio", columns="zona", values="nuevo_ha", aggfunc="sum")
por_anio["% fuera de MDD"] = por_anio["Otros departamentos"] / por_anio.sum(axis=1) * 100

print("\nHALLAZGO 2. Minería nueva por año (ha):")
print(por_anio.round(1))

huanuco = dep[dep["nombre"] == "Huánuco"]
h_2018 = huanuco.loc[huanuco["admin_year"] == 201800, "acumulado_ha"].iloc[0]
h_hoy = huanuco.loc[huanuco["admin_year"] == ultimo, "acumulado_ha"].iloc[0]
print(f"Huánuco: de {h_2018:,.0f} ha en 2018 a {h_hoy:,.0f} ha hoy")

# ---------- HALLAZGO 3: existe presión sobre áreas protegidas y territorios indígenas ----------
hoy = serie[serie["admin_year"] == ultimo]

ap = hoy[hoy["tipo"] == "Área protegida"]
es_amortiguamiento = ap["nombre"].str.contains("amortiguamiento")
nucleo = ap.loc[~es_amortiguamiento, "acumulado_ha"].sum()
amortiguamiento = ap.loc[es_amortiguamiento, "acumulado_ha"].sum()

ti = hoy[hoy["tipo"] == "Territorio indígena"].sort_values("acumulado_ha", ascending=False)

print("\nHALLAZGO 3.")
print(f"Dentro de áreas protegidas: {nucleo:,.0f} ha")
print(f"En sus zonas de amortiguamiento: {amortiguamiento:,.0f} ha")
print(f"En territorios indígenas: {ti['acumulado_ha'].sum():,.0f} ha")
print(ti[["nombre", "acumulado_ha"]].head(5).to_string(index=False))