# TP4 - Análisis Técnico: Árbol AVL vs. Árbol Binario de Búsqueda (BST) común

## 1. El problema: qué pasa cuando un árbol pierde el equilibrio

Un Árbol Binario de Búsqueda (BST) común, como el implementado en TP3 (`estructuras/arbol_binario.py`), garantiza complejidad $O(\log N)$ para insertar y buscar **solo si está razonablemente balanceado** — es decir, si la diferencia de altura entre el subárbol izquierdo y el derecho de cada nodo no es muy grande.

El problema es que un BST común **no hace nada para mantenerse balanceado**. Si los datos se insertan en un orden desfavorable (por ejemplo, ya ordenados alfabéticamente), cada clave nueva termina siendo siempre mayor (o siempre menor) que la anterior, y el árbol nunca se ramifica hacia el otro lado — degenera en lo que es, en la práctica, una lista enlazada. Ahí la complejidad deja de ser $O(\log N)$ y pasa a ser $O(N)$, perdiendo toda la ventaja de usar un árbol en primer lugar.

**Mini-ejemplo concreto (el mismo que motiva este TP):** insertar títulos de canciones en orden alfabético en un BST común hace que cada título se cuelgue como hijo derecho único del anterior. Para buscar el último título insertado, hay que recorrer los $N$ nodos uno por uno — exactamente lo mismo que una búsqueda secuencial sobre una lista. El árbol existe, pero deja de cumplir su propósito.

## 2. La solución: Árbol AVL

Un árbol **AVL** (Adelson-Velsky y Landis) es un BST que, después de **cada inserción**, verifica el **factor de balance** de cada nodo (la diferencia entre la altura de su subárbol izquierdo y derecho) y, si ese factor se sale del rango $[-1, 1]$, aplica una **rotación** para corregirlo. Esto garantiza que la altura del árbol se mantenga siempre en $O(\log N)$, sin importar en qué orden lleguen los datos.

### Las 4 rotaciones

Implementadas en `estructuras/arbol_avl.py`:

| Caso | Cuándo se dispara | Qué hace |
|---|---|---|
| **Simple Derecha** (Izquierda-Izquierda) | El subárbol izquierdo está "pesado" y su propio hijo izquierdo también. | Rota el nodo hacia la derecha, subiendo al hijo izquierdo como nueva raíz local. |
| **Simple Izquierda** (Derecha-Derecha) | El subárbol derecho está "pesado" y su propio hijo derecho también. | Rota el nodo hacia la izquierda, subiendo al hijo derecho como nueva raíz local. |
| **Doble Izquierda-Derecha** | El subárbol izquierdo está pesado, pero hacia su lado derecho (forma de "zigzag"). | Primero rota el hijo izquierdo hacia la izquierda (lo convierte en caso Izquierda-Izquierda), después rota el nodo hacia la derecha. |
| **Doble Derecha-Izquierda** | El subárbol derecho está pesado, pero hacia su lado izquierdo (zigzag inverso). | Primero rota el hijo derecho hacia la derecha (lo convierte en caso Derecha-Derecha), después rota el nodo hacia la izquierda. |

**Verificación realizada:** cada una de las 4 rotaciones se probó individualmente con un caso mínimo diseñado para dispararla exactamente a ella (claves de una sola letra: `["C","B","A"]`, `["A","B","C"]`, `["C","A","B"]`, `["A","C","B"]`). Las 4 dieron como resultado exactamente 1 rotación del tipo esperado, con la clave del medio ("B") quedando como raíz — y el árbol balanceado en los 4 casos (ver `test/test_arbol_avl.py`).

## 3. Comparación BST común vs. AVL — resultados reales

Se generaron casos de desbalance (`algoritmos/generar_casos_desbalance.py`) y se corrió un benchmark completo (`benchmarks/comparacion_bst_avl.py`), midiendo altura, cantidad de comparaciones de búsqueda y tiempo real, en dos escenarios.

### Caso 1 — Peor caso: títulos insertados YA ORDENADOS alfabéticamente

| $N$ | Altura BST común | Altura AVL | Altura ideal $\log_2(N)$ | Comparaciones BST | Comparaciones AVL |
|---:|---:|---:|---:|---:|---:|
| 10 | 10 | 4 | 4 | 10 | 4 |
| 100 | 100 | 7 | 7 | 100 | 7 |
| 1.000 | **CRASH** (RecursionError) | 10 | 10 | N/A | 10 |
| 10.000 | **CRASH** (RecursionError) | 14 | 14 | N/A | 14 |

Con $N \geq 1.000$, el BST común no solo se vuelve lento: **directamente deja de funcionar**. Al insertar más de ~1.000 nodos en una cadena lineal, la inserción recursiva de Python excede el límite de recursión del intérprete y el programa termina en error. Este resultado es, en sí mismo, la prueba más contundente de por qué hace falta una estructura auto-balanceada: un BST desbalanceado no es solo una estructura ineficiente, puede ser una estructura **inutilizable** en producción.

