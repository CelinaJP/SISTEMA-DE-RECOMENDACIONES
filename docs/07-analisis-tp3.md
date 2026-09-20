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

| $N$ | Secuencial (ms) | Binaria (ms) | Árbol BST (ms) |
|---:|---:|---:|---:|
| 1.000 | 0,0700 | 0,0019 | 0,0072 |
| 10.000 | 0,5698 | 0,0025 | 0,0092 |
| 100.000 | 6,0967 | 0,0032 | 0,0097 |

## 5. Análisis de complejidad
- **Búsqueda secuencial:** O(n). Recorre toda la lista en el peor caso.
- **Búsqueda binaria:** O(log n) pero exige lista ordenada (ordenar cuesta O(n log n) una sola vez).
- **Búsqueda en árbol:** O(log n) promedio si el árbol está balanceado; O(n) en el peor caso si está degenerado (como una lista).
- **Inserción en árbol:** O(log n) promedio, O(n) peor caso.
- **Recorridos (inorder, preorder, postorder):** O(n), porque visitan cada nodo 1 vez.

## 6. Conclusión
Al simular la prueba con hasta N=100.000 elementos, la búsqueda secuencial escala linealmente (llegando a ~6 ms), mientras que la búsqueda binaria y el Árbol BST se mantienen prácticamente constantes, ambos con complejidad O(log n). Es interesante notar que la binaria resultó levemente más rápida que el árbol: al trabajar sobre un array contiguo en memoria, acceder al elemento del medio es más económico que recorrer punteros entre nodos. Sin embargo, nos quedamos con el árbol BST como estructura del proyecto porque, a diferencia de la búsqueda binaria (que exige una lista ordenada, costosa de mantener ante cada inserción), el árbol permite insertar nuevas canciones dinámicamente en O(log n) sin reordenar toda la estructura.

## 7. Errores o dudas que tuvimos
Inicialmente teníamos duplicada la llamada a la interfaz en el punto de entrada, lo que impedía que se pasaran las instancias del árbol al menú. Lo resolvimos desacoplando la terminal e inyectando las estructuras directamente.

También detectamos que nuestra primera versión del script de benchmark medía una sola vez sobre el catálogo real (~120 canciones), lo cual no alcanza para mostrar la ventaja del árbol frente a la búsqueda secuencial. Lo corregimos generando datasets sintéticos a tres escalas distintas (N=1.000/10.000/100.000).