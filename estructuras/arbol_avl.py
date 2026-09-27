"""
Árbol AVL: un Árbol Binario de Búsqueda que se
auto-balancea tras cada inserción, garantizando altura O(log N) siempre
— a diferencia del ABB común del TP3, que en el peor caso (datos ya
ordenados) degenera en una lista enlazada con altura O(N).

Mantiene la MISMA interfaz pública que `ArbolBinarioBusqueda` (TP3):
insertar, buscar, existe, inorder, preorder, postorder, imprimir — para
poder comparar ambos árboles con el mismo código de prueba/benchmark.


"""

from typing import List, Optional
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modelos.cancion import Cancion
from estructuras.arbol_binario import _normalizar, obtener_titulo_cancion


class NodoAVL:
    """Nodo del árbol AVL. Igual que `NodoArbol` del TP3 (clave + lista de
    elementos que comparten esa clave), pero además guarda su propia
    altura, necesaria para calcular el factor de balance en cada
    inserción.
    """

    def __init__(self, clave: str):
        self._clave = clave
        self._elementos: List[Cancion] = []
        self._izquierda: Optional["NodoAVL"] = None
        self._derecha: Optional["NodoAVL"] = None
        self._altura: int = 1  # un nodo recién creado es una hoja: altura 1

    @property
    def clave(self) -> str:
        return self._clave

    @property
    def elementos(self) -> List[Cancion]:
        return self._elementos

    @property
    def izquierda(self) -> Optional["NodoAVL"]:
        return self._izquierda

    @izquierda.setter
    def izquierda(self, nodo: Optional["NodoAVL"]):
        self._izquierda = nodo

    @property
    def derecha(self) -> Optional["NodoAVL"]:
        return self._derecha

    @derecha.setter
    def derecha(self, nodo: Optional["NodoAVL"]):
        self._derecha = nodo

    @property
    def altura(self) -> int:
        return self._altura

    @altura.setter
    def altura(self, valor: int):
        self._altura = valor

    def agregar_elemento(self, cancion: Cancion) -> None:
        if cancion is None:
            return
        ids_existentes = {getattr(c, "id", None) for c in self._elementos}
        if getattr(cancion, "id", None) not in ids_existentes:
            self._elementos.append(cancion)

    def __str__(self) -> str:
        return f"{self._clave} ({len(self._elementos)} canción/es, altura={self._altura})"

    def __repr__(self) -> str:
        return f"NodoAVL(clave='{self._clave}', altura={self._altura})"


# --- Funciones auxiliares de balance (fuera de la clase, porque operan
# sobre nodos que pueden ser None, y en Python es más simple así que
# repetir chequeos de None en cada método). ---

def _altura_de(nodo: Optional[NodoAVL]) -> int:
    """Altura de un nodo, tratando None (subárbol vacío) como altura 0."""
    return nodo.altura if nodo is not None else 0


def _factor_balance(nodo: Optional[NodoAVL]) -> int:
    """Factor de balance = altura(izquierda) - altura(derecha).

    En un AVL válido, este valor debe estar siempre entre -1 y 1 para
    TODO nodo. Si se sale de ese rango, hace falta rotar.
    """
    if nodo is None:
        return 0
    return _altura_de(nodo.izquierda) - _altura_de(nodo.derecha)


def _actualizar_altura(nodo: NodoAVL) -> None:
    nodo.altura = 1 + max(_altura_de(nodo.izquierda), _altura_de(nodo.derecha))


# --- Las 4 rotaciones ---

def _rotacion_simple_derecha(nodo: NodoAVL) -> NodoAVL:
    """Rotación simple a la derecha. Se usa en el caso Izquierda-Izquierda:
    el subárbol izquierdo del izquierdo es el que está "pesado".

          nodo                  pivote
         /                     /      \\
     pivote        -->      hijo_izq   nodo
     /    \\                            /
   hijo_izq  T                        T
    """
    pivote = nodo.izquierda
    nodo.izquierda = pivote.derecha
    pivote.derecha = nodo

    _actualizar_altura(nodo)
    _actualizar_altura(pivote)
    return pivote


