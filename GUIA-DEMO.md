# Guía de Demostración 

Esta sección permite a los evaluadores reproducir de forma determinística todas las estructuras de datos y algoritmos exigidos en la presentación final:

### Paso 1: Iniciar la aplicación
```bash
python3 main.py
```

### Paso 2: Prioridad y Max-Heap (Opción 1)
- **Acción:** Ingresar `1`.
- **Qué se evalúa:** Extracción en $O(N + K \log N)$ de las 10 canciones más reproducidas a través del `MaxHeap` manual (`estructuras/heap.py`).
- **Salida esperada:** Un listado estrictamente ordenado de mayor a menor por popularidad, encabezado por temas emblemáticos de *Hotel Miranda!* como *"Don (feat. Ca7riel)"* (Popularidad 95) y *"Yo Te Diré (feat. Lali)"* (Popularidad 93). Presionar `ENTER` para retornar al menú.

### Paso 3: Búsqueda en Árbol AVL y Absorción de Versiones (Opción 2)
- **Acción:** Ingresar `2` y cuando solicite el título escribir `Don` (o `Traición`).
- **Qué se evalúa:** Búsqueda auto-balanceada en $O(\log N)$ con `ArbolAVLPorTitulo`.
- **Salida esperada:** La recuperación simultánea de **ambas versiones** agrupadas bajo el mismo nodo sin colisiones ni duplicados:
  1. Versión Clásica: `[12] Don - Miranda! | Era/Año: Clásica`
  2. Versión Moderna: `[102] Don - Miranda! (feat. Ca7riel) | Era/Año: Moderna`
  Presionar `ENTER` para retornar al menú.

### Paso 4: Red de Colaboraciones en Grafo (Opción 5)
- **Acción:** Ingresar `5` y escribir `Lali` como artista a consultar.
- **Sub-pruebas a ejecutar:**
  - **4.1. BFS (Opción `1`):** Evalúa conexiones directas (Grado 1: Miranda!) y conexiones indirectas (Grado 2: otros artistas que colaboraron con Miranda!, ej. Ca7riel, Emilia, FMK).
  - **4.2. DFS (Opción `2`):** Ejecuta exploración en profundidad devolviendo las cadenas de colaboración más largas del ecosistema musical.
  - **4.3. Dijkstra (Opción `3`):** Solicita un artista destino (ingresar `FMK`). Encuentra la ruta de mayor afinidad (menor costo `100 - popularidad`) conectando `Lali ──► Miranda! ──► FMK`.

### Paso 5: Navegación Taxonómica en Árbol General (Opción 9)
- **Acción:** Ingresar `9`.
- **Qué se evalúa:** Recorrido jerárquico multinivel del `ArbolGeneral`.
- **Interacción:**
  1. Seleccionar la Era `2` (*Moderna*).
  2. Seleccionar el Género `1` (*Pop Moderno*).
- **Salida esperada:** Lista de canciones clasificadas exclusivamente bajo esa rama del árbol (ej. `743`, `Lejos de Vos`, `Por Ese Hombre`).

### Paso 6: Verificación de Opciones Protegidas (Opciones 4, 6, 7 y 8)
- **Acción:** Probar ingresar `4`, `6`, `7` u `8`.
- **Salida esperada:** El sistema no crashea ni genera excepciones; emite el mensaje amigable correspondiente informando el estado de diseño o recordando que la comparación de versiones está integrada en la Opción 2, regresando fluidamente al menú al presionar `ENTER`.

### Paso 7: Ejecución de Tests Automatizados
Para verificar la integridad matemática y algorítmica de todas las estructuras (ABB, AVL, Árbol General, Grafo con Dijkstra y Heap):
```bash
python3 -m unittest discover -s test -v
```
**Resultado esperado:** 100% de los tests pasando (`OK`).

---