# Análisis Técnico — TP9: Optimización en Grafos Pesados (Dijkstra)

## 1. Definición de Costo en el Dominio Musical
En las versiones anteriores, el grafo de colaboraciones era **No Pesado**. Todas las conexiones valían lo mismo (1 salto). Sin embargo, en el mundo real, no todas las colaboraciones tienen el mismo impacto. 

Para esta versión, transformamos el grafo en un **Grafo Pesado**, definiendo el costo de una arista como la **"Distancia de Afinidad"**.
* **Fórmula:** `Costo = 100 - popularidad_de_la_cancion`
* **Justificación:** Una canción extremadamente popular (ej. *Don feat. Ca7riel* con popularidad 95) genera un costo muy bajo (5). Esto significa que la conexión entre Miranda! y Ca7riel es "fuerte" o "cercana". Por el contrario, una colaboración menos conocida (popularidad 60) genera un costo mayor (40), representando una conexión más "débil" o "lejana".

## 2. Justificación del Algoritmo: Dijkstra
Para encontrar el "camino de colaboración más fuerte" entre dos artistas, implementamos el **Algoritmo de Dijkstra** (`camino_mas_fuerte_dijkstra`).

**¿Por qué Dijkstra y no otro (ej. Bellman-Ford o Floyd-Warshall)?**
1. **Ausencia de pesos negativos:** La popularidad en nuestro catálogo va de 0 a 100. Por lo tanto, el costo (`100 - popularidad`) siempre será un valor positivo ($\ge 0$). Dijkstra es matemáticamente óptimo y seguro bajo esta condición.
2. **Grafo No Dirigido:** Las colaboraciones son mutuas. Dijkstra funciona perfectamente en grafos no dirigidos (tratando cada arista como bidireccional con el mismo peso positivo).
3. **Densidad del Grafo:** La red de colaboraciones musicales es un **grafo disperso** (pocos artistas colaboran con *todos* los demás). Dijkstra, implementado con una Cola de Prioridad (`heapq` en Python), tiene una complejidad de $O((V + E) \log V)$, lo cual es inmensamente más eficiente que Floyd-Warshall ($O(V^3)$) para grafos dispersos cuando solo necesitamos el camino entre un origen y un destino específicos.

## 3. Evaluación de Dependencias (Ordenamiento Topológico)
El requerimiento solicitaba evaluar la inclusión de un **Ordenamiento Topológico** si el dominio presentaba relaciones de dependencia.

**Conclusión de la evaluación:** *No es aplicable a este grafo.*
* **Justificación Matemática:** El ordenamiento topológico solo puede aplicarse a grafos **DAG** (Grafos Dirigidos Acíclicos). Nuestro grafo de colaboraciones es **No Dirigido** y altamente **Cíclico** (ej. Miranda! colabora con Lali, Lali colabora con FMK, FMK colabora con Miranda!). 
* **Justificación del Dominio:** No existen "prerrequisitos" en las colaboraciones. Un usuario no necesita escuchar a un artista A *antes* de poder escuchar a un artista B. Al no haber una flecha de dependencia estricta, el ordenamiento topológico carece de sentido semántico y matemático en esta estructura específica.
