# Análisis Técnico — TP10: Arquitectura Consolidada, Límites de Alcance y Demo Day

## 1. Introducción y Contexto del Proyecto
Este documento formaliza las decisiones de arquitectura, diseño algorítmico, límites de alcance y circunstancias de gestión que definen la entrega final (**TP10 / Demo Day**) de **EL BOT DE TU CORAZÓN (Miranda! Edition)**.

El proyecto fue desarrollado para la materia **Estructuras de Datos**, con el objetivo de demostrar la aplicación rigurosa de estructuras en memoria (Árboles Binarios de Búsqueda, Árboles AVL, Árboles Generales N-arios, Heaps / Colas de Prioridad y Grafos Pesados con BFS, DFS y Dijkstra) sobre un catálogo musical de 120 canciones de Miranda!.

---

## 2. Circunstancias de Gestión y Límites de Alcance

### A. Baja de Integrante y Reajuste Operativo
Originalmente, el plan de trabajo contemplaba el desarrollo conjunto entre dos integrantes. No obstante, ante la deserción y abandono de la cursada por parte del segundo integrante del equipo, la capacidad operativa del proyecto se redujo de manera imprevista a la mitad. 

Frente a esta situación, se tomó la decisión estratégica de **priorizar el núcleo algorítmico y la corrección técnica de las estructuras de datos en memoria** (exigencia principal de la cátedra), dejando fuera del alcance ejecutable aquellas capas externas no requeridas para la aprobación de la materia:
1. **Conexión con Telegram Bot API:** La integración con bots externos requería implementar polling asíncrono, tokens de bot, webhook listeners y manejo de excepciones de red externa, lo que dispersaba el esfuerzo del trabajo individual.
2. **Opciones adicionales de la UI:** Las opciones secundarias de generación de playlist y módulos auxiliares quedaron formalmente documentadas y desacopladas en la consola local.

### B. Justificación Técnica de la Interfaz por Consola (CLI)
Aun prescindiendo de Telegram, la interfaz de línea de comandos (CLI) adoptada en `ui/terminal.py` presenta sólidas ventajas de ingeniería:
- **RNF02 (Persistencia y Autonomía Local):** El sistema opera en memoria a partir de `datos/miranda_canciones.json` sin depender de internet ni de servicios de terceros.
- **RNF04 (Interfaz Clara y Desacoplada):** Permite ejecutar todas las búsquedas, visualizaciones taxonómicas y algoritmos de grafos de forma determinista y reproducible.
- **Benchmarking Limpio:** Facilita medir tiempos precisos ($O, \Omega, \Theta$) en `benchmarks/` sin ruido ni latencias de red.

---

## 3. Resoluciones de Diseño Algorítmico

### A. Absorción de Versiones (Opciones 6, 7 y 8) en el Árbol AVL
Los requerimientos conceptuales preliminares planteaban submódulos separados para comparar versiones clásicas vs. modernas (RF06), sugerir puentes temporales (RF07) y obtener la versión original clásica.

**Solución aplicada:**
En lugar de implementar recorridos lineales redundantes, la lógica fue absorbida de forma nativa por el árbol auto-balanceado **`ArbolAVLPorTitulo`** (`estructuras/arbol_avl.py`):
- El nodo almacena canciones agrupadas bajo la misma clave normalizada de título.
- Al consultar por ejemplo `"Traición"` o `"Don"` en la **Opción 2**, el Árbol AVL recupera en $O(\log N)$ garantizado tanto la versión de la Era Clásica como la de *Hotel Miranda!*.
- Esto consolida la comparación y el puente temporal en una sola operación atómica y eficiente, eliminando la necesidad de menús redundantes.

### B. Clasificación de la Opción 4 (Playlist por Tiempo Límite)
La propuesta inicial de seleccionar una combinación de canciones cuya duración acumulada no exceda un límite $T$ ingresado por el usuario fue evaluada algorítmicamente:
- **Naturaleza teórica:** Corresponde formalmente al **Problema de la Mochila 0/1 (0/1 Knapsack Problem)** o **Subset Sum**, perteneciente al área de **Programación Dinámica / Optimización Combinatoria**.
- **Justificación de Exclusión:** La currícula de la cursada se centra en **Estructuras de Datos Jerárquicas y Redes (Árboles, Grafos y Heaps)**. Implementar una matriz de programación dinámica $O(N \cdot W)$ se identificó como fuera del scope curricular de este proyecto, por lo que la opción se mantuvo reservada para futuras extensiones.

---

## 4. Matriz de Estructuras y Complejidades del Sistema Final

| Módulo / Funcionalidad | Estructura de Datos | Algoritmo / Operación | Complejidad Teórica |
|---|---|---|---|
| **Búsqueda por Título (Opción 2)** | Árbol AVL (`ArbolAVLPorTitulo`) | Búsqueda binaria balanceada con rotaciones | $O(\log N)$ |
| **Búsqueda por Artista (Opción 2)** | Árbol Binario de Búsqueda (`ArbolPorArtista`) | Búsqueda por clave de artista o colaborador | $O(\log N)$ promedio |
| **Ranking Top 10 (Opción 1)** | Max-Heap binario manual (`MaxHeap`) | Flotar, hundir y extracción de máximos | $O(N + K \log N)$ |
| **Taxonomía por Categorías (Opción 9)** | Árbol General N-ario (`ArbolGeneral`) | Inserción multinivel y recorridos DFS / BFS | $O(V + N)$ |
| **Conexiones Indirectas (Opción 5.1)** | Grafo no dirigido (`GrafoColaboraciones`) | Búsqueda en Amplitud (BFS) por grados | $O(V + E)$ |
| **Cadenas Profundas (Opción 5.2)** | Grafo no dirigido (`GrafoColaboraciones`) | Búsqueda en Profundidad (DFS) iterativa | $O(V + E)$ |
| **Camino de Afinidad Óptima (Opción 5.3)**| Grafo pesado (`GrafoColaboraciones`) | Algoritmo de Dijkstra con Cola de Prioridad | $O((V + E) \log V)$ |

---

## 5. Conclusión y Balance para el Demo Day
Pese a la baja de la compañera de equipo, el proyecto consolidó una arquitectura robusta, modular y totalmente funcional. Se implementaron de forma artesanal y rigurosa todas las estructuras de datos no lineales evaluadas en la cursada, respaldadas por un suite de pruebas unitarias con cobertura del 100% de tests pasando exitosamente.