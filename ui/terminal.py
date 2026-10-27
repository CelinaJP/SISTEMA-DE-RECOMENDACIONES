# ui/terminal.py

import os
from estructuras.arbol_binario import ArbolPorArtista, ArbolPorTitulo
from servicios.gestor_catalogo import Catalogo as CatalogoDeCancion


class MenuInicio:

    def __init__(
        self,
        catalogo: CatalogoDeCancion,
        arbol_titulos: ArbolPorTitulo = None,
        arbol_artistas: ArbolPorArtista = None,
        arbol_general = None,
        grafo_colaboraciones = None,
    ):
        self.catalogo = catalogo
        self.arbol_titulos = arbol_titulos
        self.arbol_artistas = arbol_artistas
        self.arbol_general = arbol_general
        self.grafo_colaboraciones = grafo_colaboraciones

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
        print(" 5. Explorar Conexiones por Colaborador (Grafo)")
        print(" 6. Comparar Versiones")
        print(" 7. Puente Temporal")
        print(" 8. Obtener Versión Clásica")
        print(" 9. Explorar categorías (Era -> Género -> Canciones)")
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
            print("--- TOP 10 CANCIONES MÁS POPULARES (Vía Cola de Prioridad / Heap) ---\n")
            from algoritmos.ranking import obtener_top_n
            top_10 = obtener_top_n(self.catalogo, n=10)
            if top_10:
                for i, c in enumerate(top_10, 1):
                    from algoritmos.prioridad import obtener_prioridad
                    pop = obtener_prioridad(c)
                    print(f"{i}. {self._formatear_cancion(c)} | Popularidad/Prioridad: {pop}")
            else:
                print("No hay canciones registradas en el catálogo.")
            input("\nPresione ENTER para continuar...")
            return True
        
        # 2. BUSCAR CANCIÓN (por ABB)
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
                ids_vistos = set()
                for c in por_titulo + por_artista:
                    cid = getattr(c, "id", None)
                    if cid not in ids_vistos:
                        ids_vistos.add(cid)
                        resultados.append(c)
            else:
                resultados = self.catalogo.buscar(criterio) if hasattr(self.catalogo, "buscar") else []

            if resultados:
                print(f"\nSe encontraron {len(resultados)} canción(es):\n")
                for c in resultados:
                    print(self._formatear_cancion(c))
            else:
                print(f"\nNo se encontraron canciones para '{criterio}'.")
            input("\nPresione ENTER para continuar...")
            return True

        # 3. FILTRAR CANCIONES
        elif opcion == "3":
            self.limpiar_pantalla()
            print("--- FILTRAR CANCIONES ---")
            valor = input("Ingrese criterio (ej. Electropop, Clasica, Desamor, 2025): ").strip()
            if valor:
                resultados = []
                def normalizar(texto):
                    if not texto: return ""
                    m = str(texto).lower()
                    for orig, reemp in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")]:
                        m = m.replace(orig, reemp)
                    return m

                busqueda = normalizar(valor)
                todas = self.catalogo.listar() if hasattr(self.catalogo, "listar") else []

                for c in todas:
                    valores = list(c.__dict__.values()) if hasattr(c, "__dict__") else []
                    texto_cancion = []
                    for v in valores:
                        if isinstance(v, list):
                            texto_cancion.append(" ".join(map(str, v)))
                        elif v is not None:
                            texto_cancion.append(str(v))
                    if busqueda in normalizar(" ".join(texto_cancion)):
                        resultados.append(c)

                if resultados:
                    print(f"\nSe encontraron {len(resultados)} canción(es):\n")
                    for c in resultados:
                        print(self._formatear_cancion(c))
                else:
                    print(f"\nNo se encontraron canciones para '{valor}'.")
            else:
                print("Filtro cancelado: el texto no puede estar vacío.")
            input("\nPresione ENTER para continuar...")
            return True

        # 5. EXPLORAR COLABORADOR (GRAFO)
        elif opcion == "5":
            self.limpiar_pantalla()
            print("--- EXPLORAR CONEXIONES POR COLABORADOR (GRAFO) ---")
            colaborador = input("Ingrese el nombre del artista o colaborador: ").strip()

            if not colaborador:
                print("Búsqueda cancelada: el nombre no puede estar vacío.")
                input("\nPresione ENTER para continuar...")
                return True

            if self.grafo_colaboraciones:
                directas = self.grafo_colaboraciones.obtener_conexiones_directas(colaborador)
                
                if not directas:
                    print(f"\n[!] No se encontró a '{colaborador}' en la red de colaboraciones.")
                else:
                    nombre_real = self.grafo_colaboraciones._encontrar_key_case_insensitive(colaborador)
                    print(f"\n[ COLABORADOR DETECTADO: {nombre_real} ]")
                    print("-" * 60)
                    print("Colaboraciones directas:")
                    for colab, canciones in directas.items():
                        canciones_str = ", ".join(f'"{c}"' for c in canciones)
                        print(f" - {colab} (en {canciones_str})")
                        
                    print("\nRed de conexiones indirectas (2 grados de separación):")
                    indirectas = self.grafo_colaboraciones.buscar_conexiones_indirectas(nombre_real, grados=2)
                    
                    # Filtrar para mostrar solo las de grado 2 (las de grado 1 ya son directas)
                    indirectas_grado2 = {k: v for k, v in indirectas.items() if v[0] == 2}
                    
                    if indirectas_grado2:
                        for colab, (grado, camino) in indirectas_grado2.items():
                            camino_str = " ──► ".join(camino)
                            print(f" - {colab} (Ruta: {camino_str})")
                    else:
                        print(" - No se encontraron conexiones indirectas a 2 grados.")
                    print("-" * 60)
            else:
                print("El grafo de colaboraciones no está inicializado.")

            input("\nPresione ENTER para continuar...")
            return True

        # OPCIONES EN DESARROLLO (4, 6, 7, 8)
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
            print(f"[En desarrollo] Esta opción usará '{metodo_nombre}()' cuando lo agreguen al catálogo.")
            input("\nPresione ENTER para continuar...")
            return True

        # 9. EXPLORAR CATEGORÍAS (Árbol General)
        elif opcion == "9":
            self.limpiar_pantalla()
            print("--- EXPLORAR CATEGORÍAS (JERARQUÍA DEL CATÁLOGO) ---\n")
            if self.arbol_general is None or self.arbol_general.raiz is None:
                print("El árbol general no está inicializado.")
            else:
                eras = self.arbol_general.raiz.hijos
                if not eras:
                    print("No hay eras registradas en el árbol.")
                else:
                    print("Eras disponibles:")
                    for idx, era in enumerate(eras, 1):
                        print(f"  {idx}. {era.etiqueta}")

                    op_era = input("\nSeleccione el número de la Era a explorar (o Enter para volver): ").strip()
                    if op_era.isdigit() and 1 <= int(op_era) <= len(eras):
                        era_elegida = eras[int(op_era) - 1]
                        self.limpiar_pantalla()
                        print(f"--- ERA: {era_elegida.etiqueta} ---\n")
                        
                        generos = era_elegida.hijos
                        if not generos:
                            print("No hay géneros en esta era.")
                        else:
                            print("Géneros disponibles:")
                            for g_idx, gen in enumerate(generos, 1):
                                print(f"  {g_idx}. {gen.etiqueta} ({len(gen.canciones)} canciones)")

                            op_gen = input("\nSeleccione el número del Género a explorar (o Enter para volver): ").strip()
                            if op_gen.isdigit() and 1 <= int(op_gen) <= len(generos):
                                gen_elegido = generos[int(op_gen) - 1]
                                self.limpiar_pantalla()
                                print(f"--- CANCIONES DE LA ERA '{era_elegida.etiqueta}' EN GÉNERO '{gen_elegido.etiqueta}' ---\n")
                                for c in gen_elegido.canciones:
                                    print(self._formatear_cancion(c))

            input("\nPresione ENTER para continuar...")
            return True

        elif opcion == "0":
            print("\n¡Gracias por usar POPBOT!")
            return False

        else:
            print("\nOpción inválida. Intente de nuevo.")
            input("\nPresione ENTER for continuar...")
            return True
        