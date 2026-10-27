# estructuras/grafo.py

from collections import deque

class GrafoColaboraciones:
    """
    Grafo No Dirigido y No Pesado implementado con Lista de Adyacencia.
    - Vértices: Artistas (Miranda! y sus colaboradores).
    - Aristas: Colaboración en una misma canción.
    """
    def __init__(self):
        # Lista de adyacencia: {artista: {colaborador: [canciones]}}
        self.adyacencia = {}

    def agregar_vertice(self, artista: str):
        if artista not in self.adyacencia:
            self.adyacencia[artista] = {}

    def agregar_arista(self, artista1: str, artista2: str, cancion: str):
        self.agregar_vertice(artista1)
        self.agregar_vertice(artista2)
        
        # Como es un grafo NO DIRIGIDO, la relación va en ambos sentidos
        if artista2 not in self.adyacencia[artista1]:
            self.adyacencia[artista1][artista2] = []
        if cancion not in self.adyacencia[artista1][artista2]:
            self.adyacencia[artista1][artista2].append(cancion)
            
        if artista1 not in self.adyacencia[artista2]:
            self.adyacencia[artista2][artista1] = []
        if cancion not in self.adyacencia[artista2][artista1]:
            self.adyacencia[artista2][artista1].append(cancion)

    def cargar_desde_catalogo(self, catalogo):
        """Construye la red de colaboraciones iterando sobre el catálogo."""
        canciones = catalogo.listar() if hasattr(catalogo, "listar") else []
        for c in canciones:
            artista_principal = getattr(c, "artista_principal", "Miranda!")
            colaboradores = getattr(c, "colaboradores", [])
            titulo = getattr(c, "titulo", "Desconocida")
            
            self.agregar_vertice(artista_principal)
            
            # Conectar al artista principal con cada colaborador
            for colab in colaboradores:
                self.agregar_arista(artista_principal, colab, titulo)
            
            # Conectar a los colaboradores entre sí (si hay más de 1 en el mismo tema, ej: María Becerra y FMK)
            for i in range(len(colaboradores)):
                for j in range(i + 1, len(colaboradores)):
                    self.agregar_arista(colaboradores[i], colaboradores[j], titulo)

    def obtener_conexiones_directas(self, artista: str):
        """Devuelve un diccionario con los colaboradores directos y las canciones compartidas."""
        artista_key = self._encontrar_key_case_insensitive(artista)
        if not artista_key:
            return {}
        return self.adyacencia.get(artista_key, {})

    def buscar_conexiones_indirectas(self, artista: str, grados: int = 2):
        """
        Algoritmo BFS (Búsqueda en Amplitud) para encontrar conexiones indirectas
        (grados de separación) en la red musical.
        Retorna: {artista_conectado: (grado, camino_recorrido)}
        """
        artista_key = self._encontrar_key_case_insensitive(artista)
        if not artista_key:
            return {}

        visitados = {artista_key}
        # La cola guarda tuplas: (nodo_actual, grado_actual, camino_hasta_aqui)
        cola = deque([(artista_key, 0, [artista_key])])
        resultados = {}

        while cola:
            actual, grado, camino = cola.popleft()
            
            if 0 < grado <= grados:
                resultados[actual] = (grado, camino)
                
            if grado < grados:
                for vecino in self.adyacencia.get(actual, {}):
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.append((vecino, grado + 1, camino + [vecino]))
                        
        return resultados

    def _encontrar_key_case_insensitive(self, artista: str):
        """Permite buscar 'lali' y encontrar 'Lali'."""
        target = artista.strip().lower()
        for key in self.adyacencia.keys():
            if key.lower() == target:
                return key
        return None