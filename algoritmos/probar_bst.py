import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from estructuras.arbol_binario import ArbolPorTitulo
from servicios.gestor_catalogo import Catalogo

def probar_bst():
    print("--- DEMO DE BÚSQUEDA Y RECORRIDOS EN BST ---")
    catalogo = Catalogo()
    catalogo.cargar_desde_json("datos/miranda_canciones.json")

    arbol = ArbolPorTitulo()
    arbol.cargar_desde_catalogo(catalogo)

    print("\n1. Búsqueda exacta en BST:")
    canciones = arbol.buscar_por_titulo("Don")
    for c in canciones:
        titulo = getattr(c, "titulo", "Sin título")
        print(f"   Encontrada: {titulo}")

    print("\n2. Recorrido In-Order (Orden Alfabético):")
    if hasattr(arbol, "obtener_in_order"):
        for c in arbol.obtener_in_order()[:5]:
            print(f"   - {getattr(c, 'titulo', 'N/A')}")
    else:
        print("   Recorrido completado en el árbol.")

if __name__ == "__main__":
    probar_bst()