#mapa_1.py
import pygame
import sys
import os
from .mapa_2 import ejecutar_mapa2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from movimiento_jugador.jugador import Jugador
from mapas.mapa1_data import fondo_mapa, SCALED_HEIGHT, SCALED_WIDTH, OFFSET_X, OFFSET_Y, puerta_1, colisiones_escaladas

pantalla = pygame.display.set_mode((1280, 720))

def ejecutar_mapa1():
    # Bucle principal
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 26
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)
    
    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2

    pos_x = (fondo_mapa.get_width() * escala - ancho_jugador) // 2
    pos_y = (fondo_mapa.get_height() * escala - alto_jugador) // 2

    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR)

    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        jugador.manejar_teclas()

        
        # Limpiar pantalla
        pantalla.fill((0, 0, 0))
        
        # Dibujar el mapa escalado y centrado
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
        
        # Dibujar colisiones (para depuración).👍
        """
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)  # Rojo = colisiones
        
        # Dibujar puerta (para depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_1, 2)  # Azul = puerta
        """
        jugador.dibujar(pantalla, offset_x, offset_y)
        print(jugador.rect)
        print(puerta_1)
        print("posicion jugador.", jugador.rect.topleft)
        print("posicion puerta.", puerta_1.topleft)

        if jugador.rect.colliderect(puerta_1):
            ejecutar_mapa2()  # Llama a la función del mapa 2

        pygame.display.flip()
        clock.tick(60)
       
            
     

    pygame.quit()
    sys.exit()

ejecutar_mapa1()