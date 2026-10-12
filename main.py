from estructuras.arbol_binario import ArbolPorArtista, ArbolPorTitulo
from estructuras.arbol_general import ArbolGeneral
from servicios.gestor_catalogo import Catalogo as CatalogoDeCancion
from ui.terminal import MenuInicio


def main():
    catalogo = CatalogoDeCancion()
    if hasattr(catalogo, "cargar_desde_json"):
        catalogo.cargar_desde_json("datos/miranda_canciones.json")

    # Inicialización e inyección de los Árboles (Binarios y General)
    arbol_titulos = ArbolPorTitulo()
    arbol_artistas = ArbolPorArtista()
    arbol_general = ArbolGeneral("CatalogoMirandaGeneral")

    if hasattr(arbol_titulos, "cargar_desde_catalogo"):
        arbol_titulos.cargar_desde_catalogo(catalogo)
        arbol_artistas.cargar_desde_catalogo(catalogo)
        arbol_general.cargar_desde_catalogo(catalogo)

    # Creamos el menú e inyectamos el árbol general
    menu = MenuInicio(catalogo, arbol_titulos, arbol_artistas, arbol_general)

    ejecutando = True
    while ejecutando:
        menu.mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        ejecutando = menu.procesar_opcion(opcion)


if __name__ == "__main__":
    main()
    