"""Servidor MCP del BCRP."""
import re
import time
import unicodedata
from functools import cache
from pathlib import Path

import httpx
import pandas as pd
import requests
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

AQUI = Path(__file__).parent
CATALOGO = AQUI / "datos" / "catalogo_bcrp.csv"
URL_CATALOGO = "https://estadisticas.bcrp.gob.pe/estadisticas/series/metadata"
API = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
SOLO_LECTURA = {"readOnlyHint": True, "openWorldHint": True}

mcp = FastMCP("bcrp", instructions=(
    "Series oficiales del Banco Central de Reserva del Perú (BCRP). Primero busca el código con buscar_series; "
    "luego usa resumen para variaciones, promedios y extremos, y serie para los datos. No calcules a mano: "
    "cita siempre el código de la serie y el periodo."))


def _sin_tildes(s):
    return unicodedata.normalize("NFD", str(s).lower()).encode("ascii", "ignore").decode()


@cache
def catalogo():
    if not CATALOGO.exists():
        CATALOGO.parent.mkdir(exist_ok=True)
        r = httpx.get(URL_CATALOGO, timeout=120)
        r.raise_for_status()
        CATALOGO.write_text(r.content.decode("latin-1"), encoding="utf-8")
    df = pd.read_csv(CATALOGO, sep=";", dtype=str).fillna("")
    df = df.rename(columns={"Código de serie": "codigo", "Categoría de serie": "categoria",
                            "Grupo de serie": "grupo", "Nombre de serie": "nombre",
                            "Frecuencia": "frecuencia", "Fecha de actualización": "actualizada",
                            "Fecha de inicio": "inicio"})
    df["texto"] = (df.categoria + " " + df.grupo + " " + df.nombre).map(_sin_tildes)
    return df


def _ficha(codigo):
    fila = catalogo().query("codigo == @codigo")
    if fila.empty:
        raise ToolError(f"No existe el código de serie {codigo!r}. Búsquenlo con buscar_series.")
    f = fila.iloc[0]
    return {"codigo": f.codigo, "nombre": f"{f.grupo} - {f.nombre}", "categoria": f.categoria,
            "frecuencia": f.frecuencia, "inicio": f.inicio, "actualizada": f.actualizada}


def _sesion_bcrp():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://estadisticas.bcrp.gob.pe/estadisticas/series/",
    })
    return s


@mcp.tool(annotations=SOLO_LECTURA)
def buscar_series(texto: str, frecuencia: str | None = None, limite: int = 10) -> list[dict]:
    """Busca series del BCRP por palabras clave."""
    df = catalogo()
    m = pd.Series(True, index=df.index)
    for palabra in _sin_tildes(texto).split():
        m &= df.texto.str.contains(re.escape(palabra))
    if frecuencia:
        m &= df.frecuencia.str.lower() == frecuencia.lower()
    sel = df[m]
    orden = sel.assign(vieja=sel.actualizada < "2025", largo=(sel.grupo + sel.nombre).str.len())
    return [_ficha(c) for c in orden.sort_values(["vieja", "largo"]).head(limite).codigo]


