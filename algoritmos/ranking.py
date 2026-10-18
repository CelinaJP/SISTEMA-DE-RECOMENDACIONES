"""
Lógica para obtener el Top-N eficiente utilizando el MaxHeap.
"""
from estructuras.heap import MaxHeap
from algoritmos.prioridad import obtener_prioridad

def obtener_top_n(catalogo, n: int = 5) -> list:
    """
    Retorna las mejores N canciones del catálogo de forma eficiente 
    utilizando una cola de prioridad (Heap).
    """
    canciones = []
    if hasattr(catalogo, "listar"):
        canciones = catalogo.listar()
    elif hasattr(catalogo, "canciones"):
        canciones = catalogo.canciones
    else:
        return []

    # Inicializamos el Heap pasando la función de prioridad como key
    heap = MaxHeap(key=obtener_prioridad)

    # Insertamos todas las canciones en el heap
    for cancion in canciones:
        heap.insertar(cancion)

    # Extraemos los N elementos principales
    resultado = []
    for _ in range(min(n, len(heap))):
        c = heap.extraer_maximo()
        if c:
            resultado.append(c)

    return resultado