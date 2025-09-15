# Main.py
import time
print("Importando módulo mapa_1...")
from movimiento_jugador import mapa_1
print("Importando otros módulos...")
from intro import main_intro
from pantalla_carga import press_any_key_screen
from menu.menuzaso import menus

def main():
    print("Iniciando juego...")
    #main_intro()   # Ejecuta la intro del juego
    #time.sleep(1)  # Pausa breve entre la intro y el menu
    #press_any_key_screen()  # Muestra la pantalla de "Press Any Key"
    #menus()         # Muestra el menú principal
    print("Llamando a ejecutar_mapa1()...")
    mapa_1.ejecutar_mapa1()

main()


