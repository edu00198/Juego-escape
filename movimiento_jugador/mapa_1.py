#principal
import pygame
import sys
import os
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, ESCALA_JUGADOR
from .jugador import Jugador
from menu.button import Button
from menu.settings import settings_menu
from movimiento_jugador.jugador import Jugador
from movimiento_jugador.colisiones import colisiones, puerta
from fondos.fondo import fondo_1,  f1_opciones
from menu.menuzaso import menus



def pause_menu(pantalla):
    """
    Menú de pausa que aparece al presionar ESC.
    Botones: Reanudar, Salir, Ayuda, Configuración
    """
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Opciones")

    # Fondo
    try:
        fondo = pygame.image.load(f1_opciones).convert()  # f1_opciones viene de configuracion.py
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = None

    # Crear botones (asumo que la clase Button está definida en otro lado)
    btn_width = 300
    btn_height = 60
    spacing = 20
    start_y = (ALTO_PANTALLA - (btn_height * 4 + spacing * 3)) // 2
    clock = pygame.time.Clock()
    if fondo:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill(BLANCO)

    reanudar_button = Button(None, (ANCHO_PANTALLA//2, start_y), text="REANUDAR")
    config_button = Button(None, (ANCHO_PANTALLA//2, start_y + 3*(btn_height + spacing)), text="CONFIGURACION")
    ayuda_button = Button(None, (ANCHO_PANTALLA//2, start_y + 2*(btn_height + spacing)), text="AYUDA")
    salir_button = Button(None, (ANCHO_PANTALLA//2, start_y + (btn_height + spacing)), text="SALIR")

    buttons = [reanudar_button,config_button, ayuda_button,salir_button]
    selected_index = 0
    buttons[selected_index].hover_effect = True

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
                    elif clicked_button == config_button:
                        settings_menu(pantalla)
                    elif clicked_button == ayuda_button:
                        print("")
                    elif clicked_button == salir_button:
                        menus()

        # Actualizar y dibujar botones
        for i, btn in enumerate(buttons):
            btn.selected = (i == selected_index)  # <<--- esto reemplaza hover_effect
            btn.update()
            btn.draw(pantalla)


        pygame.display.flip()
        clock.tick(60)


def ejecutar_juego():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Juego Escape")

    # Fondo 1
    try:
        fondo = pygame.image.load(fondo_1).convert()  # fondo_1 viene de configuracion.py
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = None


    ancho_jugador = 26
    alto_jugador = 32
    pos_x = (ANCHO_PANTALLA - ancho_jugador) // 2
    pos_y = (ALTO_PANTALLA - alto_jugador) // 2
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR)

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        clock.tick(60)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pause_menu(pantalla)

        # Movimiento del jugador con colisiones
        
        jugador.manejar_teclas()

        
        for rect in colisiones:
            pygame.draw.rect(pantalla, (255, 0, 0), rect, 2)  # dibuja cada rect en la pantalla
            pygame.draw.rect(pantalla, (0, 0, 255), puerta, 2)  # dibuja la puerta en verde



        # Chequear puerta
        if jugador.rect.colliderect(puerta):
            # Fondo 2
            try:
                fondo = pygame.image.load(fondo_2).convert()  # fondo_1 viene de configuracion.py
                fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
            except Exception as e:
                print(f"No se pudo cargar el fondo: {e}")
                fondo = None

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