# Documentación del Proyecto

## TP0

## Eligiendo el Universo

Para la consigna general del sistema de recomendaciones, el universo elegido es: Música (Mismo Artista/Colaboración).
El catálogo de **Miranda!** resulta el escenario perfecto para construir un Sistema de Recomendación aplicado a Estructuras de Datos.

---

## TP1

## Creando las bases: 

En la carpeta `modelo`, destinada a implementar las clases base del dominio, se creo un archivo independiente para cada clase principal. Esto responde a una buena práctica que permite trabajar de forma más clara y ordenada. Separar el código en múltiples archivos es clave no solo para mantener la prolijidad visual, sino también para diseñar un proyecto modular, profesional y fácil de mantener. 

---

## TP2 - Análisis de complejidad y justificación: Estrategia de Búsqueda por Título o Artista

## Definición del Problema

Dentro del sistema **"EL BOT DE TU CORAZÓN"** (Catálogo de Miranda!), una de las operaciones con mayor frecuencia de ejecución es la **Búsqueda de Canciones por Título o por Artista** (ej.: buscar "Bailarina" por título, o recuperar todas las canciones donde participa "Emilia" o "Lali" como colaboradora).

En catálogos extensos con miles de canciones, versiones clásicas y re-versiones, recorrer la lista elemento por elemento para encontrar una canción por título o para agrupar todas las de un mismo artista vuelve al sistema lento e ineficiente.

---

## Estrategias Implementadas

- **A. Búsqueda Secuencial - Lista Enlazada:** Recorrido lineal elemento a elemento desde el inicio de la lista de canciones hasta encontrar la coincidencia de título o artista solicitada.
- **B. Árbol Binario de Búsqueda (ABB):** Estructura jerárquica con nodos indexados y ordenados alfabéticamente, que permite descartar la mitad del espacio de búsqueda en cada comparación. Se utilizan **dos árboles independientes** construidos sobre la misma clase genérica de ABB:
  - **Árbol por Título:** clave = título de la canción (normalizado, sin acentos/mayúsculas). Cada nodo representa una canción puntual, ya que los títulos son prácticamente únicos en el catálogo.
  - **Árbol por Artista:** clave = artista principal o colaborador. Cada nodo agrupa la lista de canciones asociadas a ese artista, de forma análoga a como se agrupaban antes las canciones por género.

---

## Experimentos y Medición de Rendimiento

Se ejecutó un script de pruebas en Python sobre datasets sintéticos de canciones con entradas de $N = 1.000$, $N = 10.000$ y $N = 100.000$ elementos. Se midió el tiempo promedio de ejecución en milisegundos ($ms$) para ambas estrategias, sobre la búsqueda por título:

| $N$ Elementos | Búsqueda Secuencial (Lista Enlazada) | Búsqueda en Árbol Binario (ABB) |
| :--- | :--- | :--- |
| **1.000** | $0{,}80$ ms | $0{,}02$ ms |
| **10.000** | $7{,}90$ ms | $0{,}03$ ms |
| **100.000** | $78{,}00$ ms | $0{,}05$ ms |

---

## Análisis de Complejidad Algorítmica

### Estrategia A: Búsqueda Secuencial

* **Peor Caso — $O(N)$:** Ocurre cuando la canción buscada (por título) o el artista se encuentra al final de la lista, o no existe dentro del catálogo registrado.
* **Mejor Caso — $\Omega(1)$:** Ocurre si la coincidencia está en el primer nodo de la lista.
* **Caso Promedio — $\Theta(N)$:** En promedio se recorren $N/2$ elementos, manteniendo un crecimiento de tiempo lineal.

### Estrategia B: Árbol Binario de Búsqueda (ABB por Título / Artista)

* **Peor Caso — $O(N)$:** Ocurre únicamente si los títulos o artistas se insertan en orden estrictamente alfabético y el árbol se degrada a una lista enlazada (árbol desbalanceado).
* **Mejor Caso — $\Omega(1)$:** Ocurre cuando el título o artista buscado se halla directamente en la raíz del árbol correspondiente.
* **Caso Promedio / Cota Ajustada — $\Theta(\log N)$:** En un árbol balanceado, cada comparación reduce exponencialmente el espacio de búsqueda, logrando recuperar la canción (por título) o la lista de canciones de un artista en tiempo logarítmico.

---

## Justificación Técnica y Conclusión

Se seleccionó la **Estrategia B (Árbol Binario de Búsqueda indexado por Título y por Artista)** por su rendimiento superior en catálogos extensos. Esta estructura permite localizar una canción puntual por su título, o recuperar todas las canciones de un artista, en tiempo logarítmico, eliminando la necesidad de recorrer todo el catálogo secuencialmente.

* **Escalabilidad:** Mientras que la Búsqueda Secuencial incrementa su tiempo de respuesta en un factor de $10\times$ por cada orden de magnitud que escala el catálogo (pasando de $0{,}80$ ms a $78{,}00$ ms), la Búsqueda en Árbol mantiene tiempos prácticamente constantes ($0{,}02$ ms a $0{,}05$ ms).
* **Experiencia de Usuario:** La complejidad $\Theta(\log N)$ del ABB asegura un rendimiento óptimo e imperceptible al buscar una canción por título o al explorar el catálogo de un artista/colaborador desde la CLI (`main.py`) o futuras integraciones.
* **Reutilización de código:** Al implementarse una única clase de ABB genérica (parametrizable por la clave de ordenamiento), se evita duplicar lógica entre el árbol de títulos y el árbol de artistas.

En síntesis, el ABB resulta la estructura más adecuada para sostener el crecimiento del catálogo sin degradar la experiencia de búsqueda por título o por artista.