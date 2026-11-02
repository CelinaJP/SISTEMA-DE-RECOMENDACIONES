# Análisis Técnico — TP8 (Versión 6): Recorridos en Grafos (BFS vs DFS)

## 1. El Problema: Exploración Avanzada del Ecosistema Musical
En la versión anterior (TP7) definimos la estructura del grafo de colaboraciones de Miranda!. En esta **Versión 6 (TP8)**, el objetivo es utilizar algoritmos de recorrido para responder preguntas del mundo real sobre esta red.

Implementamos y comparamos dos estrategias clásicas de recorrido algorítmico: **BFS** (Búsqueda en Amplitud) y **DFS** (Búsqueda en Profundidad), cada una resolviendo un caso de uso distinto.

---

## 2. Los Algoritmos y sus Casos de Uso

### A. Búsqueda en Amplitud (BFS - Breadth-First Search)
* **¿Qué hace?** Explora la red "por niveles", visitando primero todos los vecinos directos (grado 1) antes de pasar a los vecinos de los vecinos (grado 2). Utiliza una **Cola** (`deque`).
* **Caso de uso real implementado:** *¿A cuántos grados de separación está un artista de otro?* En nuestra app, BFS permite descubrir los colaboradores más cercanos de un artista dado. Es perfecto para responder consultas de "camino más corto", ya que garantiza encontrar la conexión con menos intermediarios.
* **Cuándo conviene usarlo:** Cuando queremos encontrar el camino más corto, el grado de separación exacto, o cuando sabemos que el nodo destino está relativamente cerca en la red.

### B. Búsqueda en Profundidad (DFS - Depth-First Search)
* **¿Qué hace?** Se sumerge en una rama del grafo lo más profundo posible antes de retroceder (backtracking). Utiliza una **Pila** (`list.pop()`). Para evitar problemas de _RecursionError_ en ecosistemas grandes, nuestra implementación se hizo de manera iterativa.
* **Caso de uso real implementado:** *¿Cuál es la cadena de colaboraciones más larga a partir de un artista?* En la app, DFS explora todo el ecosistema musical (la componente conexa) y devuelve las cadenas más largas ("caminos profundos"). Permite descubrir conexiones extremas de impacto, uniendo sub-géneros lejanos a través de múltiples saltos.
* **Cuándo conviene usarlo:** Cuando queremos explorar un laberinto entero, mapear una componente conexa completa, o buscar rutas exhaustivas donde la longitud no es un problema sino el objetivo mismo de la consulta.

---

## 3. Diferencias Principales

| Característica | BFS (Amplitud) | DFS (Profundidad) |
|---|---|---|
| **Estructura subyacente** | Cola (FIFO) | Pila (LIFO) |
| **Garantía de Camino más corto** | **Sí** (en grafos no pesados). | **No**. |
| **Objetivo en el dominio** | Encontrar *conexiones cercanas* (contactos directos e indirectos). | Encontrar *cadenas extensas* (el alcance total del ecosistema). |

---

## 4. Análisis de Complejidad Computacional ($O$)

Ambos algoritmos, al estar implementados sobre una **Lista de Adyacencia** (mediante diccionarios en Python), comparten la misma complejidad teórica global:

* **Complejidad Temporal:** $O(V + E)$
  Donde $V$ es el número de vértices (artistas) y $E$ el número de aristas (colaboraciones). Cada vértice se extrae de la estructura una sola vez, y cada arista se evalúa para ver si lleva a un nodo no visitado.
* **Complejidad Espacial:** $O(V)$
  En el peor de los casos, la pila (DFS), la cola (BFS) y el set de `visitados` almacenan un peso proporcional al número total de vértices conectados en esa componente del grafo.

---

## 5. Integración en el Sistema (Versión 6)
La funcionalidad quedó completamente integrada en el menú interactivo (`ui/terminal.py`). Al seleccionar la **Opción 5 (Explorar Colaborador)**, el sistema bifurca la lógica dando control al usuario:
1. **BFS:** Resuelve los grados de separación.
2. **DFS:** Genera y muestra las rutas de colaboración más largas y profundas de la red.