def _rotacion_simple_izquierda(nodo: NodoAVL) -> NodoAVL:
    """Rotación simple a la izquierda. Se usa en el caso Derecha-Derecha:
    el subárbol derecho del derecho es el que está "pesado".

     nodo                        pivote
        \\                       /      \\
       pivote      -->        nodo   hijo_der
       /    \\                    \\
      T   hijo_der                 T
    """
    pivote = nodo.derecha
    nodo.derecha = pivote.izquierda
    pivote.izquierda = nodo

    _actualizar_altura(nodo)
    _actualizar_altura(pivote)
    return pivote


def _rotacion_doble_izquierda_derecha(nodo: NodoAVL) -> NodoAVL:
    """Rotación doble Izquierda-Derecha. Caso: el hijo izquierdo está
    pesado hacia la DERECHA. Primero se rota el hijo izquierdo a la
    izquierda (lo convierte en caso Izquierda-Izquierda), y después se
    rota el nodo original a la derecha.
    """
    nodo.izquierda = _rotacion_simple_izquierda(nodo.izquierda)
    return _rotacion_simple_derecha(nodo)


def _rotacion_doble_derecha_izquierda(nodo: NodoAVL) -> NodoAVL:
    """Rotación doble Derecha-Izquierda. Caso: el hijo derecho está
    pesado hacia la IZQUIERDA. Primero se rota el hijo derecho a la
    derecha (lo convierte en caso Derecha-Derecha), y después se rota el
    nodo original a la izquierda.
    """
    nodo.derecha = _rotacion_simple_derecha(nodo.derecha)
    return _rotacion_simple_izquierda(nodo)


