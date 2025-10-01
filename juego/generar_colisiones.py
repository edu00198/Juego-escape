import pygame

TILE_SIZE = 16  # el tamaño de cada tile del mapa

def generar_colisiones_desde_matriz(matriz):
    colisiones = []
    for y, fila in enumerate(matriz):
        for x, valor in enumerate(fila):
            if valor == 1:
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                colisiones.append(rect)
    return colisiones
