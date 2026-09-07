import json
import os
from typing import List, Optional
from modelos.cancion import Cancion


class Catalogo:
    """Lógica de negocio: carga y operaciones sobre el catálogo de Miranda!."""
    
    def __init__(self) -> None:
        self._elementos: List[Cancion] = []

    def cargar_desde_json(self, ruta_archivo: str = "datos/miranda_canciones.json") -> None:
        """Carga las canciones desde el archivo JSON al catálogo interno."""
        if not os.path.exists(ruta_archivo):
            ruta_archivo = os.path.join(os.path.dirname(__file__), "..", "datos", "miranda_canciones.json")
            
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                for item in datos:
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
                    self._elementos.append(cancion)
        except Exception as e:
            print(f"[Error al cargar catálogo]: {e}")

    def _obtener_atributo(self, cancion: Cancion, nombre_attr: str):
        """Auxiliar seguro para obtener un atributo."""
        if hasattr(cancion, nombre_attr):
            return getattr(cancion, nombre_attr)
        elif hasattr(cancion, f"_{nombre_attr}"):
            return getattr(cancion, f"_{nombre_attr}")
        return None

    def listar(self) -> List[Cancion]:
        """Retorna la lista de todos los elementos."""
        return list(self._elementos)

    def buscar(self, criterio: str) -> List[Cancion]:
        """Búsqueda por texto, sin distinguir mayúsculas."""
        criterio_norm = criterio.strip().lower()
        if not criterio_norm:
            return []

        resultados: List[Cancion] = []
        for cancion in self._elementos:
            titulo = str(self._obtener_atributo(cancion, "titulo") or "")
            artista = str(self._obtener_atributo(cancion, "artista_principal") or "")
            colabs = self._obtener_atributo(cancion, "colaboradores") or []

            match_titulo = criterio_norm in titulo.lower()
            match_artista = criterio_norm in artista.lower()
            match_colab = False
            
            if isinstance(colabs, list):
                match_colab = any(criterio_norm in str(c).lower() for c in colabs)
            elif isinstance(colabs, str):
                match_colab = criterio_norm in colabs.lower()

            if match_titulo or match_artista or match_colab:
                resultados.append(cancion)
                
        return resultados

    def filtrar(self, era: Optional[str] = None, genero: Optional[str] = None) -> List[Cancion]:
        """Filtra la lista por era o género."""
        resultados = self._elementos

        if era:
            resultados = [
                c for c in resultados 
                if str(self._obtener_atributo(c, "era") or "").strip().lower() == era.strip().lower()
            ]
            
        if genero:
            resultados = [
                c for c in resultados 
                if str(self._obtener_atributo(c, "genero") or "").strip().lower() == genero.strip().lower()
            ]

        return resultados
        
    def __len__(self) -> int:
        return len(self._elementos)