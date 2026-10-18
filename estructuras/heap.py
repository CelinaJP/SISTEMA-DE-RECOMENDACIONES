"""
Implementación manual de un Heap Binario (Max-Heap) para la Cola de Prioridad.
"""

class MaxHeap:
    def __init__(self, key=lambda x: x):
        """
        Inicializa el Heap. 
        key: función opcional para extraer el valor numérico de prioridad de cada elemento.
        """
        self._elementos = []
        self._key = key

    def esta_vacio(self) -> bool:
        return len(self._elementos) == 0

    def _padre(self, i: int) -> int:
        return (i - 1) // 2

    def _hijo_izquierdo(self, i: int) -> int:
        return 2 * i + 1

    def _hijo_derecho(self, i: int) -> int:
        return 2 * i + 2

    def _flotar(self, i: int):
        """Sube el elemento en la posición i si es mayor que su padre (Max-Heap)."""
        while i > 0 and self._key(self._elementos[i]) > self._key(self._elementos[self._padre(i)]):
            padre = self._padre(i)
            self._elementos[i], self._elementos[padre] = self._elementos[padre], self._elementos[i]
            i = padre

    def _hundir(self, i: int):
        """Baja el elemento en la posición i si es menor que alguno de sus hijos."""
        mayor = i
        izq = self._hijo_izquierdo(i)
        der = self._hijo_derecho(i)
        n = len(self._elementos)

        if izq < n and self._key(self._elementos[izq]) > self._key(self._elementos[mayor]):
            mayor = izq

        if der < n and self._key(self._elementos[der]) > self._key(self._elementos[mayor]):
            mayor = der

        if mayor != i:
            self._elementos[i], self._elementos[mayor] = self._elementos[mayor], self._elementos[i]
            self._hundir(mayor)

    def insertar(self, elemento):
        """Inserta un nuevo elemento en el heap manteniendo la propiedad de orden."""
        self._elementos.append(elemento)
        self._flotar(len(self._elementos) - 1)

    def extraer_maximo(self):
        """Extrae y retorna el elemento con mayor prioridad (la raíz)."""
        if self.esta_vacio():
            return None
        
        if len(self._elementos) == 1:
            return self._elementos.pop()

        raiz = self._elementos[0]
        self._elementos[0] = self._elementos.pop()
        self._hundir(0)
        return raiz

    def __len__(self) -> int:
        return len(self._elementos)