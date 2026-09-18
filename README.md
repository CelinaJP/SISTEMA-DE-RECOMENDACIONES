# SISTEMA DE RECOMENDACIONES
# EL BOT DE TU CORAZÓN — Miranda!  🤖❤️

Sistema de recomendación y exploración del catálogo musical de **Miranda!** que permite buscar, filtrar por eras, explorar redes de colaboración cross-género y generar selecciones personalizadas según las preferencias y el tiempo disponible del usuario

---

## Integrantes
Celina Jazmin Pereyra
Iara Stefania Santarella

---

## 📋 Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Dominio y Justificación](#1-dominio-elegido-y-justificación)
- [Problema que Resuelve](#2-problema-que-resuelve)
- [Usuario Objetivo](#3-usuario-objetivo)
- [Funcionalidades Requeridas](#4-funcionalidades-iniciales)
- [Búsqueda por Título o Artista (Árbol Binario de Búsqueda)](#búsqueda-por-título-o-artista-árbol-binario-de-búsqueda)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Ejemplo de Uso](#ejemplo-de-uso)

---

## Descripción del Proyecto
**EL BOT DE TU CORAZÓN** es una aplicación interactiva desarrollada para la materia Estructuras de Datos. Permite conectar el catálogo clásico de más de 20 años de la banda Miranda! con sus re-versiones colaborativas modernas (*Hotel Miranda!*), facilitando el descubrimiento musical a través de algoritmos de recomendación, filtrado y modelado en grafos/heaps.

---

## Dominio Elegido y Justificación
* **Dominio:** Música, Recomendaciones y Redes de Colaboración (*Electropop / Pop Latino*).
* **Justificación:** El catálogo de Miranda! brinda un conjunto heterogéneo y rico de datos ideales para aplicar y justificar el uso de estructuras de datos fundamentales:
  * **Grafos:** Mapeo de la red de colaboraciones cross-género (*Lali, CA7RIEL, María Becerra, FMK, Emilia*).
  * **Diccionarios / Tablas Hash:** Búsqueda e interconexión rápida $O(1)$ entre canciones originales y sus re-versiones.
  * **Árboles / Heaps:** Ordenamiento eficiente para la extracción dinámica de los Tops por popularidad, y búsqueda de canciones por título/artista en tiempo logarítmico mediante un Árbol Binario de Búsqueda (ver [sección dedicada](#búsqueda-por-título-o-artista-árbol-binario-de-búsqueda)).
  * **Listas y Algoritmos de Búsqueda:** Generación de playlists ajustadas a duraciones acumuladas exactas.

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
| **RF01** | **Top 10 Dinámico de Popularidad** | Muestra y ordena el catálogo de mayor a menor según su popularidad/reproducciones. |
| **RF02** | **Playlist por Tiempo Límite** | Genera una combinación de canciones ajustada a un límite de tiempo en minutos especificado por el usuario. |
| **RF03** | **Explorador por Colaborador** | Utiliza un Árbol Binario de Búsqueda indexado por artista (`ArbolPorArtista`) para recuperar en tiempo logarítmico todas las canciones asociadas a un artista invitado. |
| **RF04** | **Filtro por Era / Etapa** | Separa el catálogo entre la *Era Clásica* ($<2010$) y la *Era Moderna / Hotel Miranda!* ($\ge2020$). |
| **RF05** | **Similitud por Género / Mood** | Recomienda obras similares a partir de una canción base evaluando género o vibra. |
| **RF06** | **Comparador de Versiones** | Muestra un frente a frente comparando métricas (duración, popularidad, participantes) entre una versión clásica y su re-versión moderna. |
| **RF07** | **Puente Temporal** | Detecta una canción moderna seleccionada y sugiere automáticamente reproducir la versión clásica original (o viceversa). |
| **RF08** | **Búsqueda por Título o Artista** | Busca una canción puntual por título exacto, o todas las canciones de un artista/colaborador, usando dos Árboles Binarios de Búsqueda (`ArbolPorTitulo` y `ArbolPorArtista`). Ver detalle abajo. |

---

## Búsqueda por Título o Artista (Árbol Binario de Búsqueda)

A partir de TP3, la búsqueda de canciones por **título** o por **artista/colaborador**
se resuelve mediante dos Árboles Binarios de Búsqueda (ABB), en reemplazo de la
búsqueda secuencial de TP2. Esto baja la complejidad de $O(n)$ a $O(\log n)$ promedio.

### Cómo se usa desde la CLI

Al iniciar la aplicación, los árboles se construyen automáticamente a partir del
catálogo (`datos/miranda_canciones.json`):

```bash
python main.py
```

Luego, desde el menú principal:

- **Opción 2 — Buscar canción (por título o artista):** ingresá el título exacto de
  una canción (ej. `Bailarina`) o el nombre de un artista/colaborador (ej. `Lali`).
  La búsqueda usa el ABB internamente y devuelve resultados en tiempo logarítmico.
  > Nota: a diferencia de la opción 3 (Filtrar), esta búsqueda es por **coincidencia
  > exacta** (sin distinguir mayúsculas/acentos) — es una particularidad de cómo
  > funciona la búsqueda por clave en un árbol binario. Para búsqueda parcial/por
  > texto libre, usá la opción 3.

- **Opción 5 — Explorar Colaborador:** ingresá el nombre de un colaborador (ej.
  `Emilia`) y el sistema devuelve todas las canciones donde participó, usando el
  mismo árbol de artistas.

### Estructura interna

- `estructuras/arbol_binario.py`: contiene `NodoArbol` y `ArbolBinarioBusqueda`
  (clases genéricas), y las especializaciones `ArbolPorTitulo` y `ArbolPorArtista`.
- `ArbolPorTitulo`: indexa cada canción por su título. Los títulos repetidos
  (versión clásica y moderna de una misma canción) se agrupan en un mismo nodo.
- `ArbolPorArtista`: indexa cada canción tanto por su artista principal como por
  cada colaborador, de forma que buscar cualquiera de los dos encuentra la canción.

### Comparación de rendimiento y análisis de complejidad

El análisis completo de complejidad ($O$, $\Omega$, $\Theta$) y la comparación de
tiempos reales entre la búsqueda secuencial y el ABB están documentados en:
[`docs/02-documentacion.md`](docs/02-documentacion.md).

El script que genera esos datos de rendimiento se puede correr con:

```bash
python benchmarks/comparacion_busqueda.py
```

### Tests

```bash
python3 -m unittest discover -s test -v
```

---

## Estructura del Repositorio
El proyecto está organizado de manera modular respetando las pautas de arquitectura del curso:

```text
SISTEMA-DE-RECOMENDACIONES/
├── algoritmos/                 # Algoritmos de búsqueda, ordenamiento y grafos
├── benchmarks/                 # Scripts de comparación de rendimiento (secuencial vs ABB)
│   └── comparacion_busqueda.py
├── datos/
│   └── miranda_canciones.json  # Catálogo estructurado en JSON
├── docs/                       # Documentación y propuestas del TP
│   ├── 01-requerimientos.md
│   ├── 02-documentacion.md     # Incluye el análisis de complejidad (TP2) y su justificación
│   ├── 03-interfaz-terminal.md
│   ├── 04-diagrama-clases.md
│   └── 05-gestion-del-proyecto.md
├── estructuras/                # Implementación de estructuras de datos propias
│   └── arbol_binario.py        # ABB genérico + ArbolPorTitulo / ArbolPorArtista
├── modelos/                    # Entidades principales
│   ├── __init__.py
│   ├── cancion.py
│   ├── genero.py
│   └── usuario.py
├── servicios/                  # Lógica de negocio y recomendaciones
│   └── gestor_catalogo.py
├── test/                       # Pruebas unitarias
│   └── test_arbol_binario.py
├── ui/                         # Interfaz gráfica o de consola
│   └── terminal.py
├── .gitignore                  # Filtro de archivos no rastreados por Git
├── main.py                     # Punto de entrada de la aplicación
└── README.md                   # Documentación principal
```
---

## Estado
TP0 COMPLETADO
TP1 INCOMPLETO
TP2 COMPLETADO — Análisis de complejidad y justificación de estrategia de búsqueda
TP3 COMPLETADO — Árbol Binario de Búsqueda integrado (título/artista), tests y benchmark

---

## Instalación y ejecución

### Requisitos previos

- Python 3.8 o superior.
- Git.

### 1. Clonar el repositorio
git clone https://github.com/CelinaJP/SISTEMA-DE-RECOMENDACIONES.git

### 2. Navegar al proyecto
cd SISTEMA-DE-RECOMENDACIONES

### 3. Crear y activar entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

### 4. Instalar dependencias
pip install -r requirements.txt

### 5. Ejecutar la aplicación
python main.py

##