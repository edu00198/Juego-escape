# mapa1_data.py
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador

pygame.init()

l_decoraciones = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,19,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,104,105,0],
   [0,43,44,0,0,0,0,0,0,0,0,0,0,0,103,91,92,128,129,0],
   [0,67,68,0,0,0,0,0,0,0,0,0,0,0,127,115,116,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
l_fire = [
   [0,0,0,0,0,0,1,2,0,0,0,0,0,1,2,0,0,0,0,0],
   [0,0,0,0,0,0,12,13,0,0,0,0,0,12,13,0,0,0,0,0],
   [0,0,0,0,0,0,23,24,0,0,0,0,0,23,24,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
l_objetos = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,279,280,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,292,293,0,0,0,0,0,0,0,0],
   [0,0,283,284,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,296,297,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
l_paredes = [
   [15,15,15,15,4,5,28,28,28,28,28,28,28,28,28,28,28,28,5,6],
   [15,15,15,15,16,18,41,41,41,41,41,41,41,41,41,41,41,41,18,19],
   [4,28,28,28,29,31,54,54,54,54,54,54,54,54,54,54,54,54,31,32],
   [16,41,41,41,42,0,0,0,0,0,0,0,0,0,0,0,0,0,0,19],
   [16,54,54,54,55,0,0,0,0,0,0,0,0,0,0,0,0,0,0,19],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [43,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,2,2,45]
]
l_piso = [
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274]
]
l_roturs_en_las_paredes = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,1,0,2,4,0,0,0,4,4,0,3,0,2,0,0],
   [0,0,0,0,29,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,49,50,51,52,0,0,0,49,50,51,52,0,0,49,50,51,52,0]
]
l_hitbox_mapa_1 = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
  [1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
  [1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
DESIRED_SCREEN_WIDTH = 1280
DESIRED_SCREEN_HEIGHT = 720
TILE_SIZE = 16 
MAP_WIDTH = 20
MAP_HEIGHT = 11

MAP_REAL_WIDTH = MAP_WIDTH * TILE_SIZE
MAP_REAL_HEIGHT = MAP_HEIGHT * TILE_SIZE

SCALE_X = DESIRED_SCREEN_WIDTH / MAP_REAL_WIDTH
SCALE_Y = DESIRED_SCREEN_HEIGHT / MAP_REAL_HEIGHT

SCALE_FACTOR = min(SCALE_X, SCALE_Y)

SCALED_WIDTH = int(MAP_REAL_WIDTH * SCALE_FACTOR)
SCALED_HEIGHT = int(MAP_REAL_HEIGHT * SCALE_FACTOR)

OFFSET_X = (DESIRED_SCREEN_WIDTH - SCALED_WIDTH) // 2
OFFSET_Y = (DESIRED_SCREEN_HEIGHT - SCALED_HEIGHT) // 2

pantalla = pygame.display.set_mode((1280, 720))

def cargar_tileset(path_relativo, tile_size):
    carpeta_actual = os.path.dirname(__file__)
    ruta_completa = os.path.join(carpeta_actual, path_relativo)
    if not os.path.exists(ruta_completa):
        raise FileNotFoundError(f"No se encontró la imagen: {ruta_completa}")
    
    try:
        imagen = pygame.image.load(ruta_completa).convert_alpha()
    except pygame.error as e:
        raise RuntimeError(f"No se pudo cargar la imagen {ruta_completa}: {e}")
    ancho, alto = imagen.get_size()
    tiles = []
    
    num_tiles_x = ancho // tile_size
    num_tiles_y = alto // tile_size

    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            tile = imagen.subsurface(rect)
            tiles.append(tile)
    
    return tiles
# Diccionario de tilesets por capa
tilesets = {
    "l_piso": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
    "l_paredes": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
    "l_objetos": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
    "l_roturs_en_las_paredes": cargar_tileset("imagenes/4bd1f88f-bae1-45cb-9eb2-ae60f831a400.png", TILE_SIZE),
    "l_decoraciones": cargar_tileset("imagenes/d5783a2d-84fa-433a-5e07-73cbb3197d00.png", TILE_SIZE),
    "l_fire": cargar_tileset("imagenes/45c9c5be-c636-42b7-62d6-b8a104bf6200.png", TILE_SIZE),
    "l_hitbox": cargar_tileset("imagenes/45c9c5be-c636-42b7-62d6-b8a104bf6200.png", TILE_SIZE),
}

layersData = {
    "l_piso": l_piso,
    "l_paredes": l_paredes,
    "l_objetos": l_objetos,
    "l_roturs_en_las_paredes": l_roturs_en_las_paredes,
    "l_decoraciones": l_decoraciones,
    "l_fire": l_fire,
}

def render_layer(superficie, tilesData, tileset):
    for y, fila in enumerate(tilesData):
        for x, symbol in enumerate(fila):
            if symbol != 0:
                tile_index = symbol - 1
                if 0 <= tile_index < len(tileset):
                    tile = tileset[tile_index]
                    superficie.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    print(f"Advertencia: Tile con índice {tile_index} no encontrado en el tileset. Posición: ({x}, {y})")

def generar_fondo():
    fondo = pygame.Surface((MAP_REAL_WIDTH, MAP_REAL_HEIGHT), pygame.SRCALPHA)
    for layer_name, tilesData in layersData.items():
        tileset = tilesets.get(layer_name)
        if tileset:
            render_layer(fondo, tilesData, tileset)
    return fondo

fondo_mapa = generar_fondo()

fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))


def generar_colisiones_escaladas(hitbox_matrix, tile_size, scale_factor, offset_x, offset_y):
    colisiones = []
    for y, fila in enumerate(hitbox_matrix):
        for x, valor in enumerate(fila):
            if valor == 1:
                rect_original = pygame.Rect(
                    x * tile_size, 
                    y * tile_size, 
                    tile_size, 
                    tile_size
                )
                
                rect_escalado = pygame.Rect(
                    offset_x + rect_original.x * scale_factor,
                    offset_y + rect_original.y * scale_factor,
                    rect_original.width * scale_factor,
                    rect_original.height * scale_factor
                )
                
                colisiones.append(rect_escalado)
    
    return colisiones

colisiones_escaladas = generar_colisiones_escaladas(
    l_hitbox_mapa_1, 
    TILE_SIZE, 
    SCALE_FACTOR, 
    OFFSET_X, 
    OFFSET_Y
)

puerta_1 = pygame.Rect(
    OFFSET_X + 10 * TILE_SIZE * SCALE_FACTOR,  # posicion x (10)
    OFFSET_Y + 1 * TILE_SIZE * SCALE_FACTOR,   # posición y del tile 8
    TILE_SIZE * 2 * SCALE_FACTOR,              # Ancho (2 tiles)
    TILE_SIZE * 2 * SCALE_FACTOR                   # 1 tile de alto
)