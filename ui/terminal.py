
import os
from servicios.gestor_catalogo import Catalogo as CatalogoDeCancion
from estructuras.arbol_binario import ArbolPorTitulo, ArbolPorArtista
 
 
class MenuInicio:
    def __init__(
        self,
        catalogo: CatalogoDeCancion,
        arbol_titulos: ArbolPorTitulo = None,
        arbol_artistas: ArbolPorArtista = None,
    ):
        self.catalogo = catalogo
        
        self.arbol_titulos = arbol_titulos
        self.arbol_artistas = arbol_artistas
 
    def limpiar_pantalla(self):
        os.system("cls" if os.name == "nt" else "clear")
 
    def mostrar_menu_principal(self):
        print("\n" + "=" * 60)
        print("    EL BOT DE TU CORAZÓN — MIRANDA! (Recomendador Pop)")
        print("=" * 60)
        print(" 1. Top 10 / Listar canciones")
        print(" 2. Buscar canción (por título o artista)")
        print(" 3. Filtrar por género / era / mood")
        print(" 4. Generar Playlist por Tiempo")
        print(" 5. Explorar Colaborador")
        print(" 6. Comparar Versiones")
        print(" 7. Puente Temporal")
        print(" 8. Obtener Versión Clásica")
        print(" 0. Salir")
        print("=" * 60)
 
    def _formatear_cancion(self, cancion):
        titulo = getattr(cancion, "titulo", "Sin título")
        artista = getattr(cancion, "artista_principal", getattr(cancion, "artista", "Miranda!"))
        colabs = getattr(cancion, "colaboradores", [])
        colabs_str = f" (feat. {', '.join(colabs)})" if colabs else ""
        era = getattr(cancion, "era", getattr(cancion, "anio", "N/A"))
        mood = getattr(cancion, "mood", getattr(cancion, "genero", "N/A"))
        cid = getattr(cancion, "id", getattr(cancion, "id_cancion", "?"))
 
        return f"🎵 [{cid}] {titulo} - {artista}{colabs_str} | Era/Año: {era} | Mood/Género: {mood}"
 
    def procesar_opcion(self, opcion: str) -> bool:
        # 1. LISTAR / TOP 10
        if opcion == "1":
            self.limpiar_pantalla()
            print("--- TOP 10 CANCIONES MÁS POPULARES ---\n")
            
            todas = []
            if hasattr(self.catalogo, "listar"):
                todas = self.catalogo.listar()
            elif hasattr(self.catalogo, "canciones"):
                todas = self.catalogo.canciones
 
            if todas:
                top_10 = sorted(
                    todas, 
                    key=lambda c: getattr(c, "popularidad", c.get("popularidad", 0) if isinstance(c, dict) else 0), 
                    reverse=True
                )[:10]
 
                for i, c in enumerate(top_10, 1):
                    pop = getattr(c, "popularidad", c.get("popularidad", "N/A") if isinstance(c, dict) else "N/A")
                    print(f"{i}. {self._formatear_cancion(c)} | Popularidad: {pop}")
            else:
                print("No hay canciones registradas en el catálogo.")
 
        # 2. BUSCAR CANCIÓN (Issue 4: ahora usa el ABB por título y por artista)
        elif opcion == "2":
            self.limpiar_pantalla()
            print("--- BUSCAR CANCIÓN (título o artista) ---")
            criterio = input("Ingrese el título o artista exacto a buscar: ").strip()
 
            if not criterio:
                print("Búsqueda cancelada: el texto no puede estar vacío.")
                input("\nPresione ENTER para continuar...")
                return True
 
            resultados = []
 
            if self.arbol_titulos is not None and self.arbol_artistas is not None:
                por_titulo = self.arbol_titulos.buscar_por_titulo(criterio)
                por_artista = self.arbol_artistas.buscar_por_artista(criterio)
 
                # Unificar resultados sin duplicar (una canción puede
                # aparecer en ambos árboles, ej. si el título coincide con
                # un nombre de artista).
                ids_vistos = set()
                for c in por_titulo + por_artista:
                    cid = getattr(c, "id", None)
                    if cid not in ids_vistos:
                        ids_vistos.add(cid)
                        resultados.append(c)
            else:
                # Fallback por si el árbol no fue inicializado (no debería
                # pasar si se arma el menú desde main.py).
                resultados = self.catalogo.buscar(criterio) if hasattr(self.catalogo, "buscar") else []
 
            if resultados:
                print(f"\nSe encontraron {len(resultados)} canción(es):\n")
                for c in resultados:
                    print(self._formatear_cancion(c))
            else:
                print(f"\nNo se encontraron canciones para '{criterio}'.")
                print("(Búsqueda exacta por título/artista — revisá mayúsculas o probá la opción 3 para búsqueda parcial).")
 

        elif opcion == "3":
            self.limpiar_pantalla()
            print("--- FILTRAR CANCIONES ---")
            valor = input("Ingrese criterio (ej. Electropop, Clasica, Desamor, 2025, Hotel Miranda): ").strip()
            if valor:
                resultados = []
                
                def normalizar(texto):
                    if not texto:
                        return ""
                    m = str(texto).lower()
                    for orig, reemp in [("á","a"), ("é","e"), ("í","i"), ("ó","o"), ("ú","u")]:
                        m = m.replace(orig, reemp)
                    return m
 
                busqueda = normalizar(valor)
 
                todas = []
                if hasattr(self.catalogo, "listar"):
                    todas = self.catalogo.listar()
                elif hasattr(self.catalogo, "canciones"):
                    todas = self.catalogo.canciones
 
                for c in todas:
                    valores = []
                    if isinstance(c, dict):
                        valores = list(c.values())
                    elif hasattr(c, "__dict__"):
                        valores = list(c.__dict__.values())
 
                    texto_cancion = []
                    for v in valores:
                        if isinstance(v, list):
                            texto_cancion.append(" ".join(map(str, v)))
                        elif v is not None:
                            texto_cancion.append(str(v))
                    
                    cadena_buscar = normalizar(" ".join(texto_cancion))
 
                    if busqueda in cadena_buscar:
                        resultados.append(c)
 
                if resultados:
                    print(f"\nSe encontraron {len(resultados)} canción(es):\n")
                    for c in resultados:
                        print(self._formatear_cancion(c))
                else:
                    print(f"\nNo se encontraron canciones para '{valor}'.")
            else:
                print("Filtro cancelado: el texto no puede estar vacío.")
 

        elif opcion == "5":
            self.limpiar_pantalla()
            print("--- EXPLORAR COLABORADOR ---")
            colaborador = input("Ingrese el nombre del colaborador/artista: ").strip()
 
            if not colaborador:
                print("Búsqueda cancelada: el nombre no puede estar vacío.")
                input("\nPresione ENTER para continuar...")
                return True
 
            if self.arbol_artistas is not None:
                resultados = self.arbol_artistas.buscar_por_artista(colaborador)
            else:
                resultados = []
 
            if resultados:
                print(f"\nCanciones con '{colaborador}': {len(resultados)}\n")
                for c in resultados:
                    print(self._formatear_cancion(c))
            else:
                print(f"\nNo se encontraron canciones con '{colaborador}'.")
 
        elif opcion in ["4", "6", "7", "8"]:
            self.limpiar_pantalla()
            mapeo_metodos = {
                "4": ("playlist_x_tiempo", "Playlist por Tiempo"),
                "6": ("comparar_versiones", "Comparar Versiones"),
                "7": ("puente_temporal", "Puente Temporal"),
                "8": ("obtener_version_clasica", "Obtener Versión Clásica"),
            }
            metodo_nombre, titulo = mapeo_metodos[opcion]
            print(f"--- {titulo.upper()} ---")
 
            if hasattr(self.catalogo, metodo_nombre):
                metodo = getattr(self.catalogo, metodo_nombre)
                try:
                    res = metodo()
                    if res:
                        if isinstance(res, list):
                            for c in res:
                                print(self._formatear_cancion(c))
                        else:
                            print(self._formatear_cancion(res))
                    else:
                        print("Sin datos para mostrar.")
                except Exception as e:
                    print(f"La función '{metodo_nombre}' requiere argumentos adicionales. Detalle: {e}")
            else:
                print(f"[En desarrollo] Esta opción usará '{metodo_nombre}()' cuando lo agreguen al catálogo.")
 
        elif opcion == "0":
            print("\n¡Gracias por usar POPBOT!")
            return False
 
        else:
            print("\nOpción inválida. Intente de nuevo.")
 
        input("\nPresione ENTER para continuar...")
        return True
 