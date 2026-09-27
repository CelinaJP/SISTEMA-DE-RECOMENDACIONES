"""
Tests unitarios del Árbol AVL (TP4).

Cubre: casos borde (árbol vacío, una sola clave, clave duplicada, clave
inexistente), las 4 rotaciones (simple izquierda, simple derecha, doble
izquierda-derecha, doble derecha-izquierda) probadas una por una, y la
verificación de que el árbol nunca se desbalancea ni siquiera con el
peor caso que sí rompe al BST común (datos ya ordenados).

Cómo correrlos:
    python3 -m unittest discover -s test -v
o, apuntando solo a este archivo:
    python3 -m unittest test.test_arbol_avl -v
"""

import unittest

from modelos.cancion import Cancion
from estructuras.arbol_avl import ArbolAVL, ArbolAVLPorTitulo


class TestArbolAVLGenerico(unittest.TestCase):
    """Tests sobre la clase base genérica, con claves de texto simples."""

    def setUp(self):
        self.arbol = ArbolAVL(nombre="AVLDePrueba")

    # --- Caso borde: árbol vacío ---

    def test_arbol_vacio_al_crear(self):
        self.assertTrue(self.arbol.esta_vacio())
        self.assertEqual(self.arbol.cantidad_claves, 0)
        self.assertIsNone(self.arbol.raiz)
        self.assertEqual(self.arbol.altura(), 0)

    def test_buscar_en_arbol_vacio_devuelve_lista_vacia(self):
        self.assertEqual(self.arbol.buscar("cualquier cosa"), [])

    def test_existe_en_arbol_vacio_devuelve_false(self):
        self.assertFalse(self.arbol.existe("cualquier cosa"))

    def test_recorridos_en_arbol_vacio_devuelven_lista_vacia(self):
        self.assertEqual(self.arbol.inorder(), [])
        self.assertEqual(self.arbol.preorder(), [])
        self.assertEqual(self.arbol.postorder(), [])

    def test_arbol_vacio_esta_balanceado(self):
        # Un árbol vacío se considera trivialmente balanceado.
        self.assertTrue(self.arbol.esta_balanceado())

    def test_insertar_clave_vacia_lanza_excepcion(self):
        with self.assertRaises(ValueError):
            self.arbol.insertar("")

    # --- Caso borde: una sola clave ---

    def test_insertar_una_sola_clave(self):
        self.arbol.insertar("Pop")
        self.assertFalse(self.arbol.esta_vacio())
        self.assertEqual(self.arbol.cantidad_claves, 1)
        self.assertEqual(self.arbol.raiz.clave, "Pop")
        self.assertEqual(self.arbol.altura(), 1)
        self.assertTrue(self.arbol.esta_balanceado())

    def test_buscar_clave_unica_existente(self):
        cancion = Cancion(1, "Bailarina", "Miranda!")
        self.arbol.insertar("Pop", cancion)
        resultado = self.arbol.buscar("Pop")
        self.assertEqual(len(resultado), 1)
        self.assertIs(resultado[0], cancion)

    # --- Caso borde: clave duplicada ---

    def test_insertar_clave_duplicada_no_crea_nodo_nuevo(self):
        c1 = Cancion(1, "Bailarina", "Miranda!")
        c2 = Cancion(2, "Perdonarte", "Miranda!")
        self.arbol.insertar("Pop", c1)
        self.arbol.insertar("Pop", c2)

        self.assertEqual(self.arbol.cantidad_claves, 1)
        resultado = self.arbol.buscar("Pop")
        self.assertEqual(len(resultado), 2)

    def test_clave_duplicada_no_dispara_rotaciones(self):
        # Insertar la misma clave dos veces no cambia la altura, así que
        # no debería disparar ninguna rotación.
        self.arbol.insertar("Pop", Cancion(1, "Bailarina", "Miranda!"))
        self.arbol.insertar("Pop", Cancion(2, "Perdonarte", "Miranda!"))
        self.assertEqual(sum(self.arbol.rotaciones.values()), 0)

    # --- Caso borde: clave inexistente ---

    def test_buscar_clave_inexistente_devuelve_lista_vacia(self):
        self.arbol.insertar("Pop", Cancion(1, "Bailarina", "Miranda!"))
        self.assertEqual(self.arbol.buscar("Rock"), [])

    def test_existe_clave_inexistente_devuelve_false(self):
        self.arbol.insertar("Pop", Cancion(1, "Bailarina", "Miranda!"))
        self.assertFalse(self.arbol.existe("Rock"))

    # --- Las 4 rotaciones, cada una probada individualmente ---

    def test_rotacion_simple_derecha_caso_izquierda_izquierda(self):
        # Insertar en orden DECRECIENTE fuerza el caso Izquierda-Izquierda.
        for clave in ["C", "B", "A"]:
            self.arbol.insertar(clave)

        self.assertEqual(self.arbol.raiz.clave, "B")
        self.assertEqual(self.arbol.rotaciones["simple_derecha"], 1)
        self.assertEqual(sum(self.arbol.rotaciones.values()), 1)
        self.assertTrue(self.arbol.esta_balanceado())

    def test_rotacion_simple_izquierda_caso_derecha_derecha(self):
        # Insertar en orden CRECIENTE fuerza el caso Derecha-Derecha.
        for clave in ["A", "B", "C"]:
            self.arbol.insertar(clave)

        self.assertEqual(self.arbol.raiz.clave, "B")
        self.assertEqual(self.arbol.rotaciones["simple_izquierda"], 1)
        self.assertEqual(sum(self.arbol.rotaciones.values()), 1)
        self.assertTrue(self.arbol.esta_balanceado())

    def test_rotacion_doble_izquierda_derecha(self):
        # El hijo izquierdo queda "pesado" hacia la derecha (zigzag).
        for clave in ["C", "A", "B"]:
            self.arbol.insertar(clave)

        self.assertEqual(self.arbol.raiz.clave, "B")
        self.assertEqual(self.arbol.rotaciones["doble_izquierda_derecha"], 1)
        self.assertEqual(sum(self.arbol.rotaciones.values()), 1)
        self.assertTrue(self.arbol.esta_balanceado())

    def test_rotacion_doble_derecha_izquierda(self):
        # El hijo derecho queda "pesado" hacia la izquierda (zigzag).
        for clave in ["A", "C", "B"]:
            self.arbol.insertar(clave)

        self.assertEqual(self.arbol.raiz.clave, "B")
        self.assertEqual(self.arbol.rotaciones["doble_derecha_izquierda"], 1)
        self.assertEqual(sum(self.arbol.rotaciones.values()), 1)
        self.assertTrue(self.arbol.esta_balanceado())

    # --- El caso que degenera al BST común: acá el AVL no debe romperse ---

    def test_insertar_claves_ordenadas_mantiene_balance(self):
        # Este es exactamente el escenario que degrada al BST común del
        # TP3 a una lista enlazada (y que puede crashear con N grande).
        # El AVL tiene que mantenerse balanceado con altura ~log2(N).
        claves_ordenadas = [f"Cancion {str(i).zfill(3)}" for i in range(100)]
        for clave in claves_ordenadas:
            self.arbol.insertar(clave)

        self.assertTrue(self.arbol.esta_balanceado())
        # Altura ideal para 100 elementos es ~7 (log2(100) ≈ 6.64);
        # se da margen razonable en vez de exigir el valor exacto.
        self.assertLessEqual(self.arbol.altura(), 8)
        self.assertGreater(sum(self.arbol.rotaciones.values()), 0)  # tuvo que rebalancear

    # --- Recorridos ---

    def test_inorder_queda_alfabeticamente_ordenado(self):
        for clave in ["Pop Rock", "Electropop", "Synthpop", "Balada Pop"]:
            self.arbol.insertar(clave)

        self.assertEqual(
            self.arbol.inorder(),
            ["Balada Pop", "Electropop", "Pop Rock", "Synthpop"],
        )

    def test_preorder_y_postorder_visitan_las_mismas_claves_que_inorder(self):
        for clave in ["Pop Rock", "Electropop", "Synthpop", "Balada Pop"]:
            self.arbol.insertar(clave)

        inorder = self.arbol.inorder()
        preorder = self.arbol.preorder()
        postorder = self.arbol.postorder()

        self.assertEqual(len(inorder), len(preorder))
        self.assertEqual(len(inorder), len(postorder))
        self.assertEqual(set(inorder), set(preorder))
        self.assertEqual(set(inorder), set(postorder))

    def test_imprimir_no_lanza_excepcion_arbol_vacio_y_con_datos(self):
        try:
            self.arbol.imprimir()
            self.arbol.insertar("Pop")
            self.arbol.imprimir()
        except Exception as e:
            self.fail(f"imprimir() no debería lanzar excepciones: {e}")


