# Informe final: Inflación y pobreza monetaria en el Perú (2020–2024)

**Autor:** il.huamanm@up.edu.pe
**Fecha:** 2026-11-06

---

## 1. Pregunta de investigación

¿Cómo evolucionó la inflación peruana entre 2020 y 2024, y qué diferencias territoriales presentaba la pobreza monetaria al finalizar ese período?

La pregunta combina una dimensión macroeconómica (trayectoria temporal de precios a nivel nacional) con una dimensión microeconómica y territorial (distribución de la pobreza monetaria entre departamentos, área urbana/rural y sexo del jefe de hogar), usando el año 2024 como corte transversal de referencia.

## 2. Metodología

### 2.1 Datos de inflación
- **Fuente:** Banco Central de Reserva del Perú (BCRP), vía servidor MCP `bcrp`.
- **Serie:** `PN01273PM` — Índice de Precios al Consumidor de Lima Metropolitana, variación % a 12 meses (inflación interanual).
- **Periodo:** enero 2020 – diciembre 2024 (60 observaciones mensuales).
- **Herramientas:** `buscar_series` para localizar el código, `resumen` para estadísticos descriptivos (primer/último valor, promedio, máximo, mínimo) y `serie` para la serie mensual completa; `graficar_serie` para la visualización oficial.

### 2.2 Datos de pobreza
- **Fuente:** Encuesta Nacional de Hogares (ENAHO) 2024, INEI.
- **Insumos:** módulo 34 (Sumaria, `datos/sumaria-2024.dta`) y módulo 02 (miembros del hogar, `datos/enaho01-2024-200.dta`).
- **Procesamiento (skill `limpiando-enaho`):**
  1. Lectura de ambos módulos.
  2. Normalización de nombres de variables.
  3. Filtro de residentes habituales.
  4. Unión (merge) de personas y hogares por hogar/vivienda.
  5. Construcción de indicadores de pobreza monetaria, departamento y área, aplicando el factor de expansión `factor07` (estimaciones ponderadas, representativas de la población).
  6. Validación automática de resultados (`salidas/validacion.txt`).
- **Visualización (skill `graficando-enaho`):** gráficos ponderados de pobreza por área, por sexo y por departamento (`figuras/`).
- **Mapeo (skill `mapeando-enaho`):** unión de los indicadores departamentales con geometrías (GeoJSON departamental del Perú) por código `ubigeo`, para el mapa coroplético (`mapas/pobreza_departamental.png`).

### 2.3 Validaciones de calidad aplicadas
| Verificación | Resultado | Referencia |
|---|---|---|
| Residentes habituales | 108,664 | 108,664 |
| Pobreza nacional | 27.53% | ≈27.6% |
| Unidades territoriales | 25 | 25 |
| Valores nulos en `pobre` | 0 | 0 |

## 3. Hallazgos

### 3.1 Inflación 2020–2024
- **Ene-2020:** 1.89% (inflación baja y controlada antes de la pandemia).
- **Jun-2020:** mínimo de la serie, **1.60%**, por la contracción de demanda durante el confinamiento.
- **2021:** repunte sostenido, de 2.7% (ene) a 6.4% (dic), asociado a la recuperación de la demanda y choques de oferta.
- **2022:** aceleración hasta el **máximo de la serie, 8.81% (jun-2022)**, por el alza internacional de alimentos y energía (contexto del conflicto Rusia–Ucrania); se mantuvo sobre 8% durante casi todo el año.
- **2023:** desinflación gradual, de 8.7% (ene) a 3.2% (dic).
- **2024:** normalización adicional, cerrando en **1.97% (dic-2024)**, un nivel muy similar al de inicio de 2020.
- **Promedio del período:** 4.47%. El cambio entre el primer y el último dato es prácticamente nulo, pero encierra un ciclo completo de aceleración y desinflación entre 2021 y 2023.

*Gráfico:* `salidas/PN01273PM_2020-01_2024-12.png`

### 3.2 Pobreza monetaria 2024
- **Pobreza nacional:** 27.53%.
- **Por área:** urbana 26.97% vs. rural 27.92% — brecha urbano-rural reducida en esta base (`figuras/pobreza_area.png`).
- **Por sexo del jefe de hogar:** ver `figuras/pobreza_sexo.png`.
- **Por departamento** (brecha territorial amplia, ~39 puntos porcentuales entre extremos):

| Mayor pobreza | % | Menor pobreza | % |
|---|---|---|---|
| Cajamarca | 45.0% | Ica | 5.9% |
| Loreto | 42.6% | Moquegua | 10.9% |
| Puno | 40.4% | Madre de Dios | 11.1% |
| Huánuco | 39.5% | Lambayeque | 14.1% |
| Pasco | 39.3% | Arequipa | 15.8% |

*Gráfico:* `figuras/pobreza_departamento.png` · *Mapa:* `mapas/pobreza_departamental.png`

## 4. Interpretación

El ciclo inflacionario 2020-2024 describe una "U invertida" completa: partió de niveles bajos pre-pandemia, cayó aún más por el shock de demanda de 2020, y luego subió con fuerza durante 2021-2022 por la combinación de recuperación económica interna y choques externos de oferta (alimentos y energía), alcanzando su pico en junio de 2022. La posterior desinflación de 2023-2024 devolvió la serie a niveles similares a los de 2020, lo que sugiere que, pese al episodio inflacionario, el Perú cerró el período con una inflación nuevamente controlada y dentro del rango meta del BCRP.

