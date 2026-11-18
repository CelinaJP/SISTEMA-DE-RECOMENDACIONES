# SISTEMA DE RECOMENDACIONES
# EL BOT DE TU CORAZÓN — Miranda!  🤖❤️

Sistema de recomendación y exploración del catálogo musical de **Miranda!** que permite buscar, filtrar por eras, explorar redes de colaboración cross-género y generar selecciones personalizadas según las preferencias y el tiempo disponible del usuario.

---

## Integrantes
- Celina Jazmin Pereyra
- Iara Stefania Santarella *(Baja durante la cursada)*

---

## 📋 Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Dominio y Justificación](#1-dominio-elegido-y-justificación)
- [Problema que Resuelve](#2-problema-que-resuelve)
- [Usuario Objetivo](#3-usuario-objetivo)
- [Funcionalidades Requeridas](#4-funcionalidades-iniciales)
- [Búsqueda por Título o Artista (Árbol AVL y ABB)](#búsqueda-por-título-o-artista-árbol-avl-y-abb)
- [Balanceo Automático (Árbol AVL)](#balanceo-automático-árbol-avl)
- [Jerarquía del Catálogo (Árbol General)](#jerarquía-del-catálogo-árbol-general)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Estado](#estado)
- [Instalación y Ejecución](#instalación-y-ejecución)

---

## Descripción del Proyecto
**EL BOT DE TU CORAZÓN** es una aplicación interactiva desarrollada para la materia Estructuras de Datos. Permite conectar el catálogo clásico de más de 20 años de la banda Miranda! con sus re-versiones colaborativas modernas (*Hotel Miranda!*), facilitando el descubrimiento musical a través de algoritmos de recomendación, filtrado y modelado en grafos, árboles y heaps.

---

## Dominio Elegido y Justificación
* **Dominio:** Música, Recomendaciones y Redes de Colaboración (*Electropop / Pop Latino*).
* **Justificación:** El catálogo de Miranda! brinda un conjunto heterogéneo y rico de datos ideales para aplicar y justificar el uso de estructuras de datos fundamentales:
  * **Grafos:** Mapeo de la red de colaboraciones cross-género (*Lali, CA7RIEL, María Becerra, FMK, Emilia*).
  * **Diccionarios / Tablas Hash:** Búsqueda e interconexión rápida $O(1)$ entre canciones originales y sus re-versiones.
  * **Árboles / Heaps:** Ordenamiento eficiente para la extracción dinámica de los Tops por popularidad, y búsqueda de canciones por título/artista en tiempo logarítmico mediante un Árbol Binario de Búsqueda, con una variante auto-balanceada (AVL) que garantiza ese rendimiento incluso en el peor caso.
  * **Listas y Algoritmos de Búsqueda:** Generación de playlists y filtrado por metadatos.

---

## Problema que Resuelve
La brecha generacional y de formato entre el catálogo clásico de un artista extenso y sus re-versiones modernas dificulta a los nuevos oyentes descubrir canciones afines sin quedar a merced de algoritmos comerciales aleatorios que ignoran su disponibilidad de tiempo real y la afinidad entre artistas invitados.

---

## Usuario Objetivo
**Sofía (22 años):** Consumidora nativa de la escena urbana actual (*Lali, Emilia, Duki*). Descubrió a Miranda! mediante las colaboraciones de *Hotel Miranda!* y busca explorar el catálogo de la banda de forma personalizada: quiere conectar canciones según sus artistas urbanos favoritos, armar selecciones exactas para trayectos cortos y diferenciar rápidamente los clásicos originales de los *reworks* modernos.

---

## Funcionalidades Iniciales

| ID | Requerimiento Funcional | Descripción Algorítmica |
|---|---|---|
| **RF01** | **Top 10 Dinámico de Popularidad** | Muestra y ordena el catálogo de mayor a menor según su popularidad mediante un Max-Heap manual. |
| **RF02** | **Playlist por Tiempo Límite** | Planificada conceptualmente como problema de optimización combinatoria (Knapsack). |
| **RF03** | **Explorador por Colaborador** | Recorre la red de colaboraciones mediante algoritmos de grafos (BFS / DFS / Dijkstra). |
| **RF04** | **Filtro por Era / Etapa** | Separa el catálogo entre la *Era Clásica* ($<2010$) y la *Era Moderna / Hotel Miranda!* ($\ge2020$). |
| **RF05** | **Similitud por Género / Mood** | Recomienda obras similares a partir de una canción base evaluando género o vibra. |
| **RF06** | **Comparador de Versiones** | Integrado de forma nativa en la búsqueda AVL, agrupando versiones en el mismo nodo. |
| **RF07** | **Puente Temporal** | Detecta variantes clásicas y modernas agrupadas por clave en el Árbol AVL. |
| **RF08** | **Búsqueda por Título o Artista** | Búsqueda por título en Árbol AVL (`ArbolAVLPorTitulo`) y por artista en ABB (`ArbolPorArtista`). |
| **RF09** | **Balanceo Automático del Árbol (AVL)** | Garantiza que la búsqueda se mantenga en $O(\log n)$ incluso con datos preordenados. |

---

## Búsqueda por Título o Artista (Árbol AVL y ABB)

La búsqueda interactiva de canciones se resuelve mediante árboles:
- **Por Título:** utiliza `ArbolAVLPorTitulo` garantizando complejidad $O(\log n)$ siempre. Agrupa versiones clásica y moderna bajo el mismo nodo de título.
- **Por Artista:** utiliza `ArbolPorArtista` indexando tanto artista principal como colaboradores.

### Cómo se usa desde la CLI

```bash
python3 main.py
```

Luego, desde el menú principal:
- **Opción 2 — Buscar canción (por título o artista):** ingresá el título exacto de una canción (ej. `Traición`) o artista (ej. `Lali`). Devuelve de forma simultánea las versiones clásica y moderna agrupadas.
- **Opción 5 — Explorar Colaborador (Grafo):** permite recorrer conexiones directas, grados de separación (BFS), cadenas profundas (DFS) o el camino de afinidad más fuerte (Dijkstra).

---

## Balanceo Automático (Árbol AVL)

El Árbol Binario de Búsqueda del TP3 garantiza $O(\log n)$ solo si está balanceado. En el **peor caso** (títulos insertados ya ordenados), degenera en una lista enlazada $O(n)$ y puede desbordar la recursión de Python.

El **Árbol AVL** se auto-balancea tras cada inserción mediante rotaciones simples y dobles, garantizando $O(\log n)$ en el peor caso.

### Resultados reales (peor caso: títulos ya ordenados)

| $N$ | Altura BST común | Altura AVL | Altura ideal $\log_2(N)$ |
|---:|---:|---:|---:|
| 10 | 10 | 4 | 4 |
| 100 | 100 | 7 | 7 |
| 1.000 | **CRASH** (RecursionError) | 10 | 10 |
| 10.000 | **CRASH** (RecursionError) | 14 | 14 |

El análisis completo está disponible en [`docs/08-analisis-tp4.md`](docs/08-analisis-tp4.md).

---

## Jerarquía del Catálogo (Árbol General)

A partir del TP5, se incorporó un **Árbol General (`ArbolGeneral`)** n-ario para estructurar el catálogo de Miranda! en una jerarquía de 3 niveles:
- **Estructura:** `Era (Clásica / Moderna)` ➔ `Género (Electropop, Synthpop Retro, etc.)` ➔ `Canciones (Nodos hoja)`.
- **Justificación:** Agrupar primero por era facilita la separación conceptual de sus obras originales frente a sus re-versiones modernas y optimiza las consultas principales del bot.

Detalles en [`docs/09-analisis-tp5.md`](docs/09-analisis-tp5.md).

---

## Estructura del Repositorio
El proyecto está organizado de manera modular respetando las pautas de arquitectura del curso:

```text
SISTEMA-DE-RECOMENDACIONES/
├── algoritmos/                       # Scripts de demostración y utilidades algorítmicas
│   ├── generar_casos_desbalance.py   # Genera casos de desbalance BST vs. AVL (TP4)
│   ├── prioridad.py                  # Función de prioridad para Ranking (TP6)
│   ├── probar_bst.py                 # Demo del BST (TP3)
│   └── ranking.py                    # Extracción Top-N con MaxHeap (TP6)
├── benchmarks/                       # Scripts de comparación de rendimiento
│   ├── comparacion_busqueda.py       # Secuencial vs. binaria vs. ABB (TP2/TP3)
│   ├── resultados_comparacion.csv
│   ├── comparacion_bst_avl.py        # BST común vs. AVL (TP4)
│   └── resultados_bst_vs_avl.csv
├── datos/
│   └── miranda_canciones.json        # Catálogo estructurado en JSON (120 canciones)
├── docs/                             # Documentación técnica de entregas y análisis
│   ├── 01-requerimientos.md          # Especificación de requisitos del sistema
│   ├── 02-documentacion.md           # Análisis de complejidad y justificación (TP2)
│   ├── 03-interfaz-terminal.md       # Interaction flow de la CLI
│   ├── 04-diagrama-clases.md         # Diagrama UML de clases
│   ├── 05-gestion-del-proyecto.md    # Metodología y gestión Scrum/Kanban
│   ├── 07-analisis-tp3.md            # Análisis de BST y benchmark de búsqueda
│   ├── 08-analisis-tp4.md            # Análisis técnico: BST vs. AVL y rotaciones
│   ├── 09-analisis-tp5.md            # Análisis técnico: Árbol General N-ario
│   ├── 10-analisis-tp6.md            # Análisis técnico: Max-Heap y Ranking
│   ├── 11-analisis-tp7.md            # Análisis técnico: Grafo de Colaboraciones
│   ├── 12-analisis-tp8.md            # Análisis técnico: Recorridos BFS y DFS en grafos
│   ├── 13-analisis-tp9.md            # Análisis técnico: Grafos Pesados y Dijkstra
│   └── 14-analisis-tp10-demoday.md   # Arquitectura final, límites y Demo Day
├── estructuras/                      # Implementaciones de estructuras de datos
│   ├── arbol_avl.py                  # Árbol AVL genérico y por título (TP4)
│   ├── arbol_binario.py              # ABB genérico, por título y por artista (TP3)
│   ├── arbol_general.py              # Árbol General n-ario y NodoGeneral (TP5)
│   ├── grafo.py                      # Grafo pesado, BFS, DFS y Dijkstra (TP7/TP8/TP9)
│   └── heap.py                       # Implementación manual de Max-Heap (TP6)
├── modelos/                          # Entidades del dominio
│   ├── __init__.py
│   ├── cancion.py
│   ├── genero.py
│   └── usuario.py
├── servicios/                        # Lógica de negocio y catálogo
│   └── gestor_catalogo.py
├── test/                             # Pruebas unitarias
│   ├── test_arbol_avl.py             # Tests unitarios AVL (TP4)
│   ├── test_arbol_binario.py         # Tests unitarios ABB (TP3)
│   ├── test_arbol_general.py         # Tests unitarios Árbol General (TP5)
│   ├── test_grafo.py                 # Tests unitarios Grafo (TP7/TP8/TP9)
│   └── test_heap.py                  # Tests unitarios MaxHeap (TP6)
├── ui/                               # Interfaz de usuario por consola
│   └── terminal.py
├── .gitignore                        # Archivos ignorados por Git
├── main.py                           # Punto de entrada de la aplicación
└── README.md                         # Documentación principal
```

---

## Estado
- **TP0 COMPLETADO** — Propuesta de dominio, requerimientos y diseño inicial.
- **TP1 COMPLETADO** — Modelado del dominio con POO, encapsulamiento y lectura JSON.
- **TP2 COMPLETADO** — Análisis de complejidad y justificación de estrategias de búsqueda.
- **TP3 COMPLETADO** — Árbol Binario de Búsqueda (título/artista), tests y benchmark.
- **TP4 COMPLETADO** — Árbol AVL con rotaciones, comparación BST vs. AVL y balanceo.
- **TP5 COMPLETADO** — Jerarquía taxonómica con Árbol General N-ario (Era -> Género -> Canciones).
- **TP6 COMPLETADO** — Colas de prioridad y Max-Heap manual para Ranking Top-N.
- **TP7 COMPLETADO** — Grafo de colaboraciones no dirigido y lista de adyacencia.
- **TP8 COMPLETADO** — Recorridos BFS (grados de separación) y DFS (cadenas profundas).
- **TP9 COMPLETADO** — Optimización de grafos pesados con Algoritmo de Dijkstra.
- **TP10 COMPLETADO** — Integración en CLI con Árbol AVL, formalización de límites y Demo Day.

---

## Instalación y ejecución

### Requisitos previos
- Python 3.8 o superior.
- Git.

### 1. Clonar el repositorio
```bash
git clone https://github.com/CelinaJP/SISTEMA-DE-RECOMENDACIONES.git
```

### 2. Navegar al proyecto
```bash
cd SISTEMA-DE-RECOMENDACIONES
```

### 3. Ejecutar la aplicación
```bash
python3 main.py
```

### 4. Ejecutar la suite de tests
```bash
python3 -m unittest discover -s test -v
```
```