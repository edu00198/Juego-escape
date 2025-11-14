import pygame
import sys
import time, os

# No importar mapas pesados al inicio: se precargarán en background durante la intro
print("Iniciando módulo principal...")
def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        pygame.init()
    except Exception as e:
        print(f"Error inicializando pygame: {e}")
        raise


    try:
        print("Iniciando juego...")

        # Cargar módulos ligeros necesarios para la intro/menu justo antes de usarlos
        try:
            
            from intro_y_menu.intro import main_intro
            from intro_y_menu.pantalla_carga import press_any_key_screen
            from intro_y_menu.menu.menuzaso import menus
        except Exception as e:
            print(f"Error importando módulos de intro/menu: {e}")
            raise

        # Intentar arrancar la precarga en background si existe
        try:
            from intro_y_menu.loader import start_background_load
        except Exception:
            start_background_load = None

        if start_background_load:
            try:
                start_background_load()
            except Exception as e:
                print(f"Advertencia: start_background_load falló: {e}")


        # Ejecutar intro y menu
        #main_intro()
        #press_any_key_screen()
        menus()

        print("Llamando a ejecutar_mapa1()...")

        # Importar mapa pesado justo antes de ejecutarlo
        try:
            from juego import mapa_1
        except Exception as e:
            print(f"Error importando mapa_1 en runtime: {e}")
            raise

        # Ejecutar mapa
        limpiar_terminal()
        mapa_1.ejecutar_mapa1()


    finally:
        # Asegurar que pygame se cierre al terminar (si se inicializó)
        try:

            pygame.quit()
        except Exception:

            pass


if __name__ == "__main__":
    try:

        main()
    except Exception as e:

        print(f"Fallo en la ejecución principal: {e}")
        # Mostrar traceback corto
        import traceback
        traceback.print_exc()
        sys.exit()