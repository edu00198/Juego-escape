import pygame
import sys
import os
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, ESCALA_JUGADOR
from menu.button import Button
from movimiento_jugador.jugador import Jugador
from movimiento_jugador.colisiones import colisiones_mapa_2, puerta_2_entrada, puerta_2_salida
from mapas.fondo import mapa2
from .menu_pausa import pause_menu


def ejecutar_mapa2():
        # mapa2.py
    from configuracion import mapa_actual

    # Cambiar el mapa actual
    mapa_actual.mapa_actual = "mapa2"

    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Juego Escape")

    # Fondo 2
    try:
        fondo = pygame.image.load(mapa2).convert()  # fondo_2 viene de configuracion.py
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

        
        for rect in colisiones_mapa_2:
            pygame.draw.rect(pantalla, (255, 0, 0), rect, 2)  # dibuja cada rect en la pantalla
            pygame.draw.rect(pantalla, (0, 0, 255), puerta_2_entrada, 2)  # dibuja la puerta en verde
            pygame.draw.rect(pantalla, (0, 0, 255), puerta_2_entrada, 2) 



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
    ejecutar_mapa2()