
from typing import List, Optional
from modelos.cancion import Cancion


def _normalizar(texto: str) -> str:
    if not texto:
        return ""
    texto_normalizado = str(texto).strip().lower()
    reemplazos = [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")]
    for original, reemplazo in reemplazos:
        texto_normalizado = texto_normalizado.replace(original, reemplazo)
    return texto_normalizado


def obtener_titulo_cancion(cancion: Cancion) -> str:
    if hasattr(cancion, "titulo"):
        return getattr(cancion, "titulo")
    if hasattr(cancion, "_titulo"):
        return getattr(cancion, "_titulo")
    return "Sin título"


def obtener_artista_principal_cancion(cancion: Cancion) -> str:
    if hasattr(cancion, "artista_principal"):
        return getattr(cancion, "artista_principal")
    if hasattr(cancion, "_artista_principal"):
        return getattr(cancion, "_artista_principal")
    return "Artista desconocido"


def obtener_colaboradores_cancion(cancion: Cancion) -> List[str]:
    colaboradores = getattr(cancion, "colaboradores", None)
    if colaboradores is None:
        colaboradores = getattr(cancion, "_colaboradores", [])
    return list(colaboradores) if colaboradores else []


class NodoArbol:

    def __init__(self, clave: str):
        self._clave = clave
        self._elementos: List[Cancion] = []
        self._izquierda: Optional["NodoArbol"] = None
        self._derecha: Optional["NodoArbol"] = None

    @property
    def clave(self) -> str:
        return self._clave

    @property
    def elementos(self) -> List[Cancion]:
        return self._elementos

    @property
    def izquierda(self) -> Optional["NodoArbol"]:
        return self._izquierda

    @izquierda.setter
    def izquierda(self, nodo: Optional["NodoArbol"]):
        self._izquierda = nodo

    @property
    def derecha(self) -> Optional["NodoArbol"]:
        return self._derecha

    @derecha.setter
    def derecha(self, nodo: Optional["NodoArbol"]):
        self._derecha = nodo

    def agregar_elemento(self, cancion: Cancion) -> None:
        if cancion is None:
            return
        ids_existentes = {getattr(c, "id", None) for c in self._elementos}
        if getattr(cancion, "id", None) not in ids_existentes:
            self._elementos.append(cancion)

    def __str__(self) -> str:
        return f"{self._clave} ({len(self._elementos)} canción/es)"

    def __repr__(self) -> str:
        return f"NodoArbol(clave='{self._clave}', elementos={len(self._elementos)})"


class ArbolBinarioBusqueda:

    def __init__(self, nombre: str = "ABB"):
        self._nombre = nombre
        self._raiz: Optional[NodoArbol] = None
        self._cantidad_claves: int = 0

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def raiz(self) -> Optional[NodoArbol]:
        return self._raiz

    @property
    def cantidad_claves(self) -> int:
        return self._cantidad_claves

    def esta_vacio(self) -> bool:
        return self._raiz is None

    def insertar(self, clave: str, cancion: Optional[Cancion] = None) -> None:
     
        if not clave:
            raise ValueError("La clave no puede estar vacía.")

        self._raiz = self._insertar_recursivo(self._raiz, clave, cancion)

    def _insertar_recursivo(
        self,
        nodo: Optional[NodoArbol],
        clave: str,
        cancion: Optional[Cancion],
    ) -> NodoArbol:
        if nodo is None:
            nuevo_nodo = NodoArbol(clave)
            nuevo_nodo.agregar_elemento(cancion)
            self._cantidad_claves += 1
            return nuevo_nodo

        clave_normalizada = _normalizar(clave)
        clave_nodo_normalizada = _normalizar(nodo.clave)

        if clave_normalizada == clave_nodo_normalizada:
            nodo.agregar_elemento(cancion)
        elif clave_normalizada < clave_nodo_normalizada:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, clave, cancion)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, clave, cancion)

        return nodo

    def __len__(self) -> int:
        return self._cantidad_claves

    def __str__(self) -> str:
        return f"{self._nombre}({self._cantidad_claves} claves)"


class ArbolPorTitulo(ArbolBinarioBusqueda):
    
    def __init__(self):
        super().__init__(nombre="ArbolPorTitulo")

    def insertar_cancion(self, cancion: Cancion) -> None:
        titulo = obtener_titulo_cancion(cancion)
        self.insertar(titulo, cancion)

    def cargar_desde_catalogo(self, catalogo) -> None:
        canciones = catalogo.listar() if hasattr(catalogo, "listar") else []
        for cancion in canciones:
            self.insertar_cancion(cancion)

class ArbolPorArtista(ArbolBinarioBusqueda):

    def __init__(self):
        super().__init__(nombre="ArbolPorArtista")

    def insertar_cancion(self, cancion: Cancion) -> None:
        artista_principal = obtener_artista_principal_cancion(cancion)
        self.insertar(artista_principal, cancion)

        for colaborador in obtener_colaboradores_cancion(cancion):
            self.insertar(colaborador, cancion)

    def cargar_desde_catalogo(self, catalogo) -> None:
        canciones = catalogo.listar() if hasattr(catalogo, "listar") else []
        for cancion in canciones:
            self.insertar_cancion(cancion)


if __name__ == "__main__":
    arbol_titulos = ArbolPorTitulo()
    arbol_artistas = ArbolPorArtista()

    ejemplos = [
        Cancion(1, "Bailarina", "Miranda!"),
        Cancion(21, "Traición", "Miranda!"),
        Cancion(103, "Traición", "Miranda!", colaboradores=["Emmanuel Horvilleur", "Juan Ingaramo"]),
        Cancion(104, "Uno los Dos", "Miranda!", colaboradores=["Emilia"]),
        Cancion(112, "MEJOR QUE VOS", "Miranda!", colaboradores=["Lali"]),
    ]

    for c in ejemplos:
        arbol_titulos.insertar_cancion(c)
        arbol_artistas.insertar_cancion(c)

    print(arbol_titulos, "| Raíz:", arbol_titulos.raiz)
    print(arbol_artistas, "| Raíz:", arbol_artistas.raiz)
    