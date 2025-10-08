    # Main.py
import pygame
import time
print("Importando módulo mapa_1...")
from juego import mapa_1
print("Importando otros módulos...")
from intro_y_menu.intro  import main_intro
from intro_y_menu.pantalla_carga import press_any_key_screen
from intro_y_menu.menu.menuzaso import menus

def main():
    pygame.init()
    print("Iniciando juego...")
    #main_intro()   # Ejecuta la intro del juego
    #time.sleep(1)  # Pausa breve entre la intro y el menu
    #press_any_key_screen()  # Muestra la pantalla de "Press Any Key"
    #menus()         # Muestra el menú principal
    print("Llamando a ejecutar_mapa1()...")
    mapa_1.ejecutar_mapa1()

main()



