"""
Definición de la función de prioridad para el ranking (TP6 / Versión 4).
"""

def obtener_prioridad(cancion) -> float:
    """
    Función de prioridad basada en la popularidad o rating de la canción.
    Si el atributo no existe, retorna 0.0 por defecto.
    """
    # Intentamos obtener 'popularidad' o 'rating' de forma segura
    for atributo in ["popularidad", "rating", "anio"]:
        val = getattr(cancion, atributo, None)
        if val is not None:
            try:
                return float(val)
            except (ValueError, TypeError):
                continue
    
    # Si es un diccionario (por compatibilidad)
    if isinstance(cancion, dict):
        for atributo in ["popularidad", "rating", "anio"]:
            if atributo in cancion:
                try:
                    return float(cancion[atributo])
                except (ValueError, TypeError):
                    continue
                    
    return 0.0