El AVL, en cambio, mantiene la altura exactamente igual a la altura ideal ($\log_2 N$) en los 4 tamaños probados, sin excepción.

### Caso 2 — Caso normal: títulos insertados en orden ALEATORIO

| $N$ | Altura BST común | Altura AVL |
|---:|---:|---:|
| 10 | 5 | 4 |
| 100 | 11 | 8 |
| 1.000 | 21 | 12 |
| 10.000 | 32 | 16 |

Con orden de inserción aleatorio (más parecido a cómo llegarían canciones reales a un catálogo que va creciendo), el BST común **no crashea** y se mantiene razonablemente cerca del ideal logarítmico — más alto que el AVL, pero sin degenerar de forma catastrófica.

**Esto es clave para la conclusión:** el problema de desbalance no es una falla general del BST, es un riesgo específico que aparece cuando los datos llegan en (o cerca de) orden ordenado — algo que puede pasar, por ejemplo, si alguien carga un catálogo ya alfabetizado de una sola vez, en vez de insertarlo con el tiempo en orden de lanzamiento.

## 4. Análisis de complejidad

| Operación | BST común — mejor/promedio | BST común — peor caso | AVL — mejor/promedio | AVL — peor caso |
|---|---|---|---|---|
| Búsqueda | $O(\log N)$ | $O(N)$ (degenerado) | $O(\log N)$ | $O(\log N)$ (garantizado) |
| Inserción | $O(\log N)$ | $O(N)$ (degenerado) | $O(\log N)$ | $O(\log N)$ (garantizado) |
| Rotación por inserción | — (no aplica) | — | $O(1)$ por rotación, hasta $O(\log N)$ rotaciones en cascada en el camino de vuelta | — |

El AVL **garantiza** $O(\log N)$ en el peor caso para búsqueda e inserción — algo que el BST común no puede prometer. El costo de esa garantía es un trabajo extra en cada inserción: actualizar la altura de cada nodo en el camino de vuelta a la raíz y, si hace falta, aplicar una rotación. Ese trabajo extra es $O(1)$ por nivel, así que el costo total de insertar con balanceo sigue siendo $O(\log N)$ — no cambia el orden de complejidad de la inserción, solo le agrega una constante.

## 5. Integración al proyecto

El árbol AVL se implementó con la **misma interfaz pública** que el BST del TP3 (`insertar`, `buscar`, `existe`, `inorder`, `preorder`, `postorder`, `imprimir`), agregando además `altura()`, `factor_balance_raiz()` y `esta_balanceado()`. Esto permitió comparar ambas estructuras con el mismo código de pruebas y benchmark, sin duplicar lógica de testing.

Se agregó también `ArbolAVLPorTitulo`, especialización equivalente a `ArbolPorTitulo` del TP3, indexando canciones por título y agrupando versiones clásica/moderna en el mismo nodo (igual criterio que el BST común).

**Archivos agregados:**
- `estructuras/arbol_avl.py` — `NodoAVL`, `ArbolAVL`, `ArbolAVLPorTitulo`.
- `algoritmos/generar_casos_desbalance.py` — generación de casos de desbalance.
- `benchmarks/comparacion_bst_avl.py` y `benchmarks/resultados_bst_vs_avl.csv` — benchmark y resultados.
- `test/test_arbol_avl.py` — 25 tests (sumados a los 27 del BST del TP3 = 52 tests en total, todos pasando).

## 6. Conclusión técnica — ¿cuándo conviene AVL en vez de un BST común?

El AVL **no es estrictamente mejor** en todos los casos — es un trade-off:

- **Ventaja del AVL:** garantiza $O(\log N)$ en el peor caso, siempre. Si la aplicación no puede controlar en qué orden van a llegar los datos (por ejemplo, un catálogo que se carga desde una fuente externa que podría venir ordenada), el AVL elimina ese riesgo por completo.
- **Costo del AVL:** cada inserción hace trabajo extra (actualizar alturas, calcular factores de balance, posiblemente rotar). Ese costo es constante por nivel, así que no cambia el orden de complejidad, pero sí hace que cada inserción individual sea un poco más lenta que en un BST común en su mejor caso.
- **Cuándo conviene el BST común:** si se puede garantizar que los datos llegan en un orden razonablemente aleatorio (como vimos en el Caso 2), el BST común se comporta casi igual de bien que el AVL, con menos complejidad de código y menos overhead por inserción.
- **Cuándo conviene el AVL:** cuando el orden de los datos no está garantizado, o cuando las consecuencias de un desbalance son graves (como vimos: directamente un crash con $N$ grande).
