# Auditoría de integración MCP + Skills

**Fecha:** 6 de noviembre de 2026
**Pregunta:** ¿Cómo evolucionó la inflación peruana entre 2020 y 2024 y qué diferencias territoriales presentaba la pobreza monetaria al finalizar ese período?

## Herramientas utilizadas

- MCP del BCRP: buscar_series, serie, resumen (3 llamadas)
- Skill: limpiando-enaho
- Skill: graficando-enaho

## Log de ejecución

Read 2 files, called bcrp 3 times, ran 4 shell commands

Skill(limpiando-enaho) - Successfully loaded skill
Read 1 file, ran 2 shell commands

Skill(graficando-enaho) - Successfully loaded skill
Ran 2 shell commands

Called MCP, ran 1 shell command

## Resultados obtenidos

### Inflación BCRP (serie PN01273PM)
- Ene-2020: 1.89%
- Mínimo pandemia: 1.60% (jun-2020)
- Máximo: 8.81% (jun-2022)
- Dic-2024: 1.97%
- Promedio 2020-2024: 4.47%

### Pobreza ENAHO 2024 (Skills)
- Pobreza nacional: 27.53% (ref: 27.6%)
- Pobreza urbana: 26.97%
- Pobreza rural: 27.92%
- Residentes habituales: 108,664
- Unidades territoriales: 25

### Top 5 departamentos más pobres
1. Cajamarca: 45.0%
2. Loreto: 42.6%
3. Puno: 40.4%
4. Huánuco: 39.5%
5. Pasco: 39.3%

## Salidas generadas
- figuras/pobreza_area.png
- figuras/pobreza_sexo.png
- figuras/pobreza_departamento.png
- mapas/pobreza_departamental.png
- salidas/validacion.txt
- salidas/enaho_procesada.parquet
- salidas/PN01273PM_2020-01_2024-12.png

## Conclusión
El agente utilizó correctamente el MCP del BCRP y las Skills de ENAHO
en una misma ejecución, combinando datos macroeconómicos oficiales
con microdatos de hogares para responder la pregunta de investigación.