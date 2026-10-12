# TP5 — Análisis Técnico: Árbol General y Jerarquía del Catálogo (Miranda!)

## 1. El Problema: Organización Jerárquica Multidimensional del Catálogo

A diferencia de las búsquedas puntuales por título o artista (resueltas mediante Árboles Binarios de Búsqueda y AVL en los TPs anteriores), el dominio musical de **Miranda!** presenta una complejidad relacional natural que no puede modelarse adecuadamente en una estructura lineal ni estrictamente binaria de una sola clave: **la necesidad de clasificar las obras de forma multinivel**.

Para un usuario que explora el catálogo de una banda con más de dos décadas de trayectoria y un reciente hito de re-versiones masivas (*Hotel Miranda!*), recorrer las canciones requiere una taxonomía clara:
1. **¿A qué etapa o período pertenece?** (Los discos originales de los 2000s frente al fenómeno colaborativo moderno).
2. **¿Bajo qué género, estilo o subgénero se agrupa?** (*Electropop*, *Synthpop Retro*, *Pop Moderno*, etc.).
3. **¿Cuáles son las canciones concretas que componen esa categoría?**

Un Árbol Binario tradicional (ABB o AVL) impone una restricción artificial de un máximo de dos hijos por nodo, lo que dificulta representar una clasificación donde un nodo padre (como una Era) se ramifica simultáneamente en múltiples categorías de géneros musicales, y cada género agrupa una lista variable de canciones en los nodos hoja.

---

## 2. La Solución: Árbol General (N-ario)

Para resolver este desafío, se implementó un **Árbol General (o N-ario)** (`estructuras/arbol_general.py`) compuesto por dos clases principales:

* **`NodoGeneral`**: Modela cada punto del árbol. Contiene:
  * Una etiqueta descriptiva (`_etiqueta`: str).
  * Una lista dinámica de nodos hijos (`_hijos`: List[NodoGeneral]) para soportar $N$ ramificaciones.
  * Una lista de elementos del dominio (`_canciones`: List[Cancion]) utilizada principalmente en los nodos hoja (los géneros musicales).
  * Propiedades de encapsulamiento (`@property`) y métodos de búsqueda y validación robustos (normalización de cadenas para evitar duplicados por mayúsculas o tildes).
* **`ArbolGeneral`**: Administra la estructura global del catálogo a partir de una raíz genérica (`RaizCatálogo`), permitiendo la inserción dinámica y la construcción automatizada del árbol recorriendo el catálogo completo.

---

## 3. Justificación de la Jerarquía de 3 Niveles

Se definió una jerarquía estrictamente estructurada en **3 niveles**:

$$\text{Raíz} \longrightarrow \text{Nivel 1: Era} \longrightarrow \text{Nivel 2: Género} \longrightarrow \text{Nivel 3: Canciones (Hojas)}$$

### ¿Por qué Era $\rightarrow$ Género y no Género $\rightarrow$ Era?

1. **Evolución Artística y Temporal:** La discografía de Miranda! se divide de manera orgánica y conceptual en dos grandes etapas: la **Era Clásica** (lanzamientos originales $<2010$) y la **Era Moderna / Hotel Miranda!** ($\ge2020$). Agrupar primero por **Era** permite separar de forma inmediata los álbumes originales y sus contextos de producción frente a las colaboraciones contemporáneas con artistas urbanos.
2. **Optimización de las Consultas del Sistema:** Funcionalidades clave del bot de recomendaciones —como el *Puente Temporal* (conectar una versión moderna con su clásico original) y el filtrado por etapas— se benefician enormemente de tener a las eras como nodos de primer nivel en la raíz. Si la raíz hubiera sido el género, los géneros se habrían fragmentado y duplicado artificialmente entre ambas épocas.

---

## 4. Algoritmos de Recorrido sobre el Catálogo Real

### A. Recorrido en Profundidad (DFS - Depth-First Search)
El recorrido DFS explora cada rama del árbol hasta el nivel más profundo antes de retroceder. En nuestro `ArbolGeneral`, se implementó de forma recursiva para retornar todas las rutas completas:
* **Ejemplos en el catálogo:**
  * `RaizCatálogo > Moderna > Pop Moderno > 743`
  * `RaizCatálogo > Clásica > Electropop > Imán`

### B. Recorrido en Amplitud (BFS - Breadth-First Search)
El recorrido BFS utiliza una cola (`deque`) para visitar los nodos nivel por nivel (raíz $\rightarrow$ eras $\rightarrow$ géneros).
* **Ejemplo en el catálogo:**
  `['RaizCatálogo', 'Moderna', 'Clásica', 'Pop Moderno', 'Electropop', 'Synthpop Retro']`

---

## 5. Análisis de Complejidad Temporal

| Operación | Complejidad Promedio | Complejidad Peor Caso | Observaciones |
|---|---|---|---|
| **Inserción de nodo (Era / Género)** | $O(H \cdot K)$ | $O(N)$ | $H$ es la altura del árbol (3 niveles fijos) y $K$ el número de hijos por nodo. Costo acotado y despreciable. |
| **Búsqueda de rama por etiqueta** | $O(K)$ | $O(N)$ | Recorrido lineal sobre los hijos directos evaluando cadenas normalizadas. |
| **Carga completa del catálogo** | $O(N)$ | $O(N)$ | Visita cada una de las $N$ canciones del catálogo exactamente una vez para ubicarla en su hoja correspondiente. |
| **Recorridos (DFS / BFS)** | $O(N + V)$ | $O(N + V)$ | Visita todos los nodos $V$ y todas las canciones $N$ almacenadas en las hojas. |

---

## 6. Conclusión

La incorporación del **Árbol General** en el TP5 complementa de forma perfecta las estructuras anteriores (ABB y AVL). Mientras que los árboles binarios optimizan la búsqueda puntual por clave, el Árbol General aporta una **visión taxonómica multidimensional**, permitiendo modelar la estructura artística de Miranda! de forma intuitiva, escalable y totalmente integrada con la interfaz de terminal (Opción 9).