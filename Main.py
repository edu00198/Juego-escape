# Main.py
import time
from movimiento_jugador import principal
from intro import main_intro
from pantalla_carga import press_any_key_screen
from menu.menuzaso import menus

def main():
    
    #main_intro()   # Ejecuta la intro del juego
    #time.sleep(1)  # Pausa breve entre la intro y el menu
    press_any_key_screen()
    time.sleep(1)
    menus()         # Muestra el menú principal
    
    
    
    principal.ejecutar_juego()

if __name__ == "__main__":
    main()