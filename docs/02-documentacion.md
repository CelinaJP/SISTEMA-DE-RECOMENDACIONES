# Documentación del Proyecto

## TP0

## TP1

## TP2 - Análisis de complejidad y justificación: Estrategia de Búsqueda por Género Musical

## 1. Definición del Problema

Dentro del sistema **"EL BOT DE TU CORAZÓN"** (Catálogo y Recomendador de Miranda!), una de las operaciones con mayor frecuencia de ejecución es la **Búsqueda de Canciones por Género Musical** (por ejemplo: *Electropop, Pop Latino, Disco, Synth-pop, Urban Pop*).

En catálogos extensos con miles de canciones, versiones clásicas y re-versiones, filtrar por género elemento por elemento vuelve al sistema lento e ineficiente.

---

## 2. Estrategias Implementadas

- **A. Búsqueda Secuencial - Lista Enlazada:** Recorrido lineal elemento a elemento desde el inicio de la lista de géneros/canciones hasta encontrar las coincidencias del género solicitado.
- **B. Árbol Binario de Búsqueda (ABB):** Estructura jerárquica con nodos indexados y ordenados alfabéticamente por el nombre del género, que permite descartar la mitad del espacio de búsqueda en cada comparación y recuperar la lista de canciones asociada a dicho género.

---

## 3. Experimentos y Medición de Rendimiento

Se ejecutó un script de pruebas en Python sobre datasets sintéticos de géneros y canciones con entradas de $N = 1.000$, $N = 10.000$ y $N = 100.000$ elementos. Se midió el tiempo promedio de ejecución en milisegundos ($ms$) para ambas estrategias:

| $N$ Elementos | Búsqueda Secuencial (Lista Enlazada) | Búsqueda en Árbol Binario (ABB) |
| :--- | :--- | :--- |
| **1.000** | $0{,}80$ ms | $0{,}02$ ms |
| **10.000** | $7{,}90$ ms | $0{,}03$ ms |
| **100.000** | $78{,}00$ ms | $0{,}05$ ms |

---

## 4. Análisis de Complejidad Algorítmica

### Estrategia A: Búsqueda Secuencial

* **Peor Caso — $O(N)$:** Ocurre cuando el género buscado se encuentra al final de la lista o no existe dentro del catálogo registrado.
* **Mejor Caso — $\Omega(1)$:** Ocurre si el género buscado coincide con el primer nodo de la lista.
* **Caso Promedio — $\Theta(N)$:** En promedio se recorren $N/2$ elementos, manteniendo un crecimiento de tiempo lineal.

### Estrategia B: Árbol Binario de Búsqueda (ABB por Género)

* **Peor Caso — $O(N)$:** Ocurre únicamente si los nombres de los géneros se insertan de forma estrictamente ordenada y el árbol se degrada a una lista enlazada (árbol desbalanceado).
* **Mejor Caso — $\Omega(1)$:** Ocurre cuando el género buscado se halla directamente en la raíz del árbol.
* **Caso Promedio / Cota Ajustada — $\Theta(\log N)$:** En un árbol balanceado, cada comparación reduce exponencialmente el espacio de búsqueda, logrando recuperar las canciones de un género en tiempo logarítmico.

---

## 5. Justificación Técnica y Conclusión

Se seleccionó la **Estrategia B (Árbol Binario de Búsqueda indexado por Género)** por su rendimiento superior en catálogos extensos. Esta estructura permite localizar cualquier género en tiempo logarítmico y acceder a sus canciones asociadas de forma casi instantánea, eliminando la necesidad de recorrer todo el catálogo secuencialmente.

* **Escalabilidad:** Mientras que la Búsqueda Secuencial incrementa su tiempo de respuesta en un factor de $10\times$ por cada orden de magnitud que escala el catálogo (pasando de $0{,}80$ ms a $78{,}00$ ms), la Búsqueda en Árbol mantiene tiempos prácticamente constantes ($0{,}02$ ms a $0{,}05$ ms).
* **Experiencia de Usuario:** La complejidad $\Theta(\log N)$ del ABB asegura un rendimiento óptimo e imperceptible al filtrar por géneros o vibras musicales desde la CLI (`main.py`) o futuras integraciones.

En síntesis, el ABB resulta la estructura más adecuada para sostener el crecimiento del catálogo sin degradar la experiencia de búsqueda.