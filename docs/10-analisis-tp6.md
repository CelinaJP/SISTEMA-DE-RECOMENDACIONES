# Análisis Técnico — TP6: Colas de Prioridad y Heaps (Versión 4)

## 1. El Problema: ¿Cómo elegir lo mejor sin perder tiempo?
Imagina que tienes una lista con todas las canciones de Miranda! y un usuario te pide: *"Mostrame las 10 canciones más populares"*. 

* **La forma lenta (Fuerza Bruta):** Agarrar la lista entera, ordenar **todas** las canciones de la más popular a la menos popular, y recién ahí quedarse con las primeras 10. Si el catálogo tuviera miles o millones de canciones, hacer esto cada vez que alguien entra a la app sería sumamente lento e ineficiente.
* **La solución inteligente (Cola de Prioridad / Heap):** En lugar de ordenar todo el catálogo, usamos una estructura especial en forma de árbol llamada **Heap**. Este árbol tiene una regla de oro: **el elemento más importante (el de mayor popularidad) siempre se ubica automáticamente en la cima (la raíz)**. De este modo, "el sistema elige primero" al mejor candidato de forma instantánea sin necesidad de ordenar el resto de la base de datos.

---

## 2. ¿Cómo funciona por debajo?
Se implementó un **Max-Heap binario manual** (`estructuras/heap.py`) utilizando una lista simple de Python para representar la estructura del árbol de manera eficiente:
- **Indexación matemática:** Para cualquier nodo en la posición `i`, su hijo izquierdo está en `2 * i + 1`, su hijo derecho en `2 * i + 2`, y su padre en `(i - 1) // 2`.
- **Operaciones clave:**
  - `insertar(elemento)`: Agrega el elemento al final de la lista y ejecuta la función de *flotar* (`_flotar` / *heapify-up*) para ubicarlo correctamente según su prioridad.
  - `extraer_maximo()`: Remueve la raíz (el número uno del ranking), sube el último elemento a la cima y ejecuta la función de *hundir* (`_hundir` / *heapify-down*) para reordenar el árbol en milisegundos.

---

## 3. La Función de Prioridad
Para que el Heap sepa qué canción va primero, creamos un módulo independiente (`algoritmos/prioridad.py`) que extrae de forma segura el atributo numérico (en este caso, la **popularidad**) de cada objeto `Cancion`. Esto desacopla la regla de negocio de la estructura de datos, permitiendo cambiar el criterio (por ejemplo, sumar rating o año) sin romper el código del Heap.

---

## 4. Análisis de Complejidad ($O$)

Comparando el enfoque tradicional de ordenamiento completo frente al uso del Heap para obtener un **Top-N**:

| Operación / Enfoque | Ordenar todo el Dataset (Timsort tradicional) | Usar Heap Binario (Nuestra solución) |
|---|---|---|
| **Construcción / Estructura** | $O(N \log N)$ | $O(N)$ (mediante inserciones o heapify) |
| **Extracción del Top-N** | $O(N \log N)$ (requiere ordenar todo) | **$O(N + K \log N)$** (donde $K$ es el tamaño del Top) |
| **Rendimiento práctico** | Lento ante catálogos extensos o peticiones recurrentes. | **Altamente eficiente**, ya que no procesa el orden estricto de elementos que quedan fuera del ranking. |

---

## 5. Integración en la Terminal
Esta estructura se conectó directamente a la **opción 1** del menú interactivo (`ui/terminal.py`), permitiendo que cada vez que el usuario solicite ver el *Top 10 de canciones más populares*, el sistema construya el Heap por detrás y devuelva el ranking optimizado en tiempo récord.