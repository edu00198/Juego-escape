import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador
from juego.mapa_5 import ejecutar_mapa5
from assets.mapas.mapa4_data import (
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

from .engranajes import minijuego_engranares  # importamos el minijuego

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

def ejecutar_mapa4():
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
    pos_x = puerta2pos[0] - ancho_jugador * -10
    pos_y = puerta2pos[1] - alto_jugador * -2
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)

    # Fondo escalado
    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    # Imagen decorativa encima del jugador (opcional)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_pared = os.path.join(BASE_DIR, "assets", "mapas", "paredes_mapa_4.png")
    imagen_pared = pygame.image.load(ruta_pared).convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen_pared, (1280, 720))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        jugador.manejar_teclas()

        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
        jugador.dibujar(pantalla, offset_x, offset_y)
        pantalla.blit(imagen_escalada, (0, 0))

        
        #Dibujar colisiones (opcional para depuración)
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)

        #Dibujar puertas (opcional para depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_3_entrada, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_salida, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_engranaje, 2)
        pygame.draw.rect(pantalla, (255, 0, 255), puerta_3_cuatro_en_raya, 2)

        
        pygame.display.flip()
        clock.tick(60)

        # Transición al siguiente mapa
        if jugador.rect.colliderect(puerta_3_salida):
            print("Transición al siguiente mapa")
            running = False
            return
            
        if jugador.rect.colliderect(puerta_3_entrada):
            print("regresa a mapa 2")
            #running = False  # Aquí puedes llamar al siguiente mapa si lo tienes
            #return 2
    
        if jugador.rect.colliderect(puerta_3_cuatro_en_raya):
            print("Transición al minijuego de 4 en raya")
            running = False
            return
            

        # Minijuego engranajes: entrar y repetir hasta completar
        if jugador.rect.colliderect(puerta_3_engranaje):
            while True:
                resultado = minijuego_engranares()
                # Restaurar resolución del juego después del minijuego
                pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
                if resultado == "completado":
                    print("✅ Mecanismo alineado, puedes continuar en mapa 3")
                    # Eliminar cualquier rect de colisión que se solape con el área del engranaje
                    antes = len(colisiones_escaladas)
                    colisiones_escaladas[:] = [r for r in colisiones_escaladas if not r.colliderect(puerta_3_engranaje)]
                    despues = len(colisiones_escaladas)
                    print(f"Colisiones removidas: {antes - despues}")
                    # Mover al jugador fuera de la zona del engranaje para evitar re-trigger inmediato
                    try:
                        # Intentar mover a la derecha del trigger
                        new_x = int(puerta_3_engranaje.right + 5)
                        max_x = ANCHO_PANTALLA - jugador.rect.width
                        if new_x <= max_x:
                            jugador.rect.x = new_x
                        else:
                            # Si no cabe a la derecha, intentar a la izquierda
                            new_x_left = int(puerta_3_engranaje.left - jugador.rect.width - 5)
                            if new_x_left >= 0:
                                jugador.rect.x = new_x_left
                            else:
                                # Si no cabe a los lados, intentar abajo
                                new_y = int(puerta_3_engranaje.bottom + 5)
                                max_y = ALTO_PANTALLA - jugador.rect.height
                                if new_y <= max_y:
                                    jugador.rect.y = new_y
                                else:
                                    # Fallback: arriba dentro de la pantalla
                                    jugador.rect.y = max(0, int(puerta_3_engranaje.top - jugador.rect.height - 5))

                        # Actualizar sprite_pos para que el dibujo no quede desincronizado
                        offset_x_j = 58
                        offset_y_j = 101
                        jugador.sprite_pos.x = jugador.rect.x - offset_x_j
                        jugador.sprite_pos.y = jugador.rect.y - offset_y_j
                    except Exception:
                        pass
                    break
                else:
                    # Mostrar un mensaje y repetir; el minijuego ya maneja reinicios
                    print("❌ Fallaste el minijuego, intenta de nuevo")

    pygame.quit()
    sys.exit()
