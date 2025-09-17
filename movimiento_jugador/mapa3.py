# mapa_2.py
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from movimiento_jugador.jugador import Jugador
from mapas.mapa3_data import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    puerta_3_entrada,
    puerta_3_salida,
    colisiones_escaladas
)

pantalla = pygame.display.set_mode((1280, 720))

def ejecutar_mapa3():
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 26
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)

    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2

    
    puerta2pos = puerta_3_entrada.topleft
    pos_x = puerta2pos[0]
    pos_y = puerta2pos[1] - alto_jugador * 10
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)


    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        jugador.manejar_teclas()

        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))

        # Dibujar colisiones (depuración)
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)

        # Dibujar puertas (depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_3_entrada, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_salida, 2)

        jugador.dibujar(pantalla, offset_x, offset_y)
        pygame.display.flip()
        clock.tick(60)

        # Transiciones de mapa
        if jugador.rect.colliderect(puerta_3_salida):
            print("Transición al mapa 3")
            running = False  # Detenemos el bucle para que el main pueda cargar el siguiente mapa

        elif jugador.rect.colliderect(puerta_3_entrada):
            print("Volver al mapa 1")
            return

    pygame.quit()
    sys.exit()
