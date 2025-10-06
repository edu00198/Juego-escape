# mapa_2.py
import pygame
import sys
import os
from juego.mapa3 import ejecutar_mapa3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador
from assets.mapas.mapa2_data import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    puerta_2_entrada,
    puerta_2_salida,
    colisiones_escaladas
)

pantalla = pygame.display.set_mode((1280, 720))

def ejecutar_mapa2():
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 23
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)

    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2 

    
    puerta2pos = puerta_2_entrada.topleft
    pos_x = puerta2pos[0]
    pos_y = puerta2pos[1] - alto_jugador * 10
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)


    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_pared = os.path.join(BASE_DIR,"assets", "mapas", "pared_mapa_2.png")

    # Cargar imagen
    imagen_pared = pygame.image.load(ruta_pared).convert_alpha()

    # Escalar si querés adaptarla al tamaño de pantalla
    imagen_escalada = pygame.transform.scale(imagen_pared, (1280, 720))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        jugador.manejar_teclas()

        pantalla.fill((0, 0, 0))  # Limpiar pantalla

        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))  # Fondo del mapa

        # Dibujar colisiones (opcional para depuración)👍
        """
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)

        # Dibujar puertas (opcional para depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_2_entrada, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_2_salida, 2)
        """
        jugador.dibujar(pantalla, offset_x, offset_y)  # Primero el jugador

        pantalla.blit(imagen_escalada, (0, 0))  # Después la imagen → queda arriba del jugador

        pygame.display.flip()

        clock.tick(60)

        # Transiciones de mapa
        if jugador.rect.colliderect(puerta_2_salida):
            print("Transición al mapa 3")
            running = False  # Detenemos el bucle para que el main pueda cargar el siguiente mapa
            ejecutar_mapa3()  # Detenemos el bucle para que el main pueda cargar el siguiente mapa

        elif jugador.rect.colliderect(puerta_2_entrada):
            print("Volver al mapa 1")
            running = False  # Detenemos el bucle para que el main pueda cargar el mapa 1
            # Indica al llamador que el jugador quiere volver a mapa1
            return "to_mapa1"

    pygame.quit()
    sys.exit()
