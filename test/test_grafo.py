"""
Tests unitarios para el Grafo de Colaboraciones y algoritmos de recorrido (TP7, TP8, TP9).
"""

import unittest
import sys
import os

# Aseguramos que Python encuentre los módulos del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from estructuras.grafo import GrafoColaboraciones
from modelos.cancion import Cancion

class MockCatalogo:
    """Catálogo simulado para inyectar datos controlados en los tests."""
    def __init__(self, canciones):
        self._canciones = canciones
        
    def listar(self):
        return self._canciones

class TestGrafoColaboraciones(unittest.TestCase):

    def setUp(self):
        self.grafo = GrafoColaboraciones()
        
        # Escenario de prueba para Dijkstra:
        # Miranda! -> Lali (Popularidad 90 -> Costo 10)
        # Lali -> FMK (Popularidad 80 -> Costo 20)
        # Miranda! -> FMK (Popularidad 50 -> Costo 50)
        #
        # El camino directo Miranda! -> FMK cuesta 50.
        # El camino indirecto Miranda! -> Lali -> FMK cuesta 30 (10 + 20).
        # Dijkstra DEBE elegir el camino indirecto.
        
        c1 = Cancion(1, "Cancion A", "Miranda!", colaboradores=["Lali"], popularidad=90)
        c2 = Cancion(2, "Cancion B", "Lali", colaboradores=["FMK"], popularidad=80)
        c3 = Cancion(3, "Cancion C", "Miranda!", colaboradores=["FMK"], popularidad=50)
        
        catalogo_mock = MockCatalogo([c1, c2, c3])
        self.grafo.cargar_desde_catalogo(catalogo_mock)

    def test_dijkstra_encuentra_camino_optimo_indirecto(self):
        camino, costo = self.grafo.camino_mas_fuerte_dijkstra("Miranda!", "FMK")
        
        self.assertIsNotNone(camino)
        # Debe preferir el desvío por Lali porque es más "barato" (fuerte)
        self.assertEqual(camino, ["Miranda!", "Lali", "FMK"])
        self.assertEqual(costo, 30.0)

    def test_dijkstra_nodos_desconectados(self):
        self.grafo.agregar_vertice("Artista Solitario")
        camino, costo = self.grafo.camino_mas_fuerte_dijkstra("Miranda!", "Artista Solitario")
        
        self.assertIsNone(camino)
        self.assertEqual(costo, float('inf'))

    def test_dijkstra_nodo_inexistente(self):
        camino, costo = self.grafo.camino_mas_fuerte_dijkstra("Miranda!", "Inexistente")
        
        self.assertIsNone(camino)
        self.assertEqual(costo, float('inf'))
        
    def test_bfs_grados_separacion(self):
        # FMK está a 1 grado de Miranda! (por Cancion C) y a 1 grado de Lali (por Cancion B)
        indirectas = self.grafo.buscar_conexiones_indirectas("Miranda!", grados=1)
        self.assertIn("FMK", indirectas)
        self.assertIn("Lali", indirectas)

if __name__ == "__main__":
    unittest.main()
    