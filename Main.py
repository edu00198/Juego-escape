import pygame
import time
# No importar mapas pesados al inicio: se precargarán en background durante la intro
print("Iniciando módulo principal...")
from intro_y_menu.intro  import main_intro
from intro_y_menu.pantalla_carga import press_any_key_screen
from intro_y_menu.menu.menuzaso import menus
try:
    # Intentar arrancar la precarga tan pronto como sea posible
    from intro_y_menu.loader import start_background_load
    try:
        start_background_load()
    except Exception:
        pass
except Exception:
    pass

def main():
    pygame.init()
    print("Iniciando juego...")
    main_intro()   # Ejecuta la intro del juego
    #time.sleep(1)  # Pausa breve entre la intro y el menu
    press_any_key_screen()  # Muestra la pantalla de "Press Any Key"
    menus()         # Muestra el menú principal
    print("Llamando a ejecutar_mapa1()...")
    # Importar el mapa justo antes de ejecutarlo para aprovechar la precarga
    try:
        from juego import mapa_1
    except Exception as e:
        print(f"Error importando mapa_1 en runtime: {e}")
        raise
    mapa_1.ejecutar_mapa1()

main()
