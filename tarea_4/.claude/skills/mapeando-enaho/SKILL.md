# Skill: mapeando-enaho

## Cuándo usar esta skill
Cuando el usuario pida un mapa de pobreza departamental de la ENAHO 2024.
Si no existe la base procesada, ejecutar primero limpiando-enaho.

## Qué hace
1. Lee la base procesada de ENAHO
2. Descarga el GeoJSON departamental del Perú
3. Une indicadores de pobreza con geometrías usando ubigeo
4. Genera un mapa coroplético con las 25 unidades territoriales
5. Guarda el mapa en mapas/

## Archivos de entrada
- salidas/enaho_procesada.parquet
- GeoJSON: https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/sessions/06-geoespacial/lab/Data/peru_departamental_simple.geojson

## Archivos de salida
- mapas/pobreza_departamental.png

## Cómo ejecutar
```bash
uv run python .claude/skills/mapeando-enaho/scripts/mapear.py
```