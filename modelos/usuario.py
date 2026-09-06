from typing import List

class Usuario:
    def __init__(self, id_usuario: int, nombre: str, tiempo_disponible_min: int = 15):
        self._id = id_usuario
        self._nombre = nombre
        self._tiempo_disponible_min = tiempo_disponible_min
        self._artistas_favoritos: List[str] = []

    @property
    def id(self) -> int: return self._id

    @property
    def nombre(self) -> str: return self._nombre

    @property
    def tiempo_disponible_min(self) -> int:
        return self._tiempo_disponible_min

    @tiempo_disponible_min.setter
    def tiempo_disponible_min(self, minutos: int):
        if minutos > 0:
            self._tiempo_disponible_min = minutos
        else:
            raise ValueError("El tiempo debe ser mayor a 0.")

    def agregar_artista_favorito(self, artista: str):
        if artista not in self._artistas_favoritos:
            self._artistas_favoritos.append(artista)

    def __str__(self) -> str:
        return f"Usuario: {self._nombre} | Tiempo: {self._tiempo_disponible_min} min"

    def __repr__(self) -> str:
        return f"Usuario(id={self._id}, nombre='{self._nombre}')"

