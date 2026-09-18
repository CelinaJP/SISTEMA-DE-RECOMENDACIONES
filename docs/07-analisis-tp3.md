# Análisis de Complejidad y Rendimiento — TP3

## 1. Estrategias Comparadas

1. **Búsqueda Secuencial (Lineal)**:
   - **Complejidad Temporal:** $O(n)$ en el peor caso.
   - Recorre elemento por elemento hasta hallar la coincidencia.

2. **Búsqueda Binaria**:
   - **Complejidad Temporal:** $O(\log n)$ en el peor caso.
   - Requiere una estructura previamente ordenada. Divide el espacio de búsqueda a la mitad en cada paso.

3. **Búsqueda en Árbol Binario de Búsqueda (BST)**:
   - **Complejidad Temporal:** $O(\log n)$ promedio, $O(n)$ en el peor caso (árbol desbalanceado).
   - Permite inserciones y búsquedas dinámicas eficientes sin necesidad de reordenar un arreglo completo.

## 2. Resultados Prácticos

Los tiempos exactos generados por la corrida del benchmark se encuentran exportados en `benchmarks/resultados_comparacion.csv`.

## 3. Conclusión
El uso del árbol binario de búsqueda (BST) optimiza el acceso al catálogo respecto a la búsqueda lineal tradicional, permitiendo escalar las consultas por título y artista en tiempo logarítmico.