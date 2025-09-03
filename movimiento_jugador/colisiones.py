"""este codigo define las colisiones"""
import pygame

import os

  


# Lista de rectángulos de colisión
colisiones_mapa_1 = [
    pygame.Rect(0, 0, 320, 270), #cuadrado arriba a la derecha/ celda

    pygame.Rect(0, 270, 60, 400), # borde izq
    pygame.Rect(1220, 130, 60, 550),#borde derecha

    pygame.Rect(320, 0, 340, 150),# borde superior izq
    pygame.Rect(750, 0, 530, 150),# borde superior der
    
    pygame.Rect(60, 660, 1200, 40),# borde inferior

    pygame.Rect(860, 480, 370, 190),  # cajas der

    pygame.Rect(660, 0, 90, 20)  # parte atras cajas
]

puerta_1 = pygame.Rect(660, 15, 90, 115)  # Definición de la puerta

colisiones_mapa_2 = [
        pygame.Rect(0, 0, 1200, 70),       # borde superior
        pygame.Rect(0, 70, 60, 650),      # borde izq

        
     ]     # parte atras puerta

puerta_2 = pygame.Rect(255, 255, 60, 60)
import pygame
import sys
import os
from mapas.fondo import mapa1, mapa2


def probar_colisiones():
    # Inicializar Pygame
    pygame.init()

    # Crear la ventana
    ANCHO = 1280
    ALTO = 720
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Visualización de Colisiones")

  
    try:
        fondo = pygame.image.load(mapa2).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = None

    # Reloj para controlar los FPS
    reloj = pygame.time.Clock()

    # Rectángulo de la puerta
    puerta_1 = pygame.Rect(660, 0, 90, 115)

    # Bucle principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dibujar fondo
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill((0, 0, 0))  # Fondo negro si no se carga imagen

        # Dibujar colisiones
        for rect in colisiones_mapa_2:
            pygame.draw.rect(pantalla, (255, 0, 0), rect, 2)  # Rojo

        # Dibujar la puerta
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_1, 2)  # Azul

        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(60)


probar_colisiones