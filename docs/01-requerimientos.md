# EL BOT DE TU CORAZÓN — Propuesta (TP0)

Sistema de recomendación y exploración del catálogo de Miranda! que permite buscar, comparar eras, conectar colaboradores cross-género y descubrir canciones a partir de las preferencias y el tiempo disponible del usuario.

## 1. Dominio elegido y justificación

**Dominio:** Música, Recomendaciones y Redes de Colaboración (*Electropop / Pop Latino*).

**Justificación:**
El catálogo de **Miranda!** es el escenario perfecto para un integrador de Estructuras de Datos. Con más de 20 años de trayectoria, la banda ha mutado desde el pop de culto de los años 2000 hasta el fenómeno colaborativo actual con *Hotel Miranda!*. Este dominio nos brinda un dataset heterogéneo y rico en metadatos, ideal para aplicar y justificar:
* **Grafos:** Para mapear la compleja red de colaboraciones cross-género (*Lali, CA7RIEL, María Becerra, FMK, Emilia*).
* **Diccionarios / Tablas Hash:** Para realizar búsquedas e interconexiones instantáneas $O(1)$ entre canciones originales y sus re-versiones modernas.
* **Árboles / Heaps:** Para el ordenamiento eficiente y la extracción de Tops según métricas de popularidad global.
* **Listas y Algoritmos de Búsqueda:** Para la generación de playlists ajustadas a duraciones acumuladas precisas.

Contamos con datos reales extraídos directamente de la API pública de Spotify y archivos estructurados JSON con métricas de popularidad, duraciones, años de lanzamiento y colaboradores.

## 2. Problema que resuelve

La brecha generacional y de formato entre el catálogo clásico de un artista extenso y sus versiones colaborativas modernas dificulta a los nuevos oyentes descubrir canciones afines sin depender de algoritmos aleatorios que ignoran su tiempo disponible y sus preferencias.

## 3. Usuario objetivo

**Sofía (22 años):** Consumidora nativa de la escena urbana actual (*Lali, Emilia, Duki*). Descubrió a Miranda! mediante las colaboraciones de *Hotel Miranda!* y busca explorar el catálogo de la banda de forma personalizada: quiere conectar canciones según sus artistas urbanos favoritos, armar selecciones exactas para trayectos cortos y diferenciar rápidamente los clásicos originales de los *reworks* modernos.

## 4. Funcionalidades iniciales

| ID | Requerimiento Funcional | Descripción Algorítmica |
|---|---|---|
| **RF01** | **Top 10 Dinámico de Popularidad** | El sistema debe mostrar y ordenar las canciones de mayor a menor según su métrica de reproducción o popularidad global. |
| **RF02** | **Playlist por Tiempo Límite** |  El usuario ingresa cuántos minutos tiene disponibles (ej. 15 minutos) y el sistema selecciona una combinación de canciones cuya duración acumulada no supere ese límite. |
| **RF03** | **Explorador por Colaborador** | El sistema debe permitir ingresar el nombre de un artista invitado (ej. "María Becerra") y recorrer la red para devolver todas las canciones asociadas a esa persona. |
| **RF04** | **Filtro por Era / Etapa** | El sistema debe permitir separar los temas entre la "Era Clásica" ($< 2010$) y la "Era Hotel Miranda! / Moderna" ($\ge 2020$). |
| **RF05** | **Similitud por Género / Mood:** | Selecciona una canción base y recomienda otras que compartan el mismo género principal o subgénero/vibra.
| **RF06** | **Comparador de Versiones (Clásica vs. Re-versión):**|Permite seleccionar una canción emblemática y despliega un frente a frente comparando las métricas (duración, popularidad, participantes) de su versión original vs. su rework moderno.
| **RF07** | **Recomendador de Puente Temporal:** |  ("Si escuchás la nueva, probá la clásica"): Si el usuario selecciona o escucha una versión moderna de Hotel Miranda!, el sistema detecta la relación de la obra y sugiere automáticamente reproducir la versión original clásica (o viceversa). |

## 5. Ejemplo de uso (input/output)

