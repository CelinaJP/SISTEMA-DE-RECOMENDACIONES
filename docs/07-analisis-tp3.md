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
## 4. Comparación de tiempos
En la tabla siguiente, los tiempos son **reales**, sacados con nuestro script `benchmarks/comparacion_busqueda.py` (los resultados se exportan a `benchmarks/resultados_comparacion.csv`).

| Métrica / Estrategia | Secuencial (ms) | Binaria (ms) | Árbol BST (ms) |
|---|---:|---:|---:|
| Tiempo de búsqueda | 0.00325 | 0.00197 | 0.00464 |

## 5. Análisis de complejidad
- **Búsqueda secuencial:** O(n). Recorre toda la lista en el peor caso.
- **Búsqueda binaria:** O(log n) pero exige lista ordenada (ordenar cuesta O(n log n) una sola vez).
- **Búsqueda en árbol:** O(log n) promedio si el árbol está balanceado; O(n) en el peor caso si está degenerado (como una lista).
- **Inserción en árbol:** O(log n) promedio, O(n) peor caso.
- **Recorridos (inorder, preorder, postorder):** O(n), porque visitan cada nodo 1 vez.

## 6. Conclusión
Si bien nuestro catálogo real de canciones de Miranda! es más acotado, al simular la prueba con hasta 100.000 elementos observamos que la búsqueda secuencial escala linealmente tardando 7.84 ms, mientras que el Árbol BST mantiene un rendimiento de 0.0089 ms. Por lo tanto, nos quedamos con el árbol BST porque resulta óptimo a medida que el catálogo crece; el costo de construir la estructura se paga una sola vez al cargar la aplicación y luego las búsquedas son inmediatas.

## 7. Errores o dudas que tuvimos
Inicialmente teníamos duplicada la llamada a la interfaz en el punto de entrada, lo que impedía que se pasaran las instancias del árbol al menú. Lo resolvimos desacoplando la terminal e inyectando las estructuras directamente.