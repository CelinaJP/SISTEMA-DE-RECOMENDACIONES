
from servicios.gestor_catalogo import Catalogo as CatalogoDeCancion
from ui.terminal import MenuInicio
from estructuras.arbol_binario import ArbolPorTitulo, ArbolPorArtista
 
 
def main():
    catalogo = CatalogoDeCancion()
    if hasattr(catalogo, "cargar_desde_json"):
        catalogo.cargar_desde_json("datos/miranda_canciones.json")
 
    arbol_titulos = ArbolPorTitulo()
    arbol_titulos.cargar_desde_catalogo(catalogo)
 
    arbol_artistas = ArbolPorArtista()
    arbol_artistas.cargar_desde_catalogo(catalogo)
 
    menu = MenuInicio(catalogo, arbol_titulos, arbol_artistas)
 
    ejecutando = True
    while ejecutando:
        menu.mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        ejecutando = menu.procesar_opcion(opcion)
 
 
if __name__ == "__main__":
    main()
 