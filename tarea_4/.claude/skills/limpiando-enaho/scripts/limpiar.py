"""Script de limpieza y procesamiento de ENAHO 2024."""
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).parents[4]
DATOS = RAIZ / "datos"
SALIDAS = RAIZ / "salidas"
SALIDAS.mkdir(exist_ok=True)

# ── 1. Leer módulos ──────────────────────────────────────────────────────────
print("Leyendo módulo 34 (sumaria)...")
llaves = {"conglome": str, "vivienda": str, "hogar": str}

sumaria = pd.read_stata(
    DATOS / "sumaria-2024.dta",
    columns=["conglome", "vivienda", "hogar", "pobreza", "ubigeo",
             "dominio", "estrato", "factor07", "mieperho"],
    convert_categoricals=False,
).astype(llaves)

print("Leyendo módulo 02 (miembros)...")
miembros = pd.read_stata(
    DATOS / "enaho01-2024-200.dta",
    columns=["conglome", "vivienda", "hogar", "ubigeo",
             "p204", "p205", "p206", "p207"],
    convert_categoricals=False,
).astype(llaves)

# ── 2. Filtrar residentes habituales ─────────────────────────────────────────
print("Filtrando residentes habituales...")
residentes = miembros[
    ((miembros.p204 == 1) & (miembros.p205 == 2)) |
    ((miembros.p204 == 2) & (miembros.p206 == 1))
].copy()

n_residentes = len(residentes)
print(f"  Residentes habituales: {n_residentes:,}")

# ── 3. Unir personas y hogares ───────────────────────────────────────────────
print("Uniendo personas y hogares...")
base = residentes.merge(
    sumaria,
    on=["conglome", "vivienda", "hogar"],
    how="left",
    validate="m:1"
)

# ── 4. Construir indicadores ─────────────────────────────────────────────────
base["area"] = base["dominio"].apply(lambda x: 1 if x <= 5 else 2)
base["pobre"] = (base["pobreza"].isin([1, 2])).astype(int)
base["dpto"] = base["ubigeo_x"].str[:2]
n_dptos = base["dpto"].nunique()

# ── 5. Estimaciones ponderadas ───────────────────────────────────────────────
print("Calculando indicadores ponderados...")
total_pond = base["factor07"].sum()
pobres_pond = base.loc[base["pobre"] == 1, "factor07"].sum()
pobreza_nacional = pobres_pond / total_pond * 100

pobreza_area = (
    base.groupby("area")
    .apply(lambda g: g.loc[g["pobre"]==1, "factor07"].sum() / g["factor07"].sum() * 100)
)

# ── 6. Guardar base procesada ────────────────────────────────────────────────
print("Guardando base procesada...")
base.to_parquet(SALIDAS / "enaho_procesada.parquet", index=False)

# ── 7. Validaciones ──────────────────────────────────────────────────────────
print("Ejecutando validaciones...")
validaciones = []

def chequear(nombre, condicion, valor_obtenido, referencia):
    estado = "✅ OK" if condicion else "❌ FALLA"
    validaciones.append(f"{estado} | {nombre}: {valor_obtenido} (ref: {referencia})")
    return condicion

chequear("Residentes habituales", abs(n_residentes - 108664) <= 500,
         f"{n_residentes:,}", "108,664")

chequear("Pobreza nacional", abs(pobreza_nacional - 27.6) <= 0.1,
         f"{pobreza_nacional:.1f}%", "27.6%")

chequear("Unidades territoriales", n_dptos == 25,
         str(n_dptos), "25")

chequear("Sin valores nulos en pobre", base["pobre"].isna().sum() == 0,
         str(base["pobre"].isna().sum()), "0")

# ── 8. Escribir validacion.txt ───────────────────────────────────────────────
texto = "\n".join([
    "=" * 50,
    "VALIDACIÓN ENAHO 2024",
    "=" * 50,
    f"Pobreza nacional:      {pobreza_nacional:.2f}%",
    f"Pobreza urbana:        {pobreza_area.get(1, 0):.2f}%",
    f"Pobreza rural:         {pobreza_area.get(2, 0):.2f}%",
    f"Residentes habituales: {n_residentes:,}",
    f"Dptos identificados:   {n_dptos}",
    "",
    "VERIFICACIONES:",
    *validaciones,
    "=" * 50,
])

(SALIDAS / "validacion.txt").write_text(texto, encoding="utf-8")
print(texto)
print("\n✅ Proceso completado.")