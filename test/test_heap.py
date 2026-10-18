"""
Tests unitarios para el Heap Binario, función de prioridad y ranking Top-N (TP6 / Versión 4).
"""

import unittest
from estructuras.heap import MaxHeap
from algoritmos.prioridad import obtener_prioridad
from modelos.cancion import Cancion
from servicios.gestor_catalogo import Catalogo
from algoritmos.ranking import obtener_top_n


class TestHeapYPrioridad(unittest.TestCase):

    def test_funcion_prioridad(self):
        c1 = Cancion(1, "Tema A", "Artista 1", popularidad=80.5)
        c2 = Cancion(2, "Tema B", "Artista 2", popularidad=95.0)
        self.assertEqual(obtener_prioridad(c2), 95.0)
        self.assertEqual(obtener_prioridad(c1), 80.5)

    def test_max_heap_operaciones(self):
        heap = MaxHeap(key=lambda x: x)
        heap.insertar(10)
        heap.insertar(50)
        heap.insertar(20)

        self.assertEqual(heap.extraer_maximo(), 50)
        self.assertEqual(heap.extraer_maximo(), 20)
        self.assertEqual(heap.extraer_maximo(), 10)
        self.assertTrue(heap.esta_vacio())

    def test_top_n_con_catalogo_real(self):
        cat = Catalogo()
        cat.cargar_desde_json("datos/miranda_canciones.json")
        
        top_5 = obtener_top_n(cat, n=5)
        self.assertEqual(len(top_5), 5)
        
        # Verificamos que estén ordenados de mayor a menor prioridad
        prioridades = [obtener_prioridad(c) for c in top_5]
        self.assertEqual(prioridades, sorted(prioridades, reverse=True))


if __name__ == "__main__":
    unittest.main()