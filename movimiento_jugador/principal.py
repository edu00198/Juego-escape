import pygame
import sys
import os
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, ESCALA_JUGADOR
from .jugador import Jugador
from menu.button import Button
from menu.settings import settings_menu


def pause_menu(window):
    """
    Menú de pausa que aparece al presionar ESC.
    Botones: Reanudar, Salir, Ayuda, Configuración
    """
    clock = pygame.time.Clock()
    BASE_DIR = os.path.dirname(__file__)

    # Fondo semi-transparente
    fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
    fondo.fill((0, 0, 0))
    fondo.set_alpha(180)

    # Crear botones
    btn_width = 300
    btn_height = 60
    spacing = 20
    start_y = (ALTO_PANTALLA - (btn_height * 4 + spacing * 3)) // 2

    reanudar_button = Button(None, (ANCHO_PANTALLA//2, start_y), text="Reanudar")
    salir_button = Button(None, (ANCHO_PANTALLA//2, start_y + (btn_height + spacing)), text="Salir")
    ayuda_button = Button(None, (ANCHO_PANTALLA//2, start_y + 2*(btn_height + spacing)), text="Ayuda")
    config_button = Button(None, (ANCHO_PANTALLA//2, start_y + 3*(btn_height + spacing)), text="Configuración")

    buttons = [reanudar_button, salir_button, ayuda_button, config_button]
    selected_index = 0
    buttons[selected_index].hover_effect = True

    paused = True
    while paused:
        window.blit(fondo, (0, 0))

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
                    elif clicked_button == salir_button:
                        pygame.quit()
                        sys.exit()
                    elif clicked_button == ayuda_button:
                        print("Mostrar ayuda...")
                    elif clicked_button == config_button:
                        settings_menu(window)

        # Actualizar botones
        for i, btn in enumerate(buttons):
            btn.hover_effect = (i == selected_index)
            btn.update()
            btn.draw(window)

        pygame.display.flip()
        clock.tick(60)


def ejecutar_juego():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("movimiento_jugador")

    from configuracion import fondo_1
    try:
        fondo = pygame.image.load(fondo_1).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = None

    ancho_jugador = 50
    alto_jugador = 50
    pos_x = (ANCHO_PANTALLA - ancho_jugador) // 2
    pos_y = (ALTO_PANTALLA - alto_jugador) // 2
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR)

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        reloj.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # Llamar al menú de pausa
                    pause_menu(pantalla)

        # Manejar movimiento del jugador
        jugador.manejar_teclas()

        # Dibujar fondo
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(BLANCO)

        # Dibujar jugador
        jugador.dibujar(pantalla)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    ejecutar_juego()