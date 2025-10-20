import pygame
import sys
import os
pygame.init()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador
from juego.mapa_4 import ejecutar_mapa4
from assets.mapas.mapa3_4_en_raya_data import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    puerta_4 as puerta,
    colisiones_escaladas
)

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

def ejecutar_mapa4_en_raya():
    acertijo_en_raya = False
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 23
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)

    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2

    puerta4pos = puerta.topleft
    pos_x = puerta4pos[0]
    pos_y = puerta4pos[1] - alto_jugador * 10
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)

    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    
    # Imagen decorativa encima del jugador (opcional)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_pared = os.path.join(BASE_DIR, "assets", "mapas", "tablero.png")
    imagen_pared = pygame.image.load(ruta_pared).convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen_pared, (427, 240))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        jugador.manejar_teclas()
        

        #Dibujar puertas (opcional para depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta, 2)
        
        
        pantalla.fill((0, 0, 0))  # Limpiar pantalla

        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))  # Fondo del mapa

        """Dibujar colisiones (opcional para depuración)
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)"""

        #Dibujar puertas (opcional para depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta, 2)

        jugador.dibujar(pantalla, offset_x, offset_y)  # Primero el jugador
        
        centro_x = (ANCHO_PANTALLA - imagen_escalada.get_width()) // 2
        pantalla.blit(imagen_escalada, (centro_x, 150))


        
        pygame.display.flip()
        clock.tick(60)

        # Transiciones de mapa
        if jugador.rect.colliderect(puerta) and acertijo_en_raya==True:
            print("regresa a mapa 3")
            running = False  # Aquí puedes llamar al siguiente mapa si lo tienes
            ejecutar_mapa4()
            

    pygame.quit()
    sys.exit()