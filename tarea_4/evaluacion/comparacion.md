# Comparación Modo A vs Modo B

## Resumen de resultados

| Modo | Respuestas correctas | Incorrectas | Parciales |
|------|---------------------|-------------|-----------|
| A (sin MCP/Skills) | 7/10 | 2 | 1 |
| B (con MCP/Skills) | 10/10 | 0 | 0 |

## Análisis por pregunta

### Preguntas que mejoraron con MCP/Skills

- **Pregunta 3 (promedio inflación):** Modo A usó cierres anuales (4.41%), Modo B calculó el promedio mensual exacto (4.47%) via MCP.
- **Pregunta 6 (residentes habituales):** Modo A no encontró la cifra. Modo B respondió 108,664 exacto via Skill.
- **Pregunta 8 (pobreza urbana):** Modo A dio 24.8% (cifra oficial INEI). Modo B dio 26.97% calculado directamente desde los microdatos ENAHO.

### Preguntas correctas en ambos modos

- Preguntas 1, 2, 4, 5, 7, 9, 10: correctas en ambos modos, aunque Modo B fue más preciso y rápido.

## Tiempo de ejecución

- Modo A: ~50 segundos por pregunta (búsqueda web)
- Modo B: ~10 segundos por pregunta (MCP directo)

## Errores encontrados

- Modo A pregunta 6: no encontró cifra de residentes habituales en fuentes web.
- Modo A pregunta 8: diferencia metodológica (cifra oficial INEI vs microdatos procesados).
- Modo A pregunta 3: usó promedio de cierres anuales en vez de promedio mensual.

## Conclusión

El uso de MCP y Skills mejoró la precisión de 7/10 a 10/10. Las principales ventajas fueron:
1. Acceso directo a datos oficiales del BCRP sin búsqueda web.
2. Cálculos reproducibles desde microdatos ENAHO.
3. Mayor velocidad y precisión en las respuestas.
4. Trazabilidad completa de cada cifra hasta su fuente.