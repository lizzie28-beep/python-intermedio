#Skill: limpiando-enaho
#¿Cuándo usar esta skill
Cuando el usuario pida limpiar, procesar o preparar los datos de la ENAHO (Encuesta Nacional de Hogares) 2024, o cuando otra skill necesite la base procesada y no exista aún.
#¿Qué hace esta skill?
1. Lee los módulos 34 (sumaria) y 02 (miembros) de ENAHO 2024.
2. Normaliza nombres de las variables
3. Filtra residentes habituales
4. Une personas y hogares correctamente
5. Construye indicadores de pobreza, departamente y área
6. Aplica factores de expansión
7. Valida los resultados y genera salidas/validación.txt

## Archivos de entrada
- datos/sumaria-2024.dta → módulo 34
- datos/enaho01-2024-200.dta → módulo 02

## Archivos de salida
- salidas/enaho_procesada.parquet → base procesada
- salidas/validacion.txt → resultados de validación

## Cómo ejecutar
```bash
uv run python .claude/skills/limpiando-enaho/scripts/limpiar.py
```

## Validaciones esperadas
- Pobreza monetaria nacional ≈ 27.6%
- Residentes habituales: 108,664
- Unidades territoriales: 25
- Sin duplicados en el merge