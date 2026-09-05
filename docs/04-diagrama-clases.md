# Diagrama de Clases Inicial

```mermaid
classDiagram
    class MenuInicio {
        +mostrar_menu_principal()
        +procesar_opcion(opcion: str)
    }

    class CatalogoDeCancion {
        -canciones: list
        +top_10() : list
        +playlist_x_tiempo(minutos: int) : list
        +explorar_colaborador(artista: str) : list
        +filtrar_por_era(era: str) : list
        +filtrar_por_mood(mood: str) : list
        +comparar_versiones(id_cancion: int)
        +puente_temporal(id_cancion: int) : Cancion
        +obtener_version_clasica(id_cancion: int) : Cancion
    }

    class Cancion {
        -id: int
        -titulo: str
        -artista_principal: str
        -colaboradores: list
        -anio: int
        -era: str
        -duracion: str
        -genero: str
        -mood: str
        -popularidad: int
        -clasica_version_id: int
        -moderna_version_id: int
        +get_titulo() : str
        +get_duracion() : str
    }

    MenuInicio --> CatalogoDeCancion : gestiona
    CatalogoDeCancion "1" o-- "*" Cancion : contiene