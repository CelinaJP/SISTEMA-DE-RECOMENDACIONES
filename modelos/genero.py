class Genero:
    def __init__(self, id_genero: int, nombre: str, descripcion: str = ""):
        self._id = id_genero
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def id(self) -> int: return self._id

    @property
    def nombre(self) -> str: return self._nombre

    @property
    def descripcion(self) -> str: return self._descripcion

    @descripcion.setter
    def descripcion(self, texto: str):
        self._descripcion = texto

    def __str__(self) -> str:
        return self._nombre

    def __repr__(self) -> str:
        return f"Genero(id={self._id}, nombre='{self._nombre}')"
    