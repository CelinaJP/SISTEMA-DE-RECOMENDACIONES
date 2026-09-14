"""
Script de comparación de rendimiento: Búsqueda Secuencial vs Árbol Binario
de Búsqueda (ABB), aplicado a la búsqueda de canciones por título.

Genera datasets sintéticos de N = 1.000, 10.000 y 100.000 canciones con
títulos únicos, y mide el tiempo promedio de búsqueda para:

- Búsqueda Secuencial: recorrido lineal de una lista de `Cancion`,
  comparando título por título (equivalente a lo que hacía `Catalogo`
  antes de incorporar el ABB).
- Búsqueda en Árbol Binario: `ArbolPorTitulo.buscar_por_titulo(...)`.

Se mide tanto el caso "título existente" (búsqueda exitosa) como el caso
"título inexistente" (peor caso: hay que recorrer todo el árbol/lista).

Relacionado con: TP3 - Árbol Binario / Issue 5 (Script de comparación de
rendimiento). Los resultados de este script son los que respaldan la
tabla de tiempos de `TP2_analisis_complejidad.md`.

Uso:
    python benchmarks/comparacion_busqueda.py
"""

import csv
import os
import random
import string
import time
from typing import List, Tuple

from modelos.cancion import Cancion
from estructuras.arbol_binario import ArbolPorTitulo


def generar_dataset(n: int, semilla: int = 42) -> List[Cancion]:
    """Genera N canciones sintéticas con títulos únicos y reproducibles
    (misma semilla = mismo dataset, para que el benchmark sea repetible).
    """
    random.seed(semilla)
    canciones: List[Cancion] = []
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


def busqueda_secuencial(canciones: List[Cancion], titulo_buscado: str) -> List[Cancion]:
    """Búsqueda secuencial equivalente a la de TP2: recorre la lista
    completa comparando título por título.
    """
    return [c for c in canciones if c.titulo == titulo_buscado]


def medir_tiempo_promedio_ms(func, *args, repeticiones: int = 200) -> float:
    """Ejecuta `func(*args)` `repeticiones` veces y devuelve el tiempo
    promedio por ejecución, en milisegundos.
    """
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        func(*args)
    fin = time.perf_counter()
    return (fin - inicio) / repeticiones * 1000


def ejecutar_benchmark(n: int, repeticiones: int = 200) -> Tuple[float, float, float, float]:
    """Corre el benchmark para un tamaño de dataset `n`.

    Devuelve una tupla:
        (secuencial_encontrado_ms, abb_encontrado_ms,
         secuencial_no_encontrado_ms, abb_no_encontrado_ms)
    """
    canciones = generar_dataset(n)

    arbol = ArbolPorTitulo()
    for cancion in canciones:
        arbol.insertar_cancion(cancion)

    # Título existente: el del medio de la lista (caso promedio realista,
    # ni mejor caso -primero/raíz- ni artificialmente favorable).
    titulo_existente = canciones[n // 2].titulo
    titulo_inexistente = "Titulo Que Nunca Fue Insertado XYZ"

    sec_encontrado = medir_tiempo_promedio_ms(
        busqueda_secuencial, canciones, titulo_existente, repeticiones=repeticiones
    )
    abb_encontrado = medir_tiempo_promedio_ms(
        arbol.buscar_por_titulo, titulo_existente, repeticiones=repeticiones
    )
    sec_no_encontrado = medir_tiempo_promedio_ms(
        busqueda_secuencial, canciones, titulo_inexistente, repeticiones=repeticiones
    )
    abb_no_encontrado = medir_tiempo_promedio_ms(
        arbol.buscar_por_titulo, titulo_inexistente, repeticiones=repeticiones
    )

    return sec_encontrado, abb_encontrado, sec_no_encontrado, abb_no_encontrado


def exportar_csv(resultados: List[Tuple[int, float, float, float, float]], ruta: str) -> None:
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([
            "N",
            "secuencial_encontrado_ms",
            "abb_encontrado_ms",
            "secuencial_no_encontrado_ms",
            "abb_no_encontrado_ms",
        ])
        for fila in resultados:
            writer.writerow(fila)


def main():
    tamanos = [1_000, 10_000, 100_000]
    resultados = []

    print(f"{'N':>10} | {'Secuencial (ms)':>16} | {'ABB (ms)':>10} | {'Secuencial no enc. (ms)':>24} | {'ABB no enc. (ms)':>16}")
    print("-" * 88)

    for n in tamanos:
        sec_ok, abb_ok, sec_no, abb_no = ejecutar_benchmark(n)
        resultados.append((n, sec_ok, abb_ok, sec_no, abb_no))
        print(f"{n:>10} | {sec_ok:>16.4f} | {abb_ok:>10.4f} | {sec_no:>24.4f} | {abb_no:>16.4f}")

    ruta_csv = os.path.join(os.path.dirname(__file__), "resultados_comparacion.csv")
    exportar_csv(resultados, ruta_csv)
    print(f"\nResultados exportados a: {ruta_csv}")


if __name__ == "__main__":
    main()