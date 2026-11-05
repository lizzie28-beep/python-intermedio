"""Script de visualización de indicadores ENAHO 2024."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

RAIZ = Path(__file__).parents[4]
SALIDAS = RAIZ / "salidas"
FIGURAS = RAIZ / "figuras"
FIGURAS.mkdir(exist_ok=True)

# ── Leer base procesada ──────────────────────────────────────────────────────
print("Leyendo base procesada...")
base = pd.read_parquet(SALIDAS / "enaho_procesada.parquet")

FUENTE = "Fuente: INEI - ENAHO 2024"

def pobreza_ponderada(df, grupo):
    return (
        df.groupby(grupo)
        .apply(lambda g: g.loc[g["pobre"]==1, "factor07"].sum() / g["factor07"].sum() * 100)
        .reset_index(name="pobreza_pct")
    )

# ── Gráfico 1: Pobreza por área ──────────────────────────────────────────────
print("Generando gráfico 1: pobreza por área...")
pob_area = pobreza_ponderada(base, "area")
pob_area["area_label"] = pob_area["area"].map({1: "Urbana", 2: "Rural"})

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(pob_area["area_label"], pob_area["pobreza_pct"],
              color=["#2196F3", "#FFC107"], width=0.5)
ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=12)
ax.set_title("Pobreza monetaria por área geográfica\nPerú 2024", fontsize=14, fontweight="bold")
ax.set_ylabel("Porcentaje de población pobre (%)")
ax.set_ylim(0, 60)
ax.text(0.99, 0.01, FUENTE, transform=ax.transAxes,
        fontsize=8, ha="right", va="bottom", color="gray")
plt.tight_layout()
plt.savefig(FIGURAS / "pobreza_area.png", dpi=150)
plt.close()
print("  ✅ figuras/pobreza_area.png")

# ── Gráfico 2: Pobreza por sexo ──────────────────────────────────────────────
print("Generando gráfico 2: pobreza por sexo...")
pob_sexo = pobreza_ponderada(base, "p207")
pob_sexo["sexo_label"] = pob_sexo["p207"].map({1: "Hombre", 2: "Mujer"})

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(pob_sexo["sexo_label"], pob_sexo["pobreza_pct"],
              color=["#1565C0", "#C62828"], width=0.5)
ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=12)
ax.set_title("Pobreza monetaria por sexo\nPerú 2024", fontsize=14, fontweight="bold")
ax.set_ylabel("Porcentaje de población pobre (%)")
ax.set_ylim(0, 50)
ax.text(0.99, 0.01, FUENTE, transform=ax.transAxes,
        fontsize=8, ha="right", va="bottom", color="gray")
plt.tight_layout()
plt.savefig(FIGURAS / "pobreza_sexo.png", dpi=150)
plt.close()
print("  ✅ figuras/pobreza_sexo.png")

# ── Gráfico 3: Pobreza por departamento ──────────────────────────────────────
print("Generando gráfico 3: pobreza por departamento...")
pob_dpto = pobreza_ponderada(base, "dpto").sort_values("pobreza_pct", ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(pob_dpto["dpto"], pob_dpto["pobreza_pct"], color="#1565C0")
ax.set_title("Pobreza monetaria por departamento\nPerú 2024", fontsize=14, fontweight="bold")
ax.set_xlabel("Porcentaje de población pobre (%)")
ax.axvline(x=27.5, color="red", linestyle="--", linewidth=1.5, label="Promedio nacional")
ax.legend()
ax.text(0.99, 0.01, FUENTE, transform=ax.transAxes,
        fontsize=8, ha="right", va="bottom", color="gray")
plt.tight_layout()
plt.savefig(FIGURAS / "pobreza_departamento.png", dpi=150)
plt.close()
print("  ✅ figuras/pobreza_departamento.png")

print("\n✅ Gráficos generados en figuras/")