"""
Genera casos donde el ABB común del TP3 (`ArbolPorTitulo`) queda
desbalanceado, y compara su altura contra la del AVL (`ArbolAVLPorTitulo`)
en el mismo escenario.
 
El peor caso clásico para un ABB común es insertar las claves YA
ORDENADAS: cada clave nueva es siempre mayor (o siempre menor) que la
anterior, así que el árbol nunca se ramifica — degenera en una lista
enlazada, con altura O(N) en vez de O(log N).
 
Uso:
    python algoritmos/generar_casos_desbalance.py
"""
 
import math
import os
import sys
 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 
from modelos.cancion import Cancion
from estructuras.arbol_binario import ArbolPorTitulo
from estructuras.arbol_avl import ArbolAVLPorTitulo
 
 
def calcular_altura_bst(nodo) -> int:
    """El ABB común (TP3) no tiene método `altura()` propio, así que la
    calculamos desde afuera recorriendo los punteros izquierda/derecha
    (que sí son públicos, vía @property).
    """
    if nodo is None:
        return 0
    return 1 + max(calcular_altura_bst(nodo.izquierda), calcular_altura_bst(nodo.derecha))
 
 
def generar_titulos_ordenados(n: int):
    """Genera N títulos con padding de ceros para que el orden alfabético
    de los strings coincida con el orden numérico (ej. 'Cancion 007' <
    'Cancion 010'), y así garantizar que se insertan en el peor orden
    posible para un ABB común.
    """
    ancho = len(str(n))
    return [f"Cancion {str(i).zfill(ancho)}" for i in range(n)]
 
 
def caso_peor_escenario(n: int):
    """Inserta N títulos ya ordenados en ambos árboles y compara alturas.
 
    Con N grande, el BST común puede degenerar tanto (una cadena lineal
    de N nodos) que la inserción recursiva excede el límite de recursión
    de Python — esto se captura y se reporta como hallazgo, porque es en
    sí mismo una demostración contundente del problema: un BST
    desbalanceado no solo es "más lento", puede directamente CRASHEAR.
    """
    titulos = generar_titulos_ordenados(n)
 
    bst = ArbolPorTitulo()
    avl = ArbolAVLPorTitulo()
 
    altura_bst = None
    bst_crasheo = False
 
    for i, titulo in enumerate(titulos):
        cancion = Cancion(i, titulo, "Artista Sintetico")
        if not bst_crasheo:
            try:
                bst.insertar_cancion(cancion)
            except RecursionError:
                bst_crasheo = True
        avl.insertar_cancion(cancion)
 
    if not bst_crasheo:
        altura_bst = calcular_altura_bst(bst.raiz)
 
    altura_avl = avl.altura()
    altura_ideal = math.floor(math.log2(n)) + 1 if n > 0 else 0
 
    return {
        "n": n,
        "altura_bst": altura_bst,
        "bst_crasheo": bst_crasheo,
        "altura_avl": altura_avl,
        "altura_ideal_log2n": altura_ideal,
        "avl_balanceado": avl.esta_balanceado(),
    }
 
 
def caso_orden_aleatorio(n: int, semilla: int = 42):
    """Contraejemplo: si los datos se insertan en un orden ALEATORIO (más
    parecido a cómo llegan las canciones reales), el ABB común NO se
    desbalancea tanto — el problema es específico de datos ya ordenados,
    no del ABB en sí mismo.
    """
    import random
    random.seed(semilla)
 
    titulos = generar_titulos_ordenados(n)
    random.shuffle(titulos)
 
    bst = ArbolPorTitulo()
    avl = ArbolAVLPorTitulo()
 
    for i, titulo in enumerate(titulos):
        cancion = Cancion(i, titulo, "Artista Sintetico")
        bst.insertar_cancion(cancion)
        avl.insertar_cancion(cancion)
 
    altura_bst = calcular_altura_bst(bst.raiz)
    altura_avl = avl.altura()
    altura_ideal = math.floor(math.log2(n)) + 1 if n > 0 else 0
 
    return {
        "n": n,
        "altura_bst": altura_bst,
        "altura_avl": altura_avl,
        "altura_ideal_log2n": altura_ideal,
    }
 
 
def main():
    tamanos = [10, 100, 1_000, 10_000]
 
    print("=" * 78)
    print("CASO 1 — PEOR ESCENARIO: títulos insertados YA ORDENADOS alfabéticamente")
    print("=" * 78)
    print(f"{'N':>8} | {'Altura BST común':>18} | {'Altura AVL':>12} | {'Altura ideal log2(N)':>22}")
    print("-" * 78)
 
    for n in tamanos:
        r = caso_peor_escenario(n)
        altura_bst_str = "CRASH (RecursionError)" if r["bst_crasheo"] else str(r["altura_bst"])
        print(
            f"{r['n']:>8} | {altura_bst_str:>18} | {r['altura_avl']:>12} "
            f"| {r['altura_ideal_log2n']:>22}"
        )
        assert r["avl_balanceado"], f"El AVL no quedó balanceado para N={n}"
 
    print("\n✔ El AVL se mantuvo balanceado (altura ≈ log2(N)) en todos los tamaños.")
    print("  El BST común, en cambio, degenera tanto con datos ya ordenados que para N")
    print("  grande directamente CRASHEA con RecursionError — no es solo más lento,")
    print("  se vuelve inutilizable. Esto es en sí mismo la demostración más contundente")
    print("  de por qué hace falta un árbol auto-balanceado como el AVL.")
 
    print("\n" + "=" * 78)
    print("CASO 2 — CONTRAEJEMPLO: títulos insertados en orden ALEATORIO")
    print("=" * 78)
    print(f"{'N':>8} | {'Altura BST común':>18} | {'Altura AVL':>12} | {'Altura ideal log2(N)':>22}")
    print("-" * 78)
 
    for n in tamanos:
        r = caso_orden_aleatorio(n)
        print(
            f"{r['n']:>8} | {r['altura_bst']:>18} | {r['altura_avl']:>12} "
            f"| {r['altura_ideal_log2n']:>22}"
        )
 
    print("\n✔ Con orden aleatorio, el BST común queda razonablemente cerca del ideal")
    print("  logarítmico — el problema de desbalance es específico de datos ya ordenados,")
    print("  no una falla general del ABB.")
 
 
if __name__ == "__main__":
    main()
 