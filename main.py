from servicios.gestor_catalogo import cargar_catalogo

def mostrar_menu():
    print("\n" + "="*60)
    print("    EL BOT DE TU CORAZÓN — MIRANDA! (Recomendador Pop)")
    print("="*60)
    print(" 1. Cargar y verificar catálogo de canciones")
    print(" 0. Salir")
    print("="*60)

def main():
    # Se llama al módulo diseñado para leer y mapear el JSON con manejo de excepciones
    canciones_lista, canciones_dict = cargar_catalogo("datos/miranda_canciones.json")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            if canciones_lista:
                print(f"\n¡Éxito! Se cargaron {len(canciones_lista)} canciones correctamente en memoria.")
                print("\nPrimeras 3 canciones mapeadas a la clase Cancion:")
                for cancion in canciones_lista[:3]:
                    print(f" - ID {cancion.id}: {cancion.titulo} ({cancion.anio}) | Era: {cancion.era}")
            else:
                print("\nNo se pudieron cargar las canciones. Verifique la existencia o formato de 'datos/miranda_canciones.json'.")
            
            input("\nPresione ENTER para continuar...")

        elif opcion == "0":
            print("\n¡Gracias por usar POPBOT!")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()