"""Script de mapa coroplético de pobreza departamental ENAHO 2024."""
from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).parents[4]
SALIDAS = RAIZ / "salidas"
MAPAS = RAIZ / "mapas"
MAPAS.mkdir(exist_ok=True)

GEOJSON_URL = "https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/sessions/06-geoespacial/lab/Data/peru_departamental_simple.geojson"

# ── 1. Leer base procesada ───────────────────────────────────────────────────
print("Leyendo base procesada...")
base = pd.read_parquet(SALIDAS / "enaho_procesada.parquet")

# ── 2. Calcular pobreza por departamento ─────────────────────────────────────
print("Calculando pobreza por departamento...")
pob_dpto = (
    base.groupby("dpto")
    .apply(lambda g: g.loc[g["pobre"]==1, "factor07"].sum() / g["factor07"].sum() * 100)
    .reset_index(name="pobreza_pct")
    .rename(columns={"dpto": "ubigeo"})
)
print(f"  Departamentos calculados: {len(pob_dpto)}")

# ── 3. Leer GeoJSON ──────────────────────────────────────────────────────────
print("Leyendo GeoJSON departamental...")
geo = gpd.read_file(GEOJSON_URL)
print(f"  Columnas GeoJSON: {list(geo.columns)}")
print(f"  Unidades en GeoJSON: {len(geo)}")

# ── 4. Unir por código departamental ─────────────────────────────────────────
print("Uniendo datos con geometrías...")
# usar FIRST_IDDP como llave
geo["ubigeo"] = geo["FIRST_IDDP"].astype(str).str.zfill(2)
merged = geo.merge(pob_dpto, on="ubigeo", how="left")
print(f"  Unidades con datos: {merged['pobreza_pct'].notna().sum()}/25")

# ── 5. Generar mapa ──────────────────────────────────────────────────────────
print("Generando mapa...")
fig, ax = plt.subplots(figsize=(10, 12))

merged.plot(
    column="pobreza_pct",
    ax=ax,
    cmap="YlOrRd",
    legend=True,
    legend_kwds={"label": "Pobreza monetaria (%)", "shrink": 0.6},
    missing_kwds={"color": "lightgrey", "label": "Sin datos"},
    edgecolor="white",
    linewidth=0.5
)

ax.set_title("Pobreza monetaria por departamento\nPerú 2024", 
             fontsize=14, fontweight="bold", pad=15)
ax.axis("off")
ax.text(0.01, 0.01, "Fuente: INEI - ENAHO 2024", transform=ax.transAxes,
        fontsize=8, ha="left", va="bottom", color="gray")

plt.tight_layout()
plt.savefig(MAPAS / "pobreza_departamental.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✅ mapas/pobreza_departamental.png")
print("\n✅ Mapa generado.")