import json
import os
from typing import List, Dict, Tuple
from modelos.cancion import Cancion

def cargar_catalogo(ruta_archivo: str = "datos/miranda_canciones.json") -> Tuple[List[Cancion], Dict[int, Cancion]]:
    """
    Lee un archivo JSON, mapea los datos parseados a instancias de la clase Cancion
    y maneja excepciones básicas para archivos no encontrados o corruptos.
    
    Retorna una tupla con (lista_de_canciones, diccionario_por_id).
    """
    canciones_lista: List[Cancion] = []
    canciones_dict: Dict[int, Cancion] = {}

    # Ajuste dinámico de ruta por si se ejecuta desde subcarpetas
    if not os.path.exists(ruta_archivo):
        ruta_archivo = os.path.join(os.path.dirname(__file__), "..", "datos", "miranda_canciones.json")

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            
            for item in datos:
                # Mapeo exacto con la clase Cancion de tu modelos/cancion.py
                cancion = Cancion(
                    id_cancion=item["id"],
                    titulo=item["titulo"],
                    artista_principal=item["artista_principal"],
                    colaboradores=item.get("colaboradores", []),
                    anio=item.get("anio", 0),
                    era=item.get("era", "Clásica"),
                    duracion_segundos=item.get("duracion_segundos", 0),
                    genero=item.get("genero", "Pop"),
                    mood=item.get("mood", ""),
                    popularidad=item.get("popularidad", 0),
                    clasica_version_id=item.get("clasica_version_id"),
                    moderna_version_id=item.get("moderna_version_id")
                )
                canciones_lista.append(cancion)
                canciones_dict[cancion.id] = cancion

    except FileNotFoundError:
        print(f"[Error de Carga]: No se encontró el archivo de datos en '{ruta_archivo}'.")
    except json.JSONDecodeError:
        print(f"[Error de Carga]: El archivo '{ruta_archivo}' está corrupto o no tiene un formato JSON válido.")
    except Exception as e:
        print(f"[Error Inesperado]: Ocurrió un error al procesar el catálogo: {e}")

    return canciones_lista, canciones_dict