Sin embargo, esa estabilidad macroeconómica de cierre de período convive con una fuerte heterogeneidad territorial en la pobreza monetaria: departamentos de la sierra y selva (Cajamarca, Loreto, Puno, Huánuco, Pasco) muestran tasas de pobreza entre 39% y 45%, mientras que departamentos de la costa sur (Ica, Moquegua, Arequipa) registran tasas de un dígito o poco más de 15%. Esto indica que la trayectoria agregada de precios —aunque relevante para el poder adquisitivo de todos los hogares— no es suficiente para explicar ni corregir las brechas estructurales de pobreza entre regiones, las cuales responden más a factores de productividad, acceso a mercados, infraestructura y composición económica regional que a la dinámica de corto plazo del IPC de Lima Metropolitana.

Un hallazgo notable es que la brecha urbano-rural nacional (26.97% vs. 27.92%) es mucho menor que la brecha interdepartamental (~39 p.p.), lo que sugiere que, en 2024, el eje territorial (departamento) es más determinante de la pobreza monetaria que el eje urbano/rural por sí solo.

## 5. Limitaciones

1. **Desfase geográfico de la inflación:** la serie del BCRP utilizada (`PN01273PM`) mide el IPC de **Lima Metropolitana**, no un índice de precios nacional ni departamental; por lo tanto, no permite vincular directamente la dinámica de precios con las diferencias de pobreza observadas en otros departamentos.
2. **Comparación temporal asimétrica:** la inflación se analiza como serie 2020-2024, mientras que la pobreza se analiza solo para el corte 2024, por lo que no se puede establecer causalidad ni evolución conjunta año a año de ambas variables.
3. **Datos de pobreza de una sola ronda:** al usar únicamente ENAHO 2024, no se observa si las brechas departamentales se ampliaron o redujeron durante el episodio inflacionario 2021-2023.
4. **Posibles particularidades de la base procesada:** algunos resultados departamentales (p. ej. Callao en 33.8%) difieren de patrones históricos típicamente reportados por el INEI para esa región, lo que podría reflejar particularidades del diseño muestral, factores de expansión o del subconjunto de datos `.dta` utilizado en este ejercicio; se recomienda contrastar con los reportes oficiales de pobreza del INEI antes de usar estas cifras departamentales fuera de este contexto académico.
5. **Indicador de pobreza binario:** el análisis usa la variable `pobre` (pobre/no pobre) y no profundiza en la brecha o severidad de la pobreza (FGT1, FGT2), que podría matizar las diferencias territoriales encontradas.
6. **Incidencia en consola (Windows):** los scripts de las skills `limpiando-enaho` y `graficando-enaho` imprimen caracteres Unicode (✅) que generan `UnicodeEncodeError` en la consola por defecto de Windows (cp1252); esto no afecta los archivos de salida, pero requiere forzar `PYTHONIOENCODING=utf-8` al ejecutar.

## 6. Reproducibilidad

### 6.1 Requisitos
- Entorno gestionado con `uv` (ver `pyproject.toml` y `uv.lock`).
- Servidor MCP `bcrp` configurado en `.mcp.json`.
- Archivos de datos ENAHO 2024 en `datos/`: `sumaria-2024.dta`, `enaho01-2024-200.dta`.

### 6.2 Pasos

```bash
# 1. Inflación (BCRP, vía MCP) — ejecutado interactivamente con el servidor mcp__bcrp
#    buscar_series("inflación", frecuencia="mensual")
#    resumen("PN01273PM", "2020-01", "2024-12")
#    serie("PN01273PM", "2020-01", "2024-12")
#    graficar_serie("PN01273PM", "2020-01", "2024-12", titulo="Inflación interanual Perú 2020-2024")
#    → genera salidas/PN01273PM_2020-01_2024-12.png

# 2. Limpieza de pobreza ENAHO 2024
PYTHONIOENCODING=utf-8 uv run python .claude/skills/limpiando-enaho/scripts/limpiar.py
# → salidas/enaho_procesada.parquet, salidas/validacion.txt

# 3. Gráficos de pobreza
PYTHONIOENCODING=utf-8 uv run python .claude/skills/graficando-enaho/scripts/graficar.py
# → figuras/pobreza_area.png, figuras/pobreza_sexo.png, figuras/pobreza_departamento.png

# 4. Mapa departamental
PYTHONIOENCODING=utf-8 uv run python .claude/skills/mapeando-enaho/scripts/mapear.py
# → mapas/pobreza_departamental.png
```

### 6.3 Trazabilidad de resultados citados en este informe
- Serie BCRP: código `PN01273PM`, consultada el 2026-11-05, fuente oficial `https://estadisticas.bcrp.gob.pe/estadisticas/series/`.
- Validación ENAHO: `salidas/validacion.txt` (generado 2026-11-05).
- Cifras departamentales de pobreza: calculadas como promedio ponderado por `factor07` de la variable `pobre` sobre `salidas/enaho_procesada.parquet`, agrupado por `dpto` y unido a nombres de departamento mediante el GeoJSON departamental usado en `mapeando-enaho` (correspondencia por código `ubigeo`/`FIRST_IDDP`).

### 6.4 Archivos generados
| Archivo | Contenido |
|---|---|
| `salidas/PN01273PM_2020-01_2024-12.png` | Gráfico de inflación interanual 2020-2024 (BCRP) |
| `salidas/enaho_procesada.parquet` | Base ENAHO 2024 procesada y ponderada |
| `salidas/validacion.txt` | Validaciones automáticas de la limpieza |
| `figuras/pobreza_area.png` | Pobreza por área urbana/rural |
| `figuras/pobreza_sexo.png` | Pobreza por sexo del jefe de hogar |
| `figuras/pobreza_departamento.png` | Pobreza por departamento (barras) |
| `mapas/pobreza_departamental.png` | Mapa coroplético de pobreza departamental |
| `informes/informe_final.md` | Este informe |
