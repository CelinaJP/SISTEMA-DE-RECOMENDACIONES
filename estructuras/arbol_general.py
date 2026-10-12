from typing import List, Optional, Deque
from collections import deque
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modelos.cancion import Cancion
from estructuras.arbol_binario import _normalizar


class NodoGeneral:
    """Nodo para un Árbol General (N hijos).
    Se usa para modelar la jerarquía: Era -> Género -> Canciones.
    Los nodos hoja (géneros) contienen la lista de canciones.
    """

    def __init__(self, etiqueta: str):
        self._etiqueta = etiqueta
        self._hijos: List["NodoGeneral"] = []
        self._canciones: List[Cancion] = []

    @property
    def etiqueta(self) -> str:
        return self._etiqueta

    @property
    def hijos(self) -> List["NodoGeneral"]:
        return self._hijos

    @property
    def canciones(self) -> List[Cancion]:
        return self._canciones

    def agregar_hijo(self, nodo_hijo: "NodoGeneral") -> None:
        if nodo_hijo not in self._hijos:
            self._hijos.append(nodo_hijo)

    def agregar_cancion(self, cancion: Cancion) -> None:
        if cancion is None:
            return
        ids_existentes = {getattr(c, "id", None) for c in self._canciones}
        if getattr(cancion, "id", None) not in ids_existentes:
            self._canciones.append(cancion)

    def buscar_hijo(self, etiqueta: str) -> Optional["NodoGeneral"]:
        etiqueta_norm = _normalizar(etiqueta)
        for hijo in self._hijos:
            if _normalizar(hijo.etiqueta) == etiqueta_norm:
                return hijo
        return None

    def __str__(self) -> str:
        return f"{self._etiqueta} ({len(self._hijos)} hijos, {len(self._canciones)} canciones)"

    def __repr__(self) -> str:
        return f"NodoGeneral(etiqueta='{self._etiqueta}', hijos={len(self._hijos)})"


class ArbolGeneral:
    """Árbol General n-ario para administrar el catálogo de Miranda!
    por Era -> Género -> Canciones.
    """

    def __init__(self, nombre: str = "ArbolGeneral"):
        self._nombre = nombre
        self._raiz: Optional[NodoGeneral] = NodoGeneral("RaizCatálogo")

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def raiz(self) -> Optional[NodoGeneral]:
        return self._raiz

    def agregar_nodo(self, ruta: List[str], nombre: str) -> None:
        """Crea un nodo nuevo en la ruta indicada (ej. ['Moderna'], 'Electropop')."""
        actual = self._raiz
        for parte in ruta:
            hijo = actual.buscar_hijo(parte)
            if hijo is None:
                hijo = NodoGeneral(parte)
                actual.agregar_hijo(hijo)
            actual = hijo
        
        if actual.buscar_hijo(nombre) is None:
            actual.agregar_hijo(NodoGeneral(nombre))

    def agregar_cancion(self, era: str, genero: str, cancion: Cancion) -> None:
        """Inserta una canción en la hoja correspondiente, creando las eras y géneros si no existen."""
        nodo_era = self._raiz.buscar_hijo(era)
        if nodo_era is None:
            nodo_era = NodoGeneral(era)
            self._raiz.agregar_hijo(nodo_era)

        nodo_genero = nodo_era.buscar_hijo(genero)
        if nodo_genero is None:
            nodo_genero = NodoGeneral(genero)
            nodo_era.agregar_hijo(nodo_genero)

        nodo_genero.agregar_cancion(cancion)

    def cargar_desde_catalogo(self, catalogo) -> None:
        """Construye el árbol completo a partir de las canciones del catálogo."""
        canciones = catalogo.listar() if hasattr(catalogo, "listar") else []
        for cancion in canciones:
            era = getattr(cancion, "_era", "Clásica")
            genero = getattr(cancion, "_genero", "Pop")
            self.agregar_cancion(era, genero, cancion)

    def recorrido_dfs(self) -> List[str]:
        """Recorrido en profundidad (DFS) que devuelve la ruta completa de cada nodo."""
        rutas = []
        if self._raiz is None:
            return rutas

        def _dfs_recursivo(nodo: NodoGeneral, ruta_actual: str):
            for hijo in nodo.hijos:
                nueva_ruta = f"{ruta_actual} > {hijo.etiqueta}"
                rutas.append(nueva_ruta)
                _dfs_recursivo(hijo, nueva_ruta)
                
            for cancion in nodo.canciones:
                rutas.append(f"{ruta_actual} > {cancion.titulo}")

        _dfs_recursivo(self._raiz, self._raiz.etiqueta)
        return rutas

    def recorrido_bfs(self) -> List[str]:
        """Recorrido en amplitud (BFS) nivel por nivel."""
        visitados = []
        if self._raiz is None:
            return visitados

        cola: Deque[NodoGeneral] = deque([self._raiz])
        while cola:
            nodo = cola.popleft()
            visitados.append(nodo.etiqueta)
            for hijo in nodo.hijos:
                cola.append(hijo)
                
        return visitados

    def buscar_categoria(self, nombre: str) -> List[Cancion]:
        """Busca un nodo por nombre en cualquier nivel y devuelve todas las canciones que cuelgan de él."""
        if self._raiz is None or not nombre:
            return []

        nombre_norm = _normalizar(nombre)
        nodo_encontrado = self._buscar_nodo_recursivo(self._raiz, nombre_norm)
        
        if nodo_encontrado is None:
            return []

        canciones_resultado = []
        cola: Deque[NodoGeneral] = deque([nodo_encontrado])
        while cola:
            actual = cola.popleft()
            if actual.canciones:
                canciones_resultado.extend(actual.canciones)
            for hijo in actual.hijos:
                cola.append(hijo)
                
        return canciones_resultado

    def _buscar_nodo_recursivo(self, nodo: NodoGeneral, nombre_norm: str) -> Optional[NodoGeneral]:
        if _normalizar(nodo.etiqueta) == nombre_norm:
            return nodo
        for hijo in nodo.hijos:
            res = self._buscar_nodo_recursivo(hijo, nombre_norm)
            if res is not None:
                return res
        return None

    def imprimir(self) -> None:
        if self._raiz is None:
            print("Árbol vacío.")
            return
        print(f"--- {self._nombre} ---")
        for era in self._raiz.hijos:
            print(f"Era: {era.etiqueta}")
            for genero in era.hijos:
                print(f"  Género: {genero.etiqueta} ({len(genero.canciones)} canciones)")
                