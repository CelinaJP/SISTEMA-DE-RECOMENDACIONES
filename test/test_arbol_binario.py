"""
Tests unitarios del Árbol Binario de Búsqueda (ABB).

Cubre: inserción, búsqueda, recorridos (inorder/preorder/postorder) y
casos borde: árbol vacío, una sola clave, clave duplicada (agrupación) y
clave inexistente.

Cómo correrlos:
    python3 -m unittest discover -s tests -v
o, apuntando solo a este archivo:
    python3 -m unittest tests.test_arbol_binario -v
"""

import unittest

from modelos.cancion import Cancion
from estructuras.arbol_binario import (
    ArbolBinarioBusqueda,
    ArbolPorTitulo,
    ArbolPorArtista,
)


class TestArbolBinarioBusquedaGenerico(unittest.TestCase):
    """Tests sobre la clase base genérica, usando claves de texto simples
    (sin depender de `Cancion`) para probar la estructura en sí.
    """

    def setUp(self):
        self.arbol = ArbolBinarioBusqueda(nombre="ArbolDePrueba")

    # --- Caso borde: árbol vacío ---

    def test_arbol_vacio_al_crear(self):
        self.assertTrue(self.arbol.esta_vacio())
        self.assertEqual(self.arbol.cantidad_claves, 0)
        self.assertIsNone(self.arbol.raiz)

    def test_buscar_en_arbol_vacio_devuelve_lista_vacia(self):
        self.assertEqual(self.arbol.buscar("cualquier cosa"), [])

    def test_existe_en_arbol_vacio_devuelve_false(self):
        self.assertFalse(self.arbol.existe("cualquier cosa"))

    def test_recorridos_en_arbol_vacio_devuelven_lista_vacia(self):
        self.assertEqual(self.arbol.inorder(), [])
        self.assertEqual(self.arbol.preorder(), [])
        self.assertEqual(self.arbol.postorder(), [])

    def test_insertar_clave_vacia_lanza_excepcion(self):
        with self.assertRaises(ValueError):
            self.arbol.insertar("")

    # --- Caso borde: una sola clave ---

    def test_insertar_una_sola_clave(self):
        self.arbol.insertar("Pop")
        self.assertFalse(self.arbol.esta_vacio())
        self.assertEqual(self.arbol.cantidad_claves, 1)
        self.assertEqual(self.arbol.raiz.clave, "Pop")

    def test_buscar_clave_unica_existente(self):
        cancion = Cancion(1, "Bailarina", "Miranda!")
        self.arbol.insertar("Pop", cancion)
        resultado = self.arbol.buscar("Pop")
        self.assertEqual(len(resultado), 1)
        self.assertIs(resultado[0], cancion)

    # --- Caso borde: clave duplicada (misma clave insertada más de una vez) ---

    def test_insertar_clave_duplicada_no_crea_nodo_nuevo(self):
        c1 = Cancion(1, "Bailarina", "Miranda!")
        c2 = Cancion(2, "Perdonarte", "Miranda!")
        self.arbol.insertar("Pop", c1)
        self.arbol.insertar("Pop", c2)

        self.assertEqual(self.arbol.cantidad_claves, 1)  # sigue siendo un solo nodo
        resultado = self.arbol.buscar("Pop")
        self.assertEqual(len(resultado), 2)  # pero agrupa ambas canciones

    def test_insertar_misma_cancion_dos_veces_no_duplica(self):
        c1 = Cancion(1, "Bailarina", "Miranda!")
        self.arbol.insertar("Pop", c1)
        self.arbol.insertar("Pop", c1)  # se intenta insertar el mismo id de nuevo

        resultado = self.arbol.buscar("Pop")
        self.assertEqual(len(resultado), 1)  # no se duplica por id

    def test_clave_duplicada_es_insensible_a_mayusculas_y_acentos(self):
        self.arbol.insertar("Electropop")
        self.arbol.insertar("electropop")
        self.arbol.insertar("ELECTROPOP")

        self.assertEqual(self.arbol.cantidad_claves, 1)

    # --- Caso borde: clave inexistente ---

    def test_buscar_clave_inexistente_devuelve_lista_vacia(self):
        self.arbol.insertar("Pop", Cancion(1, "Bailarina", "Miranda!"))
        self.assertEqual(self.arbol.buscar("Rock"), [])

    def test_existe_clave_inexistente_devuelve_false(self):
        self.arbol.insertar("Pop", Cancion(1, "Bailarina", "Miranda!"))
        self.assertFalse(self.arbol.existe("Rock"))

    # --- Recorridos con varios elementos ---

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

    def test_preorder_empieza_por_la_raiz(self):
        for clave in ["Pop Rock", "Electropop", "Synthpop", "Balada Pop"]:
            self.arbol.insertar(clave)

        self.assertEqual(self.arbol.preorder()[0], self.arbol.raiz.clave)

    def test_postorder_termina_en_la_raiz(self):
        for clave in ["Pop Rock", "Electropop", "Synthpop", "Balada Pop"]:
            self.arbol.insertar(clave)

        self.assertEqual(self.arbol.postorder()[-1], self.arbol.raiz.clave)

    def test_imprimir_no_lanza_excepcion_arbol_vacio_y_con_datos(self):
        # imprimir() solo debe funcionar sin romper, no se valida su salida
        # exacta por consola (test de "no explota", no de contenido visual).
        try:
            self.arbol.imprimir()  # árbol vacío
            self.arbol.insertar("Pop")
            self.arbol.imprimir()  # árbol con datos
        except Exception as e:
            self.fail(f"imprimir() no debería lanzar excepciones: {e}")


