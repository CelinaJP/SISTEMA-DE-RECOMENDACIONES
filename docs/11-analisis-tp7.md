# Análisis Técnico — TP7: Grafos y Redes de Colaboración

## 1. El Problema: Mapear el Ecosistema Musical
El catálogo de Miranda! (especialmente en su etapa *Hotel Miranda!*) se caracteriza por una extensa red de colaboraciones con artistas de la escena urbana y pop (Lali, Ca7riel, FMK, María Becerra, etc.). 

Para un usuario, descubrir música no solo se trata de buscar un título, sino de **explorar conexiones**: *"Si me gusta Lali, ¿con quién más colaboró Miranda! que esté relacionado?"*. Un Árbol Binario de Búsqueda (como el usado en TP3) sirve para encontrar rápido a un artista, pero no sirve para entender **cómo se relacionan los artistas entre sí**. Para esto, necesitamos un **Grafo**.

---

## 2. Definición del Modelo de Grafo

Para modelar esta red en la clase `GrafoColaboraciones`, definimos los siguientes elementos:

* **Vértices (Nodos):** Representan a los **Artistas**. Tanto a la banda principal ("Miranda!") como a cualquiera de sus colaboradores ("Lali", "Emilia", "Dillom").
* **Aristas (Conexiones):** Representan una **Colaboración musical**. Si dos artistas participan en la misma canción, existe una arista que los une. La arista guarda como atributo el título de la canción compartida.

### Justificación del Tipo de Grafo
* **No Dirigido:** La colaboración es una relación mutua y bidireccional. Si Lali colaboró con Miranda!, Miranda! colaboró con Lali. No hay una jerarquía de dirección.
* **No Pesado:** Aunque guardamos el nombre de la canción en la arista, no le asignamos un "peso" numérico (como distancia o costo). Nuestro objetivo principal es evaluar la **conectividad** y los grados de separación, no calcular un "camino más corto" basado en costos.

---

## 3. Representación en Memoria: Lista de Adyacencia

Se decidió implementar el grafo utilizando una **Lista de Adyacencia** (mediante diccionarios anidados en Python: `{artista: {colaborador: [canciones]}}`).

**Justificación:**
La red de colaboraciones musicales es un **grafo disperso**. Miranda! es un nodo central (hub) conectado con casi todos los demás vértices, pero los colaboradores periféricos (ej. Cristian Castro y Dillom) rara vez están conectados entre sí. 
Si hubiéramos usado una **Matriz de Adyacencia**, tendríamos una cuadrícula gigante de $V \times V$ llena de ceros (indicando falta de conexión), desperdiciando una enorme cantidad de memoria. La lista de adyacencia solo almacena las conexiones que realmente existen, optimizando el espacio a $O(V + E)$.

---

## 4. Algoritmo de Búsqueda: BFS (Breadth-First Search)

Para responder a consultas complejas como *"¿A cuántos grados de separación está un artista de otro?"*, se implementó el método `buscar_conexiones_indirectas()` utilizando el algoritmo **BFS (Búsqueda en Amplitud)**.

* **¿Por qué BFS y no DFS?** BFS explora la red nivel por nivel (primero los contactos directos, luego los contactos de los contactos). Esto garantiza que encontremos el camino más corto en términos de "grados de separación" (ej. Lali ──► Miranda! ──► Ca7riel). Un DFS (Búsqueda en Profundidad) podría perderse en una rama larga y devolver un camino ineficiente.

---

## 5. Integración en el Sistema (Versión 5)
El grafo se instanció en `main.py` y se inyectó en la interfaz de terminal (`ui/terminal.py`). Al seleccionar la **Opción 5 (Explorar Colaborador)**, el sistema ahora:
1. Busca al artista en el grafo en $O(1)$ gracias al diccionario.
2. Imprime sus colaboraciones directas (Grado 1).
3. Ejecuta el BFS para mostrar las conexiones indirectas (Grado 2), revelando el ecosistema musical oculto detrás del catálogo.