class ArbolAVL:
    """Árbol AVL genérico, con la misma interfaz pública que
    `ArbolBinarioBusqueda` del TP3, para poder compararlos con el mismo
    código de pruebas.
    """

    def __init__(self, nombre: str = "AVL"):
        self._nombre = nombre
        self._raiz: Optional[NodoAVL] = None
        self._cantidad_claves: int = 0
        # Contador de rotaciones, útil para demostrar en las pruebas que
        # cada uno de los 4 casos clásicos se dispara correctamente.
        self._rotaciones = {
            "simple_izquierda": 0,
            "simple_derecha": 0,
            "doble_izquierda_derecha": 0,
            "doble_derecha_izquierda": 0,
        }

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def raiz(self) -> Optional[NodoAVL]:
        return self._raiz

    @property
    def cantidad_claves(self) -> int:
        return self._cantidad_claves

    @property
    def rotaciones(self) -> dict:
        """Cantidad de veces que se disparó cada tipo de rotación desde
        que se creó el árbol."""
        return dict(self._rotaciones)

    def esta_vacio(self) -> bool:
        return self._raiz is None

    def altura(self) -> int:
        """Altura total del árbol (0 si está vacío)."""
        return _altura_de(self._raiz)

    def factor_balance_raiz(self) -> int:
        return _factor_balance(self._raiz)

    # --- Inserción con balanceo automático ---

    def insertar(self, clave: str, cancion: Optional[Cancion] = None) -> None:
        if not clave:
            raise ValueError("La clave no puede estar vacía.")
        self._raiz = self._insertar_recursivo(self._raiz, clave, cancion)

    def _insertar_recursivo(
        self,
        nodo: Optional[NodoAVL],
        clave: str,
        cancion: Optional[Cancion],
    ) -> NodoAVL:
        # 1) Inserción normal de ABB
        if nodo is None:
            nuevo_nodo = NodoAVL(clave)
            nuevo_nodo.agregar_elemento(cancion)
            self._cantidad_claves += 1
            return nuevo_nodo

        clave_normalizada = _normalizar(clave)
        clave_nodo_normalizada = _normalizar(nodo.clave)

        if clave_normalizada == clave_nodo_normalizada:
            # Clave repetida: se agrupa en el mismo nodo, igual que en el
            # ABB del TP3. No cambia la altura, no hace falta rebalancear.
            nodo.agregar_elemento(cancion)
            return nodo
        elif clave_normalizada < clave_nodo_normalizada:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, clave, cancion)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, clave, cancion)

        # 2) Actualizar altura de este nodo (cambió porque insertamos abajo)
        _actualizar_altura(nodo)

        # 3) Calcular factor de balance y corregir si hace falta
        balance = _factor_balance(nodo)

        # Caso Izquierda-Izquierda: pesado a la izquierda, y el hijo
        # izquierdo también está pesado (o neutro) a la izquierda.
        if balance > 1 and _factor_balance(nodo.izquierda) >= 0:
            self._rotaciones["simple_derecha"] += 1
            return _rotacion_simple_derecha(nodo)

        # Caso Izquierda-Derecha: pesado a la izquierda, pero el hijo
        # izquierdo está pesado hacia la derecha (forma de "zigzag").
        if balance > 1 and _factor_balance(nodo.izquierda) < 0:
            self._rotaciones["doble_izquierda_derecha"] += 1
            return _rotacion_doble_izquierda_derecha(nodo)

        # Caso Derecha-Derecha: pesado a la derecha, y el hijo derecho
        # también está pesado (o neutro) a la derecha.
        if balance < -1 and _factor_balance(nodo.derecha) <= 0:
            self._rotaciones["simple_izquierda"] += 1
            return _rotacion_simple_izquierda(nodo)

        # Caso Derecha-Izquierda: pesado a la derecha, pero el hijo
        # derecho está pesado hacia la izquierda ("zigzag" del otro lado).
        if balance < -1 and _factor_balance(nodo.derecha) > 0:
            self._rotaciones["doble_derecha_izquierda"] += 1
            return _rotacion_doble_derecha_izquierda(nodo)

        # Ya estaba balanceado, no hace falta rotar.
        return nodo

    # --- Búsqueda (idéntica en espíritu a la del ABB del TP3) ---

    def buscar(self, clave: str) -> List[Cancion]:
        if not clave:
            return []
        nodo = self._buscar_nodo(self._raiz, clave)
        return list(nodo.elementos) if nodo is not None else []

    def existe(self, clave: str) -> bool:
        if not clave:
            return False
        return self._buscar_nodo(self._raiz, clave) is not None

    def _buscar_nodo(self, nodo: Optional[NodoAVL], clave: str) -> Optional[NodoAVL]:
        if nodo is None:
            return None

        clave_normalizada = _normalizar(clave)
        clave_nodo_normalizada = _normalizar(nodo.clave)

        if clave_normalizada == clave_nodo_normalizada:
            return nodo
        elif clave_normalizada < clave_nodo_normalizada:
            return self._buscar_nodo(nodo.izquierda, clave)
        else:
            return self._buscar_nodo(nodo.derecha, clave)

    # --- Recorridos (idénticos en espíritu a los del ABB del TP3) ---

    def inorder(self) -> List[str]:
        claves: List[str] = []
        self._inorder_recursivo(self._raiz, claves)
        return claves

    def _inorder_recursivo(self, nodo: Optional[NodoAVL], acumulador: List[str]) -> None:
        if nodo is None:
            return
        self._inorder_recursivo(nodo.izquierda, acumulador)
        acumulador.append(nodo.clave)
        self._inorder_recursivo(nodo.derecha, acumulador)

    def preorder(self) -> List[str]:
        claves: List[str] = []
        self._preorder_recursivo(self._raiz, claves)
        return claves

    def _preorder_recursivo(self, nodo: Optional[NodoAVL], acumulador: List[str]) -> None:
        if nodo is None:
            return
        acumulador.append(nodo.clave)
        self._preorder_recursivo(nodo.izquierda, acumulador)
        self._preorder_recursivo(nodo.derecha, acumulador)

    def postorder(self) -> List[str]:
        claves: List[str] = []
        self._postorder_recursivo(self._raiz, claves)
        return claves

    def _postorder_recursivo(self, nodo: Optional[NodoAVL], acumulador: List[str]) -> None:
        if nodo is None:
            return
        self._postorder_recursivo(nodo.izquierda, acumulador)
        self._postorder_recursivo(nodo.derecha, acumulador)
        acumulador.append(nodo.clave)

    # --- Verificación de invariante AVL (para tests / debug) ---

    def esta_balanceado(self) -> bool:
        """Recorre todo el árbol y confirma que el factor de balance de
        CADA nodo está entre -1 y 1. Si esto da False, hay un bug en la
        lógica de rotación.
        """
        return self._verificar_balance_recursivo(self._raiz)

    def _verificar_balance_recursivo(self, nodo: Optional[NodoAVL]) -> bool:
        if nodo is None:
            return True
        balance = _factor_balance(nodo)
        if balance < -1 or balance > 1:
            return False
        return self._verificar_balance_recursivo(nodo.izquierda) and \
            self._verificar_balance_recursivo(nodo.derecha)

    def imprimir(self) -> None:
        if self.esta_vacio():
            print(f"{self._nombre}: (árbol vacío)")
            return
        print(f"{self._nombre}:")
        self._imprimir_recursivo(self._raiz, nivel=0)

    def _imprimir_recursivo(self, nodo: Optional[NodoAVL], nivel: int) -> None:
        if nodo is None:
            return
        self._imprimir_recursivo(nodo.derecha, nivel + 1)
        sangria = "  " * nivel
        print(f"{sangria}{nodo.clave} (altura={nodo.altura}, balance={_factor_balance(nodo)})")
        self._imprimir_recursivo(nodo.izquierda, nivel + 1)

    def __len__(self) -> int:
        return self._cantidad_claves

    def __str__(self) -> str:
        return f"{self._nombre}({self._cantidad_claves} claves, altura={self.altura()})"