```text
============================================================
       EL BOT DE TU CORAZÓN — MIRANDA! EDITION
============================================================
 1. Top 10 Dinámico de Popularidad
 2. Generar Playlist por Tiempo Límite
 3. Explorar Conexiones por Colaborador (Grafo)
 4. Filtrar por Era (Clásica <2010 | Moderna >=2020)
 5. Similitud por Género / Mood
 6. Comparar Versiones
 7. Recomendador de Puente Temporal
 0. Salir
============================================================
Seleccione una opción (0-7): 7

--- COMPARADOR DE VERSIONES Y PUENTE TEMPORAL ---
Ingrese el nombre de la canción o versión actual: Perfecta feat. María Becerra

[ CANCIÓN DETECTADA: "Perfecta (feat. María Becerra & FMK)" - Era Moderna (2023) ]
------------------------------------------------------------
MÉTRICA        | ERA CLÁSICA (2007)    | HOTEL MIRANDA! (2023)
------------------------------------------------------------
Año            | 2007                  | 2023
Duración       | 3:45 min              | 3:09 min
Artistas       | Miranda!              | Miranda! feat. María Becerra, FMK
Popularidad    | 78/100                | 91/100
------------------------------------------------------------
🎵 ¿Te gustó este tema? Descubrí la versión original donde nació todo:

 📻 Título Original : Perfecta (con Juliana Gattas & Ale Sergi)
 📅 Año Lanzamiento : 2007 (Álbum: El Disco de tu Corazón)
 💡 Género Base     : Electropop / Pop Latino Clásico
------------------------------------------------------------
¿Deseas agregar la versión clásica a tu cola de reproducción? (S/N): S
¡Agregada con éxito a la cola!

## 6. Requerimientos

### Requerimientos Funcionales (RF)

Los requerimientos funcionales especifican las operaciones y comportamientos concretos que el sistema debe ejecutar ante las solicitudes del usuario o eventos internos. En términos operativos, establecen las capacidades y funciones específicas de la aplicación.

* **RF01 — Top 10 Dinámico de Popularidad:** El sistema debe permitir mostrar y ordenar el catálogo según la métrica de reproducción o popularidad global.
* **RF02 — Playlist por Tiempo Límite:** El sistema debe generar una selección o playlist de canciones ajustada a una duración máxima en minutos ingresada por el usuario, sin superar dicho tiempo.
* **RF03 — Explorador por Colaborador:** El sistema debe permitir consultar y recuperar todas las canciones en las que participa un artista invitado específico.
* **RF04 — Filtro por Era / Etapa:** El sistema debe permitir filtrar el catálogo de canciones discriminando por su época de lanzamiento (Era Clásica $< 2010$ y Era Moderna / Hotel Miranda! $\ge 2020$).
* **RF05 — Recomendación por Mood / Género:** El sistema debe sugerir o recomendar canciones similares a partir de una obra base seleccionada por el usuario, evaluando coincidencias de género y mood.
* **RF06 — Comparador de Versiones:** El sistema debe permitir comparar en paralelo las métricas (duración, popularidad y colaboradores) de la versión clásica original frente a su re-versión moderna de Hotel Miranda!.
* **RF07 — Puente Temporal:** El sistema debe permitir conectar y sugerir el paso directo entre la versión moderna de una canción y su versión clásica original.

### Requerimientos No Funcionales (RNF)

Los requerimientos no funcionales establecen los criterios de calidad, restricciones y propiedades de rendimiento del software. Definen el "cómo opera" el sistema en términos de eficiencia, mantenibilidad, plataforma y arquitectura.

* **RNF01 — Rendimiento:** Las operaciones de búsqueda, filtrado y comparación entre versiones deben responder con un tiempo de respuesta aceptable manejando datasets de más de 1.000 registros en memoria.
* **RNF02 — Persistencia y Carga Local:** El sistema debe poblar sus estructuras de datos a partir de archivos estructurados locales en formato JSON o CSV, sin requerir llamadas externas a APIs en tiempo de ejecución.
* **RNF03 — Modularidad y Arquitectura:** La aplicación debe estar estructurada en capas independientes (Modelos, Servicios e Interfaz de Usuario), garantizando bajo acoplamiento y encapsulamiento adecuado.
* **RNF04 — Interfaz de Usuario:** La interacción con el usuario debe llevarse a cabo mediante una interfaz de línea de comandos (CLI) intuitiva, formateada y clara en formato de texto.
* **RNF05 — Compatibilidad:** El código debe ser completamente ejecutable en un entorno Python 3.10+ sin depender de librerías externas complejas no contempladas en la materia.

## 7. Fuera de alcance

Con el objetivo de acotar el proyecto a las exigencias académicas de la cátedra, el sistema explícitamente **no** incluirá:

* **Autenticación y usuarios:** No se gestionarán cuentas de usuario, sesiones ni perfiles personalizados.
* **Reproducción de audio:** El sistema no reproducirá archivos de sonido real (`.mp3`, `.wav`), operando únicamente sobre los metadatos de las canciones.
* **Integración con APIs o servicios en la nube:** La aplicación funcionará de manera 100% local y offline, sin conectarse en tiempo real a plataformas como Spotify o Last.fm.
* **Interfaz gráfica de usuario (GUI):** No se desarrollará ninguna interfaz visual moderna (web, escritorio o móvil); la interacción será exclusivamente en texto por terminal.
* **Persistencia de modificaciones:** No se implementarán funciones para agregar, editar o eliminar canciones del archivo JSON desde la consola durante la ejecución del programa.
