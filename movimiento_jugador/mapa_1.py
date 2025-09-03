#principal
import pygame
import sys
import os
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, ESCALA_JUGADOR
from .jugador import Jugador
from menu.button import Button
from movimiento_jugador.jugador import Jugador
from movimiento_jugador.colisiones import colisiones, puerta
from mapas.fondo import mapa1, mapa2
from .menu_pausa import pause_menu
from .mapa_2 import ejecutar_mapa2

def ejecutar_mapa1():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Juego Escape")

    # Fondo 1
    try:
        fondo = pygame.image.load(mapa1).convert()  # fondo_1 viene de configuracion.py
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
                ejecutar_mapa2()
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
    ejecutar_mapa1()