class TestArbolAVLPorTitulo(unittest.TestCase):
    """Tests de la especialización por título, incluyendo el caso real
    del proyecto: versión clásica y moderna con el mismo título.
    """

    def setUp(self):
        self.arbol = ArbolAVLPorTitulo()

    def test_arbol_vacio(self):
        self.assertTrue(self.arbol.esta_vacio())
        self.assertEqual(self.arbol.buscar_por_titulo("Traición"), [])

    def test_insertar_una_cancion(self):
        cancion = Cancion(1, "Bailarina", "Miranda!")
        self.arbol.insertar_cancion(cancion)

        self.assertEqual(self.arbol.cantidad_claves, 1)
        resultado = self.arbol.buscar_por_titulo("Bailarina")
        self.assertEqual(resultado, [cancion])

    def test_titulo_duplicado_version_clasica_y_moderna(self):
        clasica = Cancion(21, "Traición", "Miranda!", era="Clásica")
        moderna = Cancion(103, "Traición", "Miranda!", era="Moderna")

        self.arbol.insertar_cancion(clasica)
        self.arbol.insertar_cancion(moderna)

        self.assertEqual(self.arbol.cantidad_claves, 1)
        resultado = self.arbol.buscar_por_titulo("Traición")
        self.assertEqual(len(resultado), 2)
        self.assertIn(clasica, resultado)
        self.assertIn(moderna, resultado)

    def test_titulo_inexistente(self):
        self.arbol.insertar_cancion(Cancion(1, "Bailarina", "Miranda!"))
        self.assertEqual(self.arbol.buscar_por_titulo("No Existe"), [])

    def test_se_mantiene_balanceado_con_titulos_reales_ordenados(self):
        # Mismo escenario que rompe al BST común del TP3, pero acá con
        # títulos reales en vez de claves de una letra.
        titulos = ["Ana", "Bailarina", "Carla", "Diana", "Elena", "Fabiola", "Gina"]
        for i, titulo in enumerate(titulos):
            self.arbol.insertar_cancion(Cancion(i, titulo, "Miranda!"))

        self.assertTrue(self.arbol.esta_balanceado())
        self.assertLessEqual(self.arbol.altura(), 4)  # log2(7) ≈ 2.8, con margen


if __name__ == "__main__":
    unittest.main()