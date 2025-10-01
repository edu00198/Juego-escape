# mapa2_data.py
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from movimiento_jugador.jugador import Jugador

pygame.init()

l_fuego = [
   [0,0,0,0,0,0,0,12,13,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,13,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,13,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,12,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0]
]
l_objetos = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,109,0,0,0,0,110,0,0,0,111,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,109,111,0,0,0,0],
   [0,17,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,41,42,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,65,66,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
l_puertas2 = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,240,241,0,0,0,0,0,0,0,0,199,199,240,241,199,0],
   [0,0,0,0,253,254,0,0,0,0,0,0,0,0,212,212,253,254,212,0],
   [0,0,0,0,266,267,0,0,0,0,0,0,0,0,225,225,266,267,225,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
l_paredes = [
   [4,5,28,28,28,28,28,28,28,28,165,28,28,28,28,28,28,28,5,6],
   [17,18,41,41,41,41,41,279,280,41,211,41,41,279,280,41,277,278,18,19],
   [20,31,54,54,54,54,54,292,293,54,211,54,54,292,293,54,290,291,31,32],
   [33,0,0,0,0,0,0,0,0,0,185,0,0,0,0,0,0,0,0,14],
   [46,0,0,162,0,0,163,0,0,0,172,0,0,162,0,0,0,0,0,207],
   [0,0,0,175,0,0,176,0,0,0,185,0,0,175,0,0,0,0,0,220],
   [143,199,199,202,0,0,189,0,0,0,185,0,0,185,0,0,0,0,225,233],
   [16,212,212,215,0,0,237,0,0,0,237,0,0,237,0,0,0,0,0,14],
   [16,225,225,228,0,0,250,0,0,0,250,0,0,250,0,0,0,0,0,14],
   [16,0,0,0,0,0,263,0,0,0,263,0,0,263,0,0,0,0,0,14],
   [43,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,45]
]



l_piso = [
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,275,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,287,288,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274]
]


l_hitbox_mapa3 = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1],
  [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
  [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,0,0,0,1,0,0,1,1,1,1,1,1,1],
  [1,1,1,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1],
  [1,1,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1],
  [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

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
    "l_objetos": cargar_tileset("imagenes/d5783a2d-84fa-433a-5e07-73cbb3197d00.png", TILE_SIZE),
    "l_roturs_en_las_paredes": cargar_tileset("imagenes/4bd1f88f-bae1-45cb-9eb2-ae60f831a400.png", TILE_SIZE),
    "l_decoraciones": cargar_tileset("imagenes/d5783a2d-84fa-433a-5e07-73cbb3197d00.png", TILE_SIZE),
    "l_fire": cargar_tileset("imagenes/45c9c5be-c636-42b7-62d6-b8a104bf6200.png", TILE_SIZE),
    "l_hitbox": cargar_tileset("imagenes/45c9c5be-c636-42b7-62d6-b8a104bf6200.png", TILE_SIZE),
}

layersData = {
    "l_piso": l_piso,
    "l_paredes": l_paredes,
    "l_objetos": l_objetos,
    "l_puertas2": l_puertas2,
    "l_fuego": l_fuego,

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
    l_hitbox_mapa3, 
    TILE_SIZE, 
    SCALE_FACTOR, 
    OFFSET_X, 
    OFFSET_Y
)

puerta_3_entrada = pygame.Rect(
    OFFSET_X * 1 * TILE_SIZE * SCALE_FACTOR,  # posicion x (10)
    OFFSET_Y + 5 * TILE_SIZE * SCALE_FACTOR,   # posición y del tile 8
    TILE_SIZE * 1 * SCALE_FACTOR,              # Ancho 
    TILE_SIZE * 1 * SCALE_FACTOR               # alto
)
puerta_3_salida = pygame.Rect(
    OFFSET_X + 16 * TILE_SIZE * SCALE_FACTOR,  # columna inicial
    OFFSET_Y + 2 * TILE_SIZE * SCALE_FACTOR,   # fila inicial
    2 * TILE_SIZE * SCALE_FACTOR,              # ancho = 2 tiles
    1 * TILE_SIZE * SCALE_FACTOR               # alto = 2 tiles
)
