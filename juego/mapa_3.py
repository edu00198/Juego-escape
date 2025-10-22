import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador
from juego.mapa_5 import ejecutar_mapa5
from juego.mapa_3_4_en_raya import ejecutar_mapa4_en_raya
from juego.mapa_4 import ejecutar_mapa4
from juego.menu_pausa import pause_menu
from assets.mapas.mapa3_data_nuevo0 import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    puerta_3_entrada,
    puerta_3_salida_al_mapa_4 as puerta_3_salida,
    puerta_3_engranaje,
    puerta_3_cuatro_en_raya,
    colisiones_escaladas
)

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

def ejecutar_mapa3():
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 23
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)

    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2

    # Posición inicial del jugador frente a la puerta de entrada
    puerta2pos = puerta_3_entrada.topleft
    pos_x = puerta2pos[0] - ancho_jugador * -3
    pos_y = puerta2pos[1] - alto_jugador * -4
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)

    # Fondo escalado
    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    # Imagen decorativa encima del jugador (opcional)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_pared = os.path.join(BASE_DIR, "assets", "mapas", "paredes_mapa3.png")
    imagen_pared = pygame.image.load(ruta_pared).convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen_pared, (1280, 720))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    try:
                        state = {
                            'mapa': 'mapa3',
                            'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y)
                        }
                    except Exception:
                        state = None
                    pause_menu(pantalla, mapa_actual=3, state=state)

        jugador.manejar_teclas()

        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
        jugador.dibujar(pantalla, offset_x, offset_y)
        pantalla.blit(imagen_escalada, (0, 0))

        
        #Dibujar colisiones (opcional para depuración)
        """for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)"""

        #Dibujar puertas (opcional para depuración)
        """pygame.draw.rect(pantalla, (0, 0, 255), puerta_3_entrada, 2)"""
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_salida, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_engranaje, 2)
        pygame.draw.rect(pantalla, (255, 0, 255), puerta_3_cuatro_en_raya, 2)

        
        pygame.display.flip()
        clock.tick(60)

        # Transición al siguiente mapa
        if jugador.rect.colliderect(puerta_3_salida):
            print("Transición al siguiente mapa")
            running = False
            ejecutar_mapa4()
            
        if jugador.rect.colliderect(puerta_3_entrada):
            print("regresa a mapa 2")
            #running = False  # Aquí puedes llamar al siguiente mapa si lo tienes
            #return 2
    
        if jugador.rect.colliderect(puerta_3_cuatro_en_raya):
            print("Transición al minijuego de 4 en raya")
            running = False
            ejecutar_mapa4_en_raya()
            

        

    pygame.quit()
    sys.exit()
