from typing import List, Optional

class Cancion:
    def __init__(
        self, id_cancion: int, titulo: str, artista_principal: str,
        colaboradores: Optional[List[str]] = None, anio: int = 0, era: str = "Clásica",
        duracion_segundos: int = 0, genero: str = "Pop", mood: str = "",
        popularidad: int = 0, clasica_version_id: Optional[int] = None,
        moderna_version_id: Optional[int] = None
    ):
        self._id = id_cancion
        self._titulo = titulo
        self._artista_principal = artista_principal
        self._colaboradores = colaboradores if colaboradores is not None else []
        self._anio = anio
        self._era = era
        self._duracion_segundos = duracion_segundos
        self._genero = genero
        self._mood = mood
        self._popularidad = popularidad
        self._clasica_version_id = clasica_version_id
        self._moderna_version_id = moderna_version_id

    # Getters (Solo lectura para atributos que no cambian)
    @property
    def id(self) -> int: return self._id
    
    @property
    def titulo(self) -> str: return self._titulo

    @property
    def duracion_segundos(self) -> int: return self._duracion_segundos

    @property
    def colaboradores(self) -> List[str]: return self._colaboradores

    # Getters y Setters para atributos mutables
    @property
    def popularidad(self) -> int:
        return self._popularidad

    @popularidad.setter
    def popularidad(self, valor: int):
        if 0 <= valor <= 100:
            self._popularidad = valor
        else:
            raise ValueError("La popularidad debe estar entre 0 y 100.")

    def __str__(self) -> str:
        return f"{self._titulo} - {self._artista_principal} ({self._anio})"

    def __repr__(self) -> str:
        return f"Cancion(id={self._id}, titulo='{self._titulo}', era='{self._era}')"
