import sys
import os
import time
import csv
import random
import string

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from estructuras.arbol_binario import ArbolPorTitulo
from servicios.gestor_catalogo import Catalogo
from modelos.cancion import Cancion

def busqueda_secuencial(lista, titulo):
    for c in lista:
        if getattr(c, "titulo", "").lower() == titulo.lower():
            return c
    return None

def busqueda_binaria(lista_ordenada, titulo):
    inicio = 0
    fin = len(lista_ordenada) - 1
    target = titulo.lower()
    while inicio <= fin:
        medio = (inicio + fin) // 2
        actual = getattr(lista_ordenada[medio], "titulo", "").lower()
        if actual == target:
            return lista_ordenada[medio]
        elif actual < target:
            inicio = medio + 1
        else:
            fin = medio - 1
    return None

def generar_dataset_sintetico(n, semilla=42):
    random.seed(semilla)
    canciones = []
    titulos_usados = set()

    for i in range(n):
        while True:
            sufijo = "".join(random.choices(string.ascii_lowercase, k=6))
            titulo = f"Cancion Sintetica {i}-{sufijo}"
            if titulo not in titulos_usados:
                titulos_usados.add(titulo)
                break
        canciones.append(Cancion(i, titulo, "Artista Sintetico"))

    return canciones

def ejecutar_benchmark():
    tamanos = [1_000, 10_000, 100_000]
    resultados = []

    print("--- RESULTADOS BENCHMARK (secuencial vs. binaria vs. árbol BST) ---\n")

    for n in tamanos:
        canciones = generar_dataset_sintetico(n)
        canciones_ordenadas = sorted(canciones, key=lambda c: getattr(c, "titulo", "").lower())

        arbol = ArbolPorTitulo()
        for c in canciones:
            arbol.insertar_cancion(c)

        target = canciones[n // 2].titulo
        iteraciones = 200

        t0 = time.perf_counter()
        for _ in range(iteraciones):
            busqueda_secuencial(canciones, target)
        t_secuencial = (time.perf_counter() - t0) / iteraciones

        t0 = time.perf_counter()
        for _ in range(iteraciones):
            busqueda_binaria(canciones_ordenadas, target)
        t_binaria = (time.perf_counter() - t0) / iteraciones

        t0 = time.perf_counter()
        for _ in range(iteraciones):
            arbol.buscar_por_titulo(target)
        t_arbol = (time.perf_counter() - t0) / iteraciones

        resultados.append((n, t_secuencial, t_binaria, t_arbol))
        print(f"N={n:>7} | Secuencial: {t_secuencial:.8f}s | Binaria: {t_binaria:.8f}s | Árbol BST: {t_arbol:.8f}s")

    os.makedirs("benchmarks", exist_ok=True)
    csv_path = "benchmarks/resultados_comparacion.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "Secuencial_Segundos", "Binaria_Segundos", "Arbol_BST_Segundos",
                          "Complejidad_Secuencial", "Complejidad_Binaria", "Complejidad_Arbol_BST"])
        for n, t_sec, t_bin, t_arb in resultados:
            writer.writerow([n, f"{t_sec:.8f}", f"{t_bin:.8f}", f"{t_arb:.8f}", "O(n)", "O(log n)", "O(log n)"])

    print(f"\nResultados guardados exitosamente en {csv_path}")

if __name__ == "__main__":
    ejecutar_benchmark()