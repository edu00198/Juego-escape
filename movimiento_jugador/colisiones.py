"""este codigo define las colisiones"""
import pygame
from .jugador import Jugador  # Importo la clase, no una instancia

def detectar_colision(rect1, rect2):
    return rect1.colliderect(rect2)


# Lista de rectángulos de colisión
colisiones = [
    pygame.Rect(0, 0, 320, 270), #cuadrado arriba a la derecha/ celda

    pygame.Rect(0, 300, 60, 360), # borde izq
    pygame.Rect(1220, 170, 60, 520),#borde derecha

    pygame.Rect(320, 0, 340, 150),# borde superior izq
    pygame.Rect(750, 0, 500, 150),# borde superior der
    
    pygame.Rect(60, 650, 1200, 40),# borde inferior

    pygame.Rect(835, 480, 370, 190)  # cajas der
]

puerta = pygame.Rect(660, 0, 90, 115)  # Definición de la puerta

#def dibujar_colisiones(pantalla):
#    for rect in colisiones:
#        pygame.draw.rect(pantalla, (255, 0, 0), rect, 2)  # dibuja cada rect en la pantalla
#    pygame.draw.rect(pantalla, (0, 0, 255), puerta, 2)  # dibuja la puerta en verde



