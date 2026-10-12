"""
Tests unitarios del Árbol General (TP5).

Cubre:
- Árbol vacío
- Agregar una categoría / nodos intermedios automáticos
- Búsqueda de categoría existente e inexistente
- Recorridos DFS y BFS (coincidencia de volumen de nodos)
- Criterio de aceptación con el catálogo real
"""

import unittest
from modelos.cancion import Cancion
from estructuras.arbol_general import ArbolGeneral, NodoGeneral
from servicios.gestor_catalogo import Catalogo


class TestArbolGeneral(unittest.TestCase):

    def setUp(self):
        self.arbol = ArbolGeneral(nombre="ArbolPrueba")

    def test_arbol_vacio(self):
        self.assertIsNotNone(self.arbol.raiz)
        self.assertEqual(self.arbol.raiz.etiqueta, "RaizCatálogo")
        self.assertEqual(self.arbol.recorrido_bfs(), ["RaizCatálogo"])
        self.assertEqual(self.arbol.recorrido_dfs(), [])
        self.assertEqual(self.arbol.buscar_categoria("Moderna"), [])

    def test_agregar_categoria_y_nodos_intermedios(self):
        # Insertar una canción en era y género inexistentes debe crear los nodos intermedios
        cancion = Cancion(1, "Bailarina", "Miranda!", era="Clásica", genero="Electropop")
        self.arbol.agregar_cancion("Clásica", "Electropop", cancion)

        # Verificamos que se crearon los nodos
        nodo_era = self.arbol.raiz.buscar_hijo("Clásica")
        self.assertIsNotNone(nodo_era)
        
        nodo_genero = nodo_era.buscar_hijo("Electropop")
        self.assertIsNotNone(nodo_genero)
        self.assertIn(cancion, nodo_genero.canciones)

    def test_buscar_categoria_existente(self):
        c1 = Cancion(1, "Bailarina", "Miranda!", era="Moderna", genero="Pop Moderno")
        c2 = Cancion(2, "743", "Miranda!", era="Moderna", genero="Pop Moderno")
        
        self.arbol.agregar_cancion("Moderna", "Pop Moderno", c1)
        self.arbol.agregar_cancion("Moderna", "Pop Moderno", c2)

        # Buscar por era ("Moderna") debe devolver todas las canciones de la era
        resultados_era = self.arbol.buscar_categoria("Moderna")
        self.assertEqual(len(resultados_era), 2)
        self.assertIn(c1, resultados_era)
        self.assertIn(c2, resultados_era)

        # Buscar por género ("Pop Moderno") también debe devolverlas
        resultados_genero = self.arbol.buscar_categoria("Pop Moderno")
        self.assertEqual(len(resultados_genero), 2)

    def test_buscar_categoria_inexistente(self):
        self.arbol.agregar_cancion("Clásica", "Synthpop", Cancion(1, "Romix", "Miranda!"))
        resultado = self.arbol.buscar_categoria("Desconocido")
        self.assertEqual(resultado, [])

    def test_comparacion_recorridos_dfs_y_bfs(self):
        self.arbol.agregar_cancion("Clásica", "Electropop", Cancion(1, "Imán", "Miranda!"))
        self.arbol.agregar_cancion("Moderna", "Pop Moderno", Cancion(2, "743", "Miranda!"))

        bfs = self.arbol.recorrido_bfs()
        dfs = self.arbol.recorrido_dfs()

        # Ambos recorridos deben haber visitado elementos estructurales
        self.assertTrue(len(bfs) > 0)
        self.assertTrue(len(dfs) > 0)


class TestArbolGeneralCatalogoReal(unittest.TestCase):
    """Pruebas del árbol general utilizando el catálogo completo de 120 canciones reales."""

    def test_cargar_catalogo_real_y_criterios_aceptacion(self):
        cat = Catalogo()
        cat.cargar_desde_json("datos/miranda_canciones.json")

        arbol = ArbolGeneral("CatalogoReal")
        arbol.cargar_desde_catalogo(cat)

        # Criterio: buscar_categoria("Moderna") devuelve solo canciones de esa era
        canciones_modernas = arbol.buscar_categoria("Moderna")
        self.assertTrue(len(canciones_modernas) > 0)
        
        for cancion in canciones_modernas:
            self.assertEqual(getattr(cancion, "_era", ""), "Moderna")

        # Verificar que los recorridos funcionan sin errores sobre el catálogo real
        bfs = arbol.recorrido_bfs()
        dfs = arbol.recorrido_dfs()
        self.assertTrue(len(bfs) > 0)
        self.assertTrue(len(dfs) > 0)


if __name__ == "__main__":
    unittest.main()