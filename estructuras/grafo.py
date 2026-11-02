# estructuras/grafo.py

from collections import deque
import heapq

class GrafoColaboraciones:
    """
    Grafo No Dirigido y Pesado implementado con Lista de Adyacencia.
    - Vértices: Artistas (Miranda! y sus colaboradores).
    - Aristas: Colaboración en una misma canción.
    - Peso (Costo): "Distancia de afinidad" calculada como (100 - popularidad).
    """
    def __init__(self):
        # Lista de adyacencia: {artista: {colaborador: {'canciones': [], 'peso': float}}}
        self.adyacencia = {}

    def agregar_vertice(self, artista: str):
        if artista not in self.adyacencia:
            self.adyacencia[artista] = {}

    def agregar_arista(self, artista1: str, artista2: str, cancion: str, peso: float):
        self.agregar_vertice(artista1)
        self.agregar_vertice(artista2)
        
        # Como es un grafo NO DIRIGIDO, la relación va en ambos sentidos
        for origen, destino in [(artista1, artista2), (artista2, artista1)]:
            if destino not in self.adyacencia[origen]:
                self.adyacencia[origen][destino] = {'canciones': [], 'peso': float('inf')}
            
            if cancion not in self.adyacencia[origen][destino]['canciones']:
                self.adyacencia[origen][destino]['canciones'].append(cancion)
            
            # Si hay múltiples colaboraciones, nos quedamos con la conexión más fuerte (menor costo)
            if peso < self.adyacencia[origen][destino]['peso']:
                self.adyacencia[origen][destino]['peso'] = peso

    def cargar_desde_catalogo(self, catalogo):
        """Construye la red de colaboraciones iterando sobre el catálogo."""
        canciones = catalogo.listar() if hasattr(catalogo, "listar") else []
        for c in canciones:
            # Búsqueda segura de atributos (públicos o privados)
            artista_principal = getattr(c, "artista_principal", getattr(c, "_artista_principal", "Miranda!"))
            colaboradores = getattr(c, "colaboradores", getattr(c, "_colaboradores", []))
            titulo = getattr(c, "titulo", getattr(c, "_titulo", "Desconocida"))
            
            # Calculamos el costo: a mayor popularidad, menor "distancia" (costo)
            popularidad = getattr(c, "popularidad", getattr(c, "_popularidad", 50))
            peso = max(1.0, 100.0 - float(popularidad))
            
            self.agregar_vertice(artista_principal)
            
            # Conectar al artista principal con cada colaborador
            for colab in colaboradores:
                self.agregar_arista(artista_principal, colab, titulo, peso)
            
            # Conectar a los colaboradores entre sí
            for i in range(len(colaboradores)):
                for j in range(i + 1, len(colaboradores)):
                    self.agregar_arista(colaboradores[i], colaboradores[j], titulo, peso)

    def obtener_conexiones_directas(self, artista: str):
        """Devuelve un diccionario con los colaboradores directos y las canciones compartidas."""
        artista_key = self._encontrar_key_case_insensitive(artista)
        if not artista_key:
            return {}
        
        # Formateamos la salida para mantener compatibilidad con la UI existente
        res = {}
        for colab, data in self.adyacencia.get(artista_key, {}).items():
            res[colab] = data['canciones']
        return res

    def buscar_conexiones_indirectas(self, artista: str, grados: int = 2):
        """Algoritmo BFS (Búsqueda en Amplitud) para grados de separación."""
        artista_key = self._encontrar_key_case_insensitive(artista)
        if not artista_key:
            return {}

        visitados = {artista_key}
        cola = deque([(artista_key, 0, [artista_key])])
        resultados = {}

        while cola:
            actual, grado, camino = cola.popleft()
            
            if 0 < grado <= grados:
                resultados[actual] = (grado, camino)
                
            if grado < grados:
                for vecino in self.adyacencia.get(actual, {}).keys():
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.append((vecino, grado + 1, camino + [vecino]))
                        
        return resultados

    def explorar_ecosistema_dfs(self, artista: str):
        """Algoritmo DFS (Búsqueda en Profundidad) iterativo."""
        artista_key = self._encontrar_key_case_insensitive(artista)
        if not artista_key:
            return []

        visitados = set()
        pila = [(artista_key, [artista_key])]
        caminos_profundos = []

        while pila:
            actual, camino = pila.pop()
            
            if actual not in visitados:
                visitados.add(actual)
                
                vecinos_no_visitados = [v for v in self.adyacencia.get(actual, {}).keys() if v not in visitados]
                
                if not vecinos_no_visitados and len(camino) > 1:
                    caminos_profundos.append(camino)
                
                for vecino in sorted(vecinos_no_visitados, reverse=True):
                    pila.append((vecino, camino + [vecino]))
                    
        return caminos_profundos

    def camino_mas_fuerte_dijkstra(self, origen: str, destino: str):
        """
        Algoritmo de Dijkstra para encontrar el camino de colaboración más fuerte (menor costo).
        Retorna: (lista_del_camino, costo_total)
        """
        origen_key = self._encontrar_key_case_insensitive(origen)
        destino_key = self._encontrar_key_case_insensitive(destino)
        
        if not origen_key or not destino_key:
            return None, float('inf')

        distancias = {nodo: float('inf') for nodo in self.adyacencia}
        distancias[origen_key] = 0
        padres = {nodo: None for nodo in self.adyacencia}
        
        # Cola de prioridad: (distancia_acumulada, nodo_actual)
        pq = [(0, origen_key)]
        
        while pq:
            dist_actual, actual = heapq.heappop(pq)
            
            # Si encontramos un camino peor al ya registrado, lo ignoramos
            if dist_actual > distancias[actual]:
                continue
                
            # Si llegamos al destino, podemos detenernos (Dijkstra garantiza que es el mínimo)
            if actual == destino_key:
                break
                
            for vecino, data in self.adyacencia.get(actual, {}).items():
                peso_arista = data['peso']
                nueva_dist = dist_actual + peso_arista
                
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    padres[vecino] = actual
                    heapq.heappush(pq, (nueva_dist, vecino))
                    
        if distancias[destino_key] == float('inf'):
            return None, float('inf')
            
        # Reconstruir el camino desde el destino hacia el origen
        camino = []
        actual = destino_key
        while actual is not None:
            camino.append(actual)
            actual = padres[actual]
        camino.reverse()
        
        return camino, distancias[destino_key]

    def _encontrar_key_case_insensitive(self, artista: str):
        target = artista.strip().lower()
        for key in self.adyacencia.keys():
            if key.lower() == target:
                return key
        return None
    