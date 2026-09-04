# Gestión del Proyecto

## Tablero Kanban
* **Enlace al Tablero de Gestión:** [Tablero Kanban - GitHub Projects](https://github.com/users/CelinaJP/projects/1/views/1)

---

## Metodología de Trabajo

Para la organización y desarrollo del proyecto aplicamos **Scrum** (adaptado a la dinámica de la cursada):

* **Sprints por TP:** El trabajo se divide en Sprints iterativos e incrementales, haciendo coincidir cada Sprint con la entrega de cada Trabajo Práctico (ej. Sprint TP0, Sprint TP1)
* **Comunicación Continua y Aprendizaje:** Nos comunicamos activamente ante cada nueva implementación o explicación técnica. Realizamos reportes periódicos para evaluar el estado del proyecto, hacer devoluciones sobre qué corregir y enseñar los nuevos conceptos aplicados.
* **Flujo de Trabajo Kanban:** Visualizamos el flujo del Sprint en el tablero mediante las siguientes columnas:
  * **Todo (Por hacer):** Backlog de *Issues* planificados para el Sprint.
  * **In Progress (En progreso):** Tareas en desarrollo activo dentro de ramas secundarias (`feature/`).
  * **In Review (En revisión):** Código finalizado con Pull Request abierto, pendiente de revisión y prueba por parte del equipo.
  * **Done (Hecho):** Tareas cuyos Pull Requests fueron aprobados y fusionados (*merged*) con la rama `main`.

---

## Flujo de Trabajo en Git y GitHub (Gitflow Simplificado)

Seguimos las **Reglas de Oro** exigidas para garantizar la calidad del código:

1. **Main Siempre Funcional:** La rama `main` contiene únicamente código estable y ejecutable.
2. **Uso de Ramas e Issues:** Cada tarea surge de un *Issue* y se trabaja en una rama individual (`feature/nombre-de-tarea`).
3. **Pull Requests (PR) y Revisión Obligatoria:** Todo cambio requiere un PR y la revisión obligatoria de un compañero antes de fusionarse a `main`.
4. **Automatización:** Los Pull Requests incluyen palabras clave (ej. `Closes #X`) para cerrar los *Issues* y mover automáticamente las tarjetas a **Done**.
5. **Commits Claros:** Mensajes redactados con verbos en modo imperativo en español explicando el *qué* y el *porqué*.

---

## Estado de Sprints

### Sprint TP0: Lanzamiento
* [x] Definir universo, problema y usuario objetivo
* [x] Especificar las funcionalidades iniciales del sistema
* [x] Diseñar boceto de interfaz de terminal e interaction flow
* [x] Diseñar diagrama inicial de clases o componentes
* [x] Configuración del repositorio base y documentación inicial

### Retro TP0
* **Lo que salió bien:** Buena comunicación en el equipo para definir el dominio, acordar la metodología e integrar las automatizaciones entre GitHub Projects y las ramas del repositorio.
* **A mejorar:** Mantener la disciplina en el registro individual de commits, cumplir con la metodología y más comunicación.

---

### Sprint TP1: Objetos y Clases
* [ ] Implementar clases del dominio con encapsulamiento
* [ ] Diseñar e implementar interfaces entre módulos
* [ ] Implementar lectura y gestión de datos (JSON/CSV)
* [ ] Implementar operaciones principales (Buscar, Listar, Filtrar)
* [ ] Implementar la interfaz de consola interactiva
* [ ] Actualizar README, datos de prueba e instrucciones de ejecución

### Retro TP1
* **Lo que salió bien:** *Animarse a ser autodidacta y tener autogestión sobre las tareas y prácticas*
* **A mejorar:** *Dejar de querer tener el control (para Celi) y perder el miedo a romper cosas (Iari)*

```