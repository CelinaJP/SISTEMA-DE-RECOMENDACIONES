from typing import List, Optional
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
        # 1. Asegurar era
        nodo_era = self._raiz.buscar_hijo(era)
        if nodo_era is None:
            nodo_era = NodoGeneral(era)
            self._raiz.agregar_hijo(nodo_era)

        # 2. Asegurar género bajo la era
        nodo_genero = nodo_era.buscar_hijo(genero)
        if nodo_genero is None:
            nodo_genero = NodoGeneral(genero)
            nodo_era.agregar_hijo(nodo_genero)

        # 3. Agregar canción a la hoja de género
        nodo_genero.agregar_cancion(cancion)

    def cargar_desde_catalogo(self, catalogo) -> None:
        """Construye el árbol completo a partir de las canciones del catálogo."""
        canciones = catalogo.listar() if hasattr(catalogo, "listar") else []
        for cancion in canciones:
            era = getattr(cancion, "_era", "Clásica")
            genero = getattr(cancion, "_genero", "Pop")
            self.agregar_cancion(era, genero, cancion)

    def imprimir(self) -> None:
        if self._raiz is None:
            print("Árbol vacío.")
            return
        print(f"--- {self._nombre} ---")
        for era in self._raiz.hijos:
            print(f"Era: {era.etiqueta}")
            for genero in era.hijos:
                print(f"  Género: {genero.etiqueta} ({len(genero.canciones)} canciones)")
                for c in genero.canciones[:3]:  # Muestra las primeras 3 de ejemplo
                    print(f"      🎵 {c.titulo} ({getattr(c, '_anio', 0)})")


if __name__ == "__main__":
    from servicios.gestor_catalogo import Catalogo
    
    # 1. Cargamos el catálogo de 120 canciones reales
    cat = Catalogo()
    cat.cargar_desde_json("datos/miranda_canciones.json")

    # 2. Construimos e imprimimos el Árbol General
    arbol = ArbolGeneral("CatalogoMirandaGeneral")
    arbol.cargar_desde_catalogo(cat)
    arbol.imprimir()

    # 3. Recorrido manual de 2 ramas para verificar la jerarquía (Criterio de Aceptación):
    print("\n" + "=" * 60)
    print("VERIFICACIÓN MANUAL DE RAMAS (Era -> Género -> Canciones)")
    print("=" * 60)
    
    for nodo_era in arbol.raiz.hijos[:2]:  # Recorremos las 2 eras
        print(f"\n📁 [Nivel 1] Era: {nodo_era.etiqueta}")
        for nodo_genero in nodo_era.hijos[:2]:  # Recorremos los primeros 2 géneros de cada era
            print(f"   📂 [Nivel 2] Género: {nodo_genero.etiqueta} ({len(nodo_genero.canciones)} canciones)")
            for cancion in nodo_genero.canciones[:2]:  # Mostramos 2 canciones del nivel hoja
                print(f"      🎵 [Nivel 3] {cancion.titulo} - Era: {getattr(cancion, '_era', '')} | Género: {getattr(cancion, '_genero', '')}")