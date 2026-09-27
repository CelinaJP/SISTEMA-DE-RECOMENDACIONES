"""
Compara BST común (TP3) vs. AVL (TP4) en dos escenarios: dataset "peor
caso" (títulos insertados ya ordenados alfabéticamente) y dataset
"normal" (orden aleatorio, más parecido a cómo llegan las canciones
reales). Para cada uno mide: altura del árbol, cantidad de comparaciones
para buscar, y tiempo real de búsqueda.

Relacionado con: TP4 - AVL / Issue 2 (Comparación BST vs. AVL).

Uso:
    python benchmarks/comparacion_bst_avl.py
"""

import csv
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelos.cancion import Cancion
from estructuras.arbol_binario import ArbolPorTitulo, _normalizar
from estructuras.arbol_avl import ArbolAVLPorTitulo


def generar_titulos_ordenados(n: int):
    """Títulos con padding de ceros para que el orden alfabético de los
    strings coincida con el orden numérico — así se insertan en el peor
    orden posible para un ABB común.
    """
    ancho = len(str(n))
    return [f"Cancion {str(i).zfill(ancho)}" for i in range(n)]


def generar_titulos_aleatorios(n: int, semilla: int = 42):
    titulos = generar_titulos_ordenados(n)
    random.seed(semilla)
    random.shuffle(titulos)
    return titulos


def calcular_altura_bst(nodo) -> int:
    """El ABB común (TP3) no tiene método `altura()` propio; se calcula
    desde afuera recorriendo los punteros izquierda/derecha (públicos).
    """
    if nodo is None:
        return 0
    return 1 + max(calcular_altura_bst(nodo.izquierda), calcular_altura_bst(nodo.derecha))


def buscar_con_conteo(raiz, clave: str) -> int:
    """Búsqueda manual que cuenta cuántas comparaciones hace hasta
    encontrar la clave (o llegar a None). Funciona sobre CUALQUIER árbol
    cuyos nodos tengan .clave, .izquierda y .derecha públicos — por eso
    sirve tanto para el BST común como para el AVL, sin duplicar lógica.
    """
    clave_normalizada = _normalizar(clave)
    comparaciones = 0
    actual = raiz

    while actual is not None:
        comparaciones += 1
        clave_actual_normalizada = _normalizar(actual.clave)
        if clave_normalizada == clave_actual_normalizada:
            return comparaciones
        elif clave_normalizada < clave_actual_normalizada:
            actual = actual.izquierda
        else:
            actual = actual.derecha

    return comparaciones  # no encontrada; cuenta igual los pasos dados


def medir_tiempo_busqueda_ms(func, *args, iteraciones: int = 200) -> float:
    inicio = time.perf_counter()
    for _ in range(iteraciones):
        func(*args)
    return (time.perf_counter() - inicio) / iteraciones * 1000


def construir_arboles(titulos):
    """Construye el BST común y el AVL con el mismo dataset. Si el BST
    revienta por RecursionError (degenerado + N grande), se captura y se
    reporta como hallazgo en vez de tirar abajo todo el benchmark.
    """
    bst = ArbolPorTitulo()
    avl = ArbolAVLPorTitulo()
    bst_crasheo = False

    for i, titulo in enumerate(titulos):
        cancion = Cancion(i, titulo, "Artista Sintetico")
        if not bst_crasheo:
            try:
                bst.insertar_cancion(cancion)
            except RecursionError:
                bst_crasheo = True
        avl.insertar_cancion(cancion)

    return bst, avl, bst_crasheo


def ejecutar_caso(nombre_caso: str, generador_titulos, tamanos):
    filas = []
    print(f"\n{'=' * 92}")
    print(nombre_caso)
    print("=" * 92)
    print(
        f"{'N':>8} | {'Alt.BST':>8} | {'Alt.AVL':>8} | {'Ideal log2N':>12} "
        f"| {'Comp.BST':>9} | {'Comp.AVL':>9} | {'T.BST(ms)':>10} | {'T.AVL(ms)':>10}"
    )
    print("-" * 92)

    for n in tamanos:
        titulos = generador_titulos(n)
        bst, avl, bst_crasheo = construir_arboles(titulos)

        # Búsqueda del último título insertado: en el caso ordenado, es
        # el peor caso posible para el BST degenerado (queda en la hoja
        # más profunda de la cadena).
        objetivo = titulos[-1]
        altura_ideal = math.floor(math.log2(n)) + 1 if n > 0 else 0

        if bst_crasheo:
            altura_bst_str = "CRASH"
            comp_bst_str = "N/A"
            t_bst_str = "N/A"
        else:
            altura_bst = calcular_altura_bst(bst.raiz)
            comp_bst = buscar_con_conteo(bst.raiz, objetivo)
            t_bst = medir_tiempo_busqueda_ms(bst.buscar_por_titulo, objetivo)
            altura_bst_str, comp_bst_str, t_bst_str = str(altura_bst), str(comp_bst), f"{t_bst:.5f}"

        altura_avl = avl.altura()
        comp_avl = buscar_con_conteo(avl.raiz, objetivo)
        t_avl = medir_tiempo_busqueda_ms(avl.buscar_por_titulo, objetivo)

        print(
            f"{n:>8} | {altura_bst_str:>8} | {altura_avl:>8} | {altura_ideal:>12} "
            f"| {comp_bst_str:>9} | {comp_avl:>9} | {t_bst_str:>10} | {t_avl:>10.5f}"
        )

        filas.append({
            "caso": nombre_caso,
            "N": n,
            "altura_bst": altura_bst_str,
            "altura_avl": altura_avl,
            "altura_ideal_log2n": altura_ideal,
            "comparaciones_bst": comp_bst_str,
            "comparaciones_avl": comp_avl,
            "tiempo_bst_ms": t_bst_str,
            "tiempo_avl_ms": f"{t_avl:.5f}",
            "avl_balanceado": avl.esta_balanceado(),
        })

    return filas


def main():
    tamanos = [10, 100, 1_000, 10_000]

    filas_ordenado = ejecutar_caso(
        "CASO 1 — PEOR CASO: títulos insertados YA ORDENADOS alfabéticamente",
        generar_titulos_ordenados,
        tamanos,
    )
    filas_aleatorio = ejecutar_caso(
        "CASO 2 — CASO NORMAL: títulos insertados en orden ALEATORIO",
        generar_titulos_aleatorios,
        tamanos,
    )

    todas_las_filas = filas_ordenado + filas_aleatorio
    for fila in todas_las_filas:
        assert fila["avl_balanceado"], f"El AVL no quedó balanceado: {fila}"

    print("\n✔ El AVL se mantuvo balanceado en los 8 escenarios probados (2 casos × 4 tamaños).")
    print("  En el caso ordenado, la diferencia con el BST común es dramática (llega a crashear).")
    print("  En el caso aleatorio, la diferencia es mucho menor — confirma que el problema")
    print("  de desbalance es específico de datos ya ordenados, no una falla general del BST.")

    ruta_csv = os.path.join(os.path.dirname(__file__), "resultados_bst_vs_avl.csv")
    columnas = list(todas_las_filas[0].keys())
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        for fila in todas_las_filas:
            writer.writerow(fila)

    print(f"\nResultados exportados a: {ruta_csv}")


if __name__ == "__main__":
    main()