class TestArbolPorTitulo(unittest.TestCase):
    """Tests de la especialización por título, incluyendo el caso real
    del proyecto: versión clásica y moderna con el mismo título.
    """

    def setUp(self):
        self.arbol = ArbolPorTitulo()

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

        self.assertEqual(self.arbol.cantidad_claves, 1)  # un solo nodo "Traición"
        resultado = self.arbol.buscar_por_titulo("Traición")
        self.assertEqual(len(resultado), 2)
        self.assertIn(clasica, resultado)
        self.assertIn(moderna, resultado)

    def test_titulo_inexistente(self):
        self.arbol.insertar_cancion(Cancion(1, "Bailarina", "Miranda!"))
        self.assertEqual(self.arbol.buscar_por_titulo("No Existe"), [])

    def test_inorder_devuelve_titulos_ordenados(self):
        for titulo in ["Yo Te Diré", "Bailarina", "MEJOR QUE VOS"]:
            self.arbol.insertar_cancion(Cancion(len(titulo), titulo, "Miranda!"))

        self.assertEqual(
            self.arbol.inorder(),
            ["Bailarina", "MEJOR QUE VOS", "Yo Te Diré"],
        )


class TestArbolPorArtista(unittest.TestCase):
    """Tests de la especialización por artista, incluyendo colaboradores."""

    def setUp(self):
        self.arbol = ArbolPorArtista()

    def test_arbol_vacio(self):
        self.assertTrue(self.arbol.esta_vacio())
        self.assertEqual(self.arbol.buscar_por_artista("Miranda!"), [])

    def test_insertar_una_cancion_indexa_por_artista_principal(self):
        cancion = Cancion(1, "Bailarina", "Miranda!")
        self.arbol.insertar_cancion(cancion)

        resultado = self.arbol.buscar_por_artista("Miranda!")
        self.assertEqual(resultado, [cancion])

    def test_artista_con_varias_canciones_se_agrupan_en_un_nodo(self):
        c1 = Cancion(1, "Bailarina", "Miranda!")
        c2 = Cancion(2, "Perdonarte", "Miranda!")

        self.arbol.insertar_cancion(c1)
        self.arbol.insertar_cancion(c2)

        self.assertEqual(self.arbol.cantidad_claves, 1)  # un solo nodo "Miranda!"
        resultado = self.arbol.buscar_por_artista("Miranda!")
        self.assertEqual(len(resultado), 2)

    def test_colaborador_tambien_queda_indexado(self):
        cancion = Cancion(112, "MEJOR QUE VOS", "Miranda!", colaboradores=["Lali"])
        self.arbol.insertar_cancion(cancion)

        # La canción debe encontrarse tanto por el artista principal...
        self.assertEqual(self.arbol.buscar_por_artista("Miranda!"), [cancion])
        # ...como por el colaborador.
        self.assertEqual(self.arbol.buscar_por_artista("Lali"), [cancion])

    def test_artista_inexistente(self):
        self.arbol.insertar_cancion(Cancion(1, "Bailarina", "Miranda!"))
        self.assertEqual(self.arbol.buscar_por_artista("Bad Bunny"), [])


if __name__ == "__main__":
    unittest.main()