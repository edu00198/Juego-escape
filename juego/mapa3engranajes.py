# mapa3engranajes.py
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador
from juego.menu_pausa import pause_menu
from juego.engranajes import minijuego_engranares
from assets.mapas.mapa3engranajes_data import (
    fondo_escalado,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    colisiones_escaladas,
    puerta_4  # Puerta que lleva al mapa 4
)

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Definir el área de activación del minijuego (usar un rectángulo en el centro del mapa)
AREA_MINIJUEGO = pygame.Rect(
    OFFSET_X + SCALED_WIDTH // 3,  # Un tercio desde la izquierda
    OFFSET_Y + SCALED_HEIGHT // 3,  # Un tercio desde arriba
    SCALED_WIDTH // 3,  # Un tercio del ancho
    SCALED_HEIGHT // 3   # Un tercio del alto
)

def ejecutar_mapa3engranajes():
    clock = pygame.time.Clock()
    running = True

    # Calcular posición inicial del jugador (cerca de la entrada)
    pos_x = OFFSET_X + SCALED_WIDTH // 2  # Centro del mapa horizontalmente
    pos_y = SCALED_HEIGHT - 50  # Cerca del borde inferior
    
    jugador = Jugador(pos_x, pos_y, 
                      ancho=23, alto=15, 
                      escala=ESCALA_JUGADOR, 
                      colisiones=colisiones_escaladas)

    minijuego_completado = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu(pantalla)

        # Guardar posición anterior para colisiones
        pos_anterior = jugador.rect.topleft
        jugador.manejar_teclas()

        # Colisiones con objetos del mapa
        for colision in colisiones_escaladas:
            if jugador.rect.colliderect(colision):
                jugador.rect.topleft = pos_anterior
                jugador.sprite_pos.x = jugador.rect.x
                jugador.sprite_pos.y = jugador.rect.y
                break

        # Verificar si el jugador está en el área del minijuego
        if jugador.rect.colliderect(AREA_MINIJUEGO) and not minijuego_completado:
            print("¡Iniciando minijuego de engranajes!")
            resultado = minijuego_engranares()
            # Restaurar resolución del juego después del minijuego
            pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
            if resultado == "completado":  # Si el jugador completa el minijuego
                minijuego_completado = True
                print("¡Minijuego completado!")

        # Verificar si el jugador puede pasar al siguiente mapa
        if jugador.rect.colliderect(puerta_4) and minijuego_completado:
            print("¡Pasando al mapa 4!")
            from juego.mapa_4 import ejecutar_mapa4  # Import here to avoid circular dependency
            return ejecutar_mapa4(pantalla, spawn_point='engranajes')

        # Dibujar todo
        pantalla.fill((0, 0, 0))  # Fondo negro
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))  # Mapa
        jugador.dibujar(pantalla)
        
        # Si el minijuego no está completado, dibujar un indicador en el área del minijuego
        if not minijuego_completado:
            pygame.draw.rect(pantalla, (255, 255, 255, 128), AREA_MINIJUEGO, 2)  # Rectángulo blanco semitransparente

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()