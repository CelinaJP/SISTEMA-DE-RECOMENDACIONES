from servicios.gestor_catalogo import Catalogo as CatalogoDeCancion
from ui.terminal import MenuInicio


def main():
    catalogo = CatalogoDeCancion()
    if hasattr(catalogo, "cargar_desde_json"):
        catalogo.cargar_desde_json("datos/miranda_canciones.json")

    menu = MenuInicio(catalogo)

    ejecutando = True
    while ejecutando:
        menu.mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        ejecutando = menu.procesar_opcion(opcion)


if __name__ == "__main__":
    main()