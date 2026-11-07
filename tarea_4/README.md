# Tarea 4 – Agente de investigación socioeconómica

## Objetivo
Agente de IA que investiga la realidad socioeconómica peruana usando datos oficiales del INEI (ENAHO 2024) y el BCRP, combinando servidores MCP y Skills de Claude Code.

**Pregunta de investigación:** ¿Cómo evolucionó la inflación peruana entre 2020 y 2024 y qué diferencias territoriales presentaba la pobreza monetaria al finalizar ese período?

---

## Arquitectura

Claude Code coordina dos fuentes de datos:
- MCP Server (BCRP): buscar_series, serie, resumen, graficar_serie
- Skills (ENAHO): limpiando-enaho, graficando-enaho, mapeando-enaho

## Herramientas MCP

| Herramienta | Función |
|---|---|
| `buscar_series` | Busca series por palabras clave |
| `serie` | Descarga datos de una serie |
| `resumen` | Calcula estadísticas (min, max, promedio, variación) |
| `graficar_serie` | Genera gráfico PNG de una serie |

## Skills

| Skill | Función |
|---|---|
| `limpiando-enaho` | Limpia ENAHO, aplica factores de expansión, valida cifras |
| `graficando-enaho` | Gráficos de pobreza por área, sexo y departamento |
| `mapeando-enaho` | Mapa coroplético de pobreza departamental |

## Datos

| Fuente | Archivo | Descarga |
|---|---|---|
| INEI ENAHO 2024 Módulo 34 | sumaria-2024.dta | [Link](https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo34.zip) |
| INEI ENAHO 2024 Módulo 02 | enaho01-2024-200.dta | [Link](https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo02.zip) |
| GeoJSON departamental | peru_departamental_simple.geojson | [Link](https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/sessions/06-geoespacial/lab/Data/peru_departamental_simple.geojson) |
| BCRP Series estadísticas | API en línea | [Link](https://estadisticas.bcrp.gob.pe/estadisticas/series/) |

## Instalación

Requisitos: Python 3.11+, uv, Claude Code

```bash
git clone https://github.com/TU_USUARIO/python-intermedio
cd python-intermedio/tarea_4
uv sync
```

## Conectar MCP a Claude Code

```bash
claude mcp add --scope project bcrp -- uv run python mcp/server.py
claude
```

## Reproducir el procesamiento

```bash
# Limpiar ENAHO
uv run python .claude/skills/limpiando-enaho/scripts/limpiar.py

# Generar gráficos
uv run python .claude/skills/graficando-enaho/scripts/graficar.py

# Generar mapa
uv run python .claude/skills/mapeando-enaho/scripts/mapear.py

# Correr pruebas MCP
cd mcp && uv run pytest -q
```

## Validación ENAHO 2024

| Indicador | Resultado | Referencia | Estado |
|---|---|---|---|
| Pobreza nacional | 27.53% | 27.6% | OK |
| Residentes habituales | 108,664 | 108,664 | OK |
| Unidades territoriales | 25 | 25 | OK |

## Evaluación del agente

| Modo | Correctas |
|---|---|
| Sin MCP/Skills | 7/10 |
| Con MCP/Skills | 10/10 |

## Limitaciones

- La inflación del BCRP corresponde a Lima Metropolitana, no al Perú nacional.
- La pobreza rural procesada difiere de la cifra oficial INEI por diferencias metodológicas.
- Los microdatos originales no se suben al repo por su tamaño.

## Evidencias de uso de IA

Las conversaciones con Claude usadas durante el desarrollo están en `evidencias_ia/`.

## Ejemplo de ejecución completa

Abrir Claude Code en `tarea_4/` y escribir:

> ¿Cómo evolucionó la inflación peruana entre 2020 y 2024 y qué diferencias territoriales presentaba la pobreza monetaria?

Claude Code usará automáticamente el MCP del BCRP y las Skills de ENAHO para responder.