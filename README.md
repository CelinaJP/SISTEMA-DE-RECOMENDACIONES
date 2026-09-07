# SISTEMA DE RECOMENDACIONES
# EL BOT DE TU CORAZÓN — Miranda!  🤖❤️

Sistema de recomendación y exploración del catálogo musical de **Miranda!** que permite buscar, filtrar por eras, explorar redes de colaboración cross-género y generar selecciones personalizadas según las preferencias y el tiempo disponible del usuario

---

## 📋 Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Dominio y Justificación](#1-dominio-elegido-y-justificación)
- [Problema que Resuelve](#2-problema-que-resuelve)
- [Usuario Objetivo](#3-usuario-objetivo)
- [Funcionalidades Requeridas](#4-funcionalidades-iniciales)
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
  * **Árboles / Heaps:** Ordenamiento eficiente para la extracción dinámica de los Tops por popularidad.
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
| **RF03** | **Explorador por Colaborador** | Recorre la red de colaboraciones y devuelve todas las canciones asociadas a un artista invitado. |
| **RF04** | **Filtro por Era / Etapa** | Separa el catálogo entre la *Era Clásica* ($<2010$) y la *Era Moderna / Hotel Miranda!* ($\ge2020$). |
| **RF05** | **Similitud por Género / Mood** | Recomienda obras similares a partir de una canción base evaluando género o vibra. |
| **RF06** | **Comparador de Versiones** | Muestra un frente a frente comparando métricas (duración, popularidad, participantes) entre una versión clásica y su re-versión moderna. |
| **RF07** | **Puente Temporal** | Detecta una canción moderna seleccionada y sugiere automáticamente reproducir la versión clásica original (o viceversa). |

---

## Estructura del Repositorio
El proyecto está organizado de manera modular respetando las pautas de arquitectura del curso:

```text
SISTEMA-DE-RECOMENDACIONES/
├── algoritmos/                 # Algoritmos de búsqueda, ordenamiento y grafos
├── datos/
│   └── miranda_canciones.json  # Catálogo estructurado en JSON
├── docs/                       # Documentación y propuestas del TP
│   ├── 01-requerimientos.md
│   ├── 03-interfaz-terminal.md
│   ├── 04-diagrama-clases.md
│   └── 05-gestion-del-proyecto.md
├── estructuras/                # Implementación de estructuras de datos propias
├── modelos/                    # Entidades principales
│   ├── __init__.py
│   ├── cancion.py
│   ├── genero.py
│   └── usuario.py
├── servicios/                  # Lógica de negocio y recomendaciones
├── test/                       # Pruebas unitarias
├── ui/                         # Interfaz gráfica o de consola
├── .gitignore                  # Filtro de archivos no rastreados por Git
├── main.py                     # Punto de entrada de la aplicación
└── README.md                   # Documentación principal
```

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