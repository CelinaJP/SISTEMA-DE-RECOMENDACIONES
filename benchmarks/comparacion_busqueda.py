import sys
import os
import time
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from estructuras.arbol_binario import ArbolPorTitulo
from servicios.gestor_catalogo import Catalogo

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

def ejecutar_benchmark():
    catalogo = Catalogo()
    catalogo.cargar_desde_json("datos/miranda_canciones.json")
    canciones = catalogo.listar() if hasattr(catalogo, "listar") else catalogo.canciones
    
    canciones_ordenadas = sorted(canciones, key=lambda c: getattr(c, "titulo", "").lower())
    
    arbol = ArbolPorTitulo()
    arbol.cargar_desde_catalogo(catalogo)

    target = "Don"
    iteraciones = 10000

    # 1. Secuencial
    t0 = time.perf_counter()
    for _ in range(iteraciones):
        busqueda_secuencial(canciones, target)
    t_secuencial = (time.perf_counter() - t0) / iteraciones

    # 2. Binaria
    t0 = time.perf_counter()
    for _ in range(iteraciones):
        busqueda_binaria(canciones_ordenadas, target)
    t_binaria = (time.perf_counter() - t0) / iteraciones

    # 3. Árbol BST
    t0 = time.perf_counter()
    for _ in range(iteraciones):
        arbol.buscar_por_titulo(target)
    t_arbol = (time.perf_counter() - t0) / iteraciones

    # Guardar en CSV
    os.makedirs("benchmarks", exist_ok=True)
    csv_path = "benchmarks/resultados_comparacion.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Estrategia", "Tiempo_Promedio_Segundos", "Complejidad_Teorica"])
        writer.writerow(["Secuencial", f"{t_secuencial:.8f}", "O(n)"])
        writer.writerow(["Binaria", f"{t_binaria:.8f}", "O(log n)"])
        writer.writerow(["Arbol_BST", f"{t_arbol:.8f}", "O(log n)"])

    print("--- RESULTADOS BENCHMARK ---")
    print(f"Secuencial: {t_secuencial:.8f} s (O(n))")
    print(f"Binaria:    {t_binaria:.8f} s (O(log n))")
    print(f"Árbol BST:  {t_arbol:.8f} s (O(log n))")
    print(f"\nResultados guardados exitosamente en {csv_path}")

if __name__ == "__main__":
    ejecutar_benchmark()