class ArbolAVLPorTitulo(ArbolAVL):
    """Especialización del AVL indexada por título de canción — misma
    semántica que `ArbolPorTitulo` del TP3, para poder comparar ambos
    árboles con el mismo dataset y el mismo criterio de clave.
    """

    def __init__(self):
        super().__init__(nombre="ArbolAVLPorTitulo")

    def insertar_cancion(self, cancion: Cancion) -> None:
        titulo = obtener_titulo_cancion(cancion)
        self.insertar(titulo, cancion)

    def cargar_desde_catalogo(self, catalogo) -> None:
        canciones = catalogo.listar() if hasattr(catalogo, "listar") else []
        for cancion in canciones:
            self.insertar_cancion(cancion)

    def buscar_por_titulo(self, titulo: str) -> List[Cancion]:
        return self.buscar(titulo)


if __name__ == "__main__":
    # --- Parte 1: demo con títulos reales, el peor caso para un ABB común ---
    arbol = ArbolAVLPorTitulo()

    titulos_ordenados = [
        "Ana", "Bailarina", "Carla", "Diana", "Elena",
        "Fabiola", "Gina", "Helena", "Irene", "Julia",
    ]

    for i, titulo in enumerate(titulos_ordenados):
        arbol.insertar_cancion(Cancion(i, titulo, "Miranda!"))

    print(f"Insertados {len(titulos_ordenados)} títulos YA ORDENADOS alfabéticamente.")
    print(f"Altura del AVL: {arbol.altura()}  (un ABB común degeneraría a altura {len(titulos_ordenados)})")
    print(f"¿Está balanceado?: {arbol.esta_balanceado()}")
    print(f"Rotaciones disparadas: {arbol.rotaciones}")
    print(f"\nRaíz del árbol: '{arbol.raiz.clave}'")
    print("\nVisualización:")
    arbol.imprimir()

    # --- Parte 2: un ejemplo mínimo de CADA una de las 4 rotaciones,
    # con claves de una sola letra elegidas específicamente para
    # disparar cada caso (esto es lo que pide el criterio de
    # aceptación: "probado con al menos un ejemplo de cada uno"). ---

    print("\n" + "=" * 60)
    print("EJEMPLOS MÍNIMOS DE CADA ROTACIÓN")
    print("=" * 60)

    casos = {
        "Simple Derecha (Izquierda-Izquierda)": ["C", "B", "A"],
        "Simple Izquierda (Derecha-Derecha)": ["A", "B", "C"],
        "Doble Izquierda-Derecha": ["C", "A", "B"],
        "Doble Derecha-Izquierda": ["A", "C", "B"],
    }

    for nombre_caso, claves in casos.items():
        arbol_caso = ArbolAVL(nombre=nombre_caso)
        for clave in claves:
            arbol_caso.insertar(clave)

        print(f"\n{nombre_caso}")
        print(f"  Claves insertadas en orden: {claves}")
        print(f"  Raíz resultante: '{arbol_caso.raiz.clave}'  (debe quedar la del medio, ej. 'B')")
        print(f"  Rotaciones disparadas: {arbol_caso.rotaciones}")
        print(f"  ¿Balanceado?: {arbol_caso.esta_balanceado()}")
        assert arbol_caso.esta_balanceado(), f"El árbol del caso '{nombre_caso}' no quedó balanceado"
        assert sum(arbol_caso.rotaciones.values()) == 1, f"Se esperaba exactamente 1 rotación en '{nombre_caso}'"

    print("\n✔ Los 4 casos dispararon exactamente 1 rotación cada uno, y quedaron balanceados.")