@mcp.tool(annotations=SOLO_LECTURA)
def serie(codigo: str, desde: str, hasta: str) -> dict:
    """Descarga los datos de una serie oficial del BCRP para un período determinado."""
    ficha = _ficha(codigo)

    def _fecha_api(fecha, freq):
        if "mensual" in freq or "trimestral" in freq:
            partes = fecha.split("-")
            if len(partes) == 2:
                return f"{partes[0]}-{int(partes[1])}"
        return fecha

    freq = ficha["frecuencia"].lower()
    desde_api = _fecha_api(desde, freq)
    hasta_api = _fecha_api(hasta, freq)
    url = f"{API}/{codigo}/json/{desde_api}/{hasta_api}"

    sesion = _sesion_bcrp()
    payload = None
    for intento in range(3):
        r = sesion.get(url, timeout=30)
        r.raise_for_status()
        try:
            payload = r.json()
            break
        except Exception:
            time.sleep(3 + intento * 2)

    if payload is None:
        raise ToolError(f"La API no respondió JSON para {codigo!r}. Intente más tarde.")

    if "errorType" in payload:
        raise ToolError(f"Código {codigo!r} no encontrado en la API del BCRP.")

    def _parsear_periodo(nombre):
        meses = {"ene":"01","feb":"02","mar":"03","abr":"04","may":"05","jun":"06",
                 "jul":"07","ago":"08","set":"09","sep":"09","oct":"10","nov":"11","dic":"12"}
        n = nombre.lower()
        partes = n.split(".")
        # diaria: "01.Oct.26" → 3 partes
        if len(partes) == 3:
            dia = partes[0].zfill(2)
            mes = meses.get(partes[1], "01")
            anio = partes[2] if len(partes[2]) == 4 else f"20{partes[2].zfill(2)}"
            return f"{anio}-{mes}-{dia}"
        # trimestral: "T1.25"
        if len(partes) == 2 and partes[0].startswith("t"):
            trim = partes[0].replace("t","")
            anio = partes[1] if len(partes[1]) == 4 else f"20{partes[1].zfill(2)}"
            return f"{anio}-T{trim}"
        # mensual: "Ene.2025"
        if len(partes) == 2:
            mes = meses.get(partes[0], "01")
            anio = partes[1] if len(partes[1]) == 4 else f"20{partes[1].zfill(2)}"
            return f"{anio}-{mes}"
        return nombre

    datos = []
    for p in payload.get("periods", []):
        v = p["values"][0]
        if v == "n.d.":
            continue
        datos.append({"periodo": _parsear_periodo(p["name"]), "valor": float(v)})

    return {
        "codigo": ficha["codigo"],
        "nombre": ficha["nombre"],
        "frecuencia": ficha["frecuencia"],
        "datos": datos,
        "fuente": "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    }


@mcp.tool(annotations=SOLO_LECTURA)
def resumen(codigo: str, desde: str, hasta: str) -> dict:
    """Calcula estadísticas de una serie: primer y último valor, variación, promedio, máximo y mínimo."""
    resultado = serie(codigo, desde, hasta)
    valores = resultado["datos"]

    if not valores:
        raise ToolError(f"No hay datos para {codigo!r} entre {desde} y {hasta}.")

    primero = valores[0]
    ultimo = valores[-1]
    nums = [d["valor"] for d in valores]
    cambio = ultimo["valor"] - primero["valor"]
    variacion_pct = (cambio / primero["valor"]) * 100 if primero["valor"] != 0 else None
    idx_max = nums.index(max(nums))
    idx_min = nums.index(min(nums))

    return {
        "codigo": codigo,
        "nombre": resultado["nombre"],
        "frecuencia": resultado["frecuencia"],
        "desde": desde,
        "hasta": hasta,
        "primero": primero,
        "ultimo": ultimo,
        "cambio": round(cambio, 4),
        "variacion_pct": round(variacion_pct, 2) if variacion_pct is not None else None,
        "promedio": round(sum(nums) / len(nums), 4),
        "maximo": {"valor": valores[idx_max]["valor"], "periodo": valores[idx_max]["periodo"]},
        "minimo": {"valor": valores[idx_min]["valor"], "periodo": valores[idx_min]["periodo"]},
        "fuente": "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    }


@mcp.tool(annotations=SOLO_LECTURA)
def graficar_serie(codigo: str, desde: str, hasta: str, titulo: str | None = None) -> dict:
    """Genera y guarda un gráfico de línea de una serie oficial del BCRP en salidas/."""
    import matplotlib.pyplot as plt

    datos = serie(codigo, desde, hasta)
    if not datos["datos"]:
        raise ToolError(f"No hay datos para graficar {codigo!r} en {desde} - {hasta}.")

    periodos = [d["periodo"] for d in datos["datos"]]
    valores = [d["valor"] for d in datos["datos"]]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(periodos, valores, linewidth=2, color="#003087")
    ax.set_title(titulo or datos["nombre"], fontsize=13, fontweight="bold")
    ax.set_xlabel("Período")
    ax.set_ylabel(datos["nombre"])

    paso = max(1, len(periodos) // 12)
    ax.set_xticks(range(0, len(periodos), paso))
    ax.set_xticklabels(periodos[::paso], rotation=45, ha="right")
    ax.text(0.99, 0.01, "Fuente: BCRP", transform=ax.transAxes,
            fontsize=8, ha="right", va="bottom", color="gray")

    plt.tight_layout()
    salidas = AQUI.parent / "salidas"
    salidas.mkdir(exist_ok=True)
    ruta = salidas / f"{codigo}_{desde}_{hasta}.png".replace("/", "-")
    plt.savefig(ruta, dpi=150)
    plt.close()

    return {
        "codigo": codigo,
        "nombre": datos["nombre"],
        "archivo": str(ruta),
        "periodos_graficados": len(periodos),
        "fuente": "https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    }


@mcp.resource("bcrp://serie/{codigo}")
def recurso_serie(codigo: str) -> str:
    """Devuelve la ficha descriptiva de una serie oficial del BCRP."""
    ficha = _ficha(codigo)
    return (
        f"Código: {ficha['codigo']}\n"
        f"Nombre: {ficha['nombre']}\n"
        f"Categoría: {ficha['categoria']}\n"
        f"Frecuencia: {ficha['frecuencia']}\n"
        f"Inicio de datos: {ficha['inicio']}\n"
        f"Última actualización: {ficha['actualizada']}\n"
        f"Fuente: https://estadisticas.bcrp.gob.pe/estadisticas/series/"
    )


@mcp.prompt()
def informe(tema: str) -> str:
    """Genera un prompt para elaborar un informe sobre un indicador del BCRP."""
    return (
        f"Elabora un informe breve sobre {tema} usando exclusivamente datos oficiales del BCRP. "
        f"Para cada cifra que menciones debes: "
        f"1) Citar el código exacto de la serie usada. "
        f"2) Indicar el período al que corresponde. "
        f"3) Especificar si el valor es mensual, trimestral o anual. "
        f"Usa primero buscar_series para encontrar los códigos correctos, "
        f"luego resumen para obtener las estadísticas. "
        f"No calcules cifras a mano ni las inventes. "
        f"Al final indica la fecha de actualización de cada serie consultada."
    )


if __name__ == "__main__":
    mcp.run()