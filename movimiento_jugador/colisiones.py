"""este codigo define las colisiones"""
import pygame
from jugador import Jugador  # Importo la clase, no una instancia

def detectar_colision(rect1, rect2):
    return rect1.colliderect(rect2)

# Lista de obstáculos
colisiones = [
    pygame.Rect(50, 50, 100, 100),
    pygame.Rect(75, 75, 100, 100)
]

# Crear una instancia del jugador para probar
jugador = Jugador(60, 60, 32, 32)  # x, y, ancho, alto

# Chequeo de colisiones contra todos los obstáculos
for obstaculo in colisiones:
    if detectar_colision(jugador.rect, obstaculo):
        print("¡Colisión detectada con obstáculo!")
