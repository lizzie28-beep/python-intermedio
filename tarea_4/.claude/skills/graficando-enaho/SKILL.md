# Skill: graficando-enaho

## ¿Cuándo usar esta skill?
Cuando el usuario pida gráficos o visualizaciones de indicadores de la ENAHO 2024. Si no existe la base procesada, ejecutar primero limpiando-enaho.

## ¿Qué hace esta skill?
1. Lee la base procesada de ENAHO 2024
2. Genera gráficos con estimaciones ponderadas
3. Guarda los resultados en figuras/

## Gráficos disponibles
- Pobreza por área (urbana/rural)
- Pobreza por sexo
- Pobreza por departamento

## Archivos de entrada
- salidas/enaho_procesada.parquet

## Archivos de salida
- figuras/pobreza_area.png
- figuras/pobreza_sexo.png
- figuras/pobreza_departamento.png

## ¿Cómo ejecutar?
```bash
uv run python .claude/skills/graficando-enaho/scripts/graficar.py
```