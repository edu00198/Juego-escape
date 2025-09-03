# principal
import pygame
import sys
import os
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, ESCALA_JUGADOR, m1_opciones, m2_opciones
from menu.button import Button
from menu.settings import settings_menu
from menu.menuzaso import menus


def pause_menu(pantalla, mapa_actual=1):
    """
    Menú de pausa que aparece al presionar ESC.
    Botones: Reanudar, Ayuda, Configuración, Salir
    """
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("OPCIONES")

    # Fondo según el mapa
    try:
        if mapa_actual == 1:
            fondo = pygame.image.load(m1_opciones).convert()
        elif mapa_actual == 2:
            fondo = pygame.image.load(m2_opciones).convert()
        else:
            raise ValueError("Mapa no válido")

        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = None

    # Crear botones
    btn_width = 300
    btn_height = 60
    spacing = 20
    start_y = (ALTO_PANTALLA - (btn_height * 4 + spacing * 3)) // 2
    clock = pygame.time.Clock()

    if fondo:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill(BLANCO)

    reanudar_button = Button(None, (ANCHO_PANTALLA // 2, start_y), text="REANUDAR")
    ayuda_button = Button(None, (ANCHO_PANTALLA // 2, start_y + (btn_height + spacing)), text="AYUDA")
    config_button = Button(None, (ANCHO_PANTALLA // 2, start_y + 2 * (btn_height + spacing)), text="CONFIGURACION")
    salir_button = Button(None, (ANCHO_PANTALLA // 2, start_y + 3 * (btn_height + spacing)), text="SALIR")

    buttons = [reanudar_button, ayuda_button, config_button, salir_button]
    selected_index = 0
    buttons[selected_index].selected = True

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key in [pygame.K_UP, pygame.K_LEFT]:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_ESCAPE:
                    return  # volver al juego
                elif event.key == pygame.K_RETURN:
                    clicked_button = buttons[selected_index]
                    if clicked_button == reanudar_button:
                        return
                    elif clicked_button == ayuda_button:
                        print("Abrir ayuda...")
                    elif clicked_button == config_button:
                        settings_menu(pantalla)  # pasamos el mapa
                    elif clicked_button == salir_button:
                        menus()

        # Dibujar fondo
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(BLANCO)

        # Actualizar y dibujar botones
        for i, btn in enumerate(buttons):
            btn.selected = (i == selected_index)
            btn.update()
            btn.draw(pantalla)

        pygame.display.flip()
        clock.tick(60)
