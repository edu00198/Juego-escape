# mapa3_data.py
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.jugador import Jugador

pygame.init()



l_decoracion = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,102,109,0,0,0,108,0,0,107,0,0,108,0],
   [0,0,0,0,0,0,0,126,133,0,0,0,132,0,0,131,0,0,132,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
l_decorative_cracks = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,2,0,0,0,3,0,1,28,0,30,0,0,0,0,0,0,0,0],
   [3,0,0,7,0,0,0,7,0,36,0,38,0,0,0,0,0,0,0,20],
   [0,0,0,0,0,0,0,0,0,44,0,46,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,2,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,49,0],
   [0,5,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [59,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,49,49,51,0,49,49,0,51,0,0,0,50,49,51,50,0,0,0]
]
l_fuego = [
   [0,0,1,2,0,0,0,1,2,0,0,0,0,0,36,37,38,0,0,0],
   [0,0,12,13,0,0,0,12,13,0,0,0,0,0,47,48,49,0,0,0],
   [0,0,23,24,0,0,0,23,24,0,0,0,0,0,58,59,60,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,1,2,0,0,0,1,2,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,12,13,0,0,0,12,13,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,23,24,0,0,0,23,24,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

l_paredes1_ =[
   [15,7,8,28,28,28,28,28,8,9,15,7,8,28,28,28,28,28,5,6],
   [28,20,21,41,0,0,41,41,21,22,28,20,21,0,0,41,0,0,18,19],
   [41,33,34,54,0,0,54,54,34,35,41,33,34,0,0,54,0,0,31,32],
   [54,46,47,0,0,0,0,0,47,48,54,46,47,0,0,0,0,0,0,14],
   [0,0,50,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [4,5,28,28,29,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [17,18,41,41,42,0,0,0,0,0,0,0,0,0,0,0,0,1,2,45],
   [30,31,54,54,55,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15],
   [43,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,45,15,15]
]
l_piso = [
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,285,274,274,274,274,274],
   [274,274,285,285,285,285,285,285,285,285,285,285,285,285,285,285,285,285,285,274],
   [285,285,285,299,285,285,285,285,285,285,285,285,285,285,299,285,80,285,285,274],
   [285,285,285,285,285,285,285,285,285,285,285,285,285,285,285,299,285,299,80,274],
   [274,274,274,274,285,285,285,285,285,285,285,285,285,285,80,285,285,80,285,274],
   [274,274,274,274,274,285,285,285,285,285,285,285,285,285,285,80,299,285,285,274],
   [274,274,274,274,285,285,80,285,285,285,299,285,285,285,285,285,285,285,285,274],
   [274,285,285,285,285,285,285,299,80,285,285,285,285,285,285,80,285,285,285,274],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274]
]
l_sombra_piso_2 = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,274,274,0,274,274,274,0],
   [0,0,288,274,274,132,274,288,274,0,0,0,274,274,288,132,274,288,274,0],
   [274,288,274,0,0,0,0,0,274,274,0,274,274,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,275,132,0,0,0,0,0,0],
   [0,0,0,0,0,274,274,132,274,274,274,274,275,274,0,0,0,0,0,0],
   [0,0,0,0,0,274,132,274,274,132,274,274,275,274,0,0,0,0,0,0],
   [0,0,0,0,0,274,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,274,132,274,274,288,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
l_sombra_piso = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,132,132,0,0,0,0,0,0,0,132,132,132,132,132,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,132,132,132,132,132,0,0],
   [0,0,121,145,145,145,145,145,122,132,0,132,121,145,145,145,145,145,145,0],
   [145,145,146,0,0,0,0,0,144,145,132,121,146,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,132,132,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,132,132,132,132,132,132,134,119,120,0,0,0,0,0,0],
   [0,0,0,0,0,121,145,145,145,145,145,145,145,146,0,0,0,0,0,0],
   [0,0,0,0,132,133,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,132,132,132,132,146,0,0,0,0,0,0,120,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
hitbox_mapa_4 = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,0,0,1,1],
  [1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1],
  [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1],
  [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
  [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1],
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

pantalla = None 

# ...existing code...
def cargar_tileset(path_relativo, tile_size):
    carpeta_actual = os.path.dirname(__file__)
    ruta_completa = os.path.normpath(os.path.join(carpeta_actual, path_relativo))

    # Preparar lista de rutas a probar (ruta solicitada y algunas alternativas útiles)
    alternativas = [
        ruta_completa,
        os.path.normpath(os.path.join(carpeta_actual, "paredes_mapa3.png")),
        os.path.normpath(os.path.join(carpeta_actual, path_relativo.replace("imagenes/", ""))),
        os.path.normpath(os.path.join(carpeta_actual, os.path.basename(path_relativo))),
    ]

    ruta_encontrada = None
    for ruta in alternativas:
        if os.path.exists(ruta):
            ruta_encontrada = ruta
            break

    if ruta_encontrada is None:
        raise FileNotFoundError(f"No se encontró ninguna de las rutas de imagen: {alternativas}")

    try:
        imagen = pygame.image.load(ruta_encontrada)
        # usar convert_alpha si la imagen tiene canal alpha, si no usar convert
        if imagen.get_alpha() is None:
            imagen = imagen.convert()
        else:
            imagen = imagen.convert_alpha()
    except pygame.error as e:
        raise RuntimeError(f"No se pudo cargar la imagen {ruta_encontrada}: {e}")

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
# ...existing code...
#assets\mapas\imagenes\4bd1f88f-bae1-45cb-9eb2-ae60f831a400.png
layersData = {
   "l_piso": l_piso,
   "l_sombra_piso": l_sombra_piso,
   "l_sombra_piso_2": l_sombra_piso_2,
   "l_paredes1_": l_paredes1_,
   "l_decorative_cracks": l_decorative_cracks,
   "l_decoracion": l_decoracion,
   "l_fuego": l_fuego,
}

tilesets = {
  "l_piso": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
  "l_sombra_piso": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
  "l_sombra_piso_2": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
  "l_paredes1_": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
  "l_decorative_cracks": cargar_tileset("imagenes/4bd1f88f-bae1-45cb-9eb2-ae60f831a400.png", TILE_SIZE),
  "l_decoracion": cargar_tileset("imagenes/d5783a2d-84fa-433a-5e07-73cbb3197d00.png", TILE_SIZE),
  "l_fuego": cargar_tileset("imagenes/45c9c5be-c636-42b7-62d6-b8a104bf6200.png", TILE_SIZE),
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
    hitbox_mapa_4, 
    TILE_SIZE, 
    SCALE_FACTOR, 
    OFFSET_X, 
    OFFSET_Y
)
# -------------------------
# Puertas / zonas importantes
# -------------------------
puerta_3_entrada = pygame.Rect(
    int(OFFSET_X + 0 * TILE_SIZE * SCALE_FACTOR),
    int(OFFSET_Y + 3 * TILE_SIZE * SCALE_FACTOR),
    int(1 * TILE_SIZE * SCALE_FACTOR),
    int(2 * TILE_SIZE * SCALE_FACTOR)
)
puerta_3_salida_al_mapa_4 = pygame.Rect(
    int(OFFSET_X + 16 * TILE_SIZE * SCALE_FACTOR),
    int(OFFSET_Y + 2 * TILE_SIZE * SCALE_FACTOR),
    int(2 * TILE_SIZE * SCALE_FACTOR),
    int(1 * TILE_SIZE * SCALE_FACTOR)
)

puerta_3_engranaje = pygame.Rect(
    int(OFFSET_X + 13 * TILE_SIZE * SCALE_FACTOR),
    int(OFFSET_Y + 2 * TILE_SIZE * SCALE_FACTOR),
    int(2 * TILE_SIZE * SCALE_FACTOR),
    int(1 * TILE_SIZE * SCALE_FACTOR)
)
puerta_3_cuatro_en_raya = pygame.Rect(
    int(OFFSET_X + 4 * TILE_SIZE * SCALE_FACTOR),
    int(OFFSET_Y + 2 * TILE_SIZE * SCALE_FACTOR),
    int(2 * TILE_SIZE * SCALE_FACTOR),
    int(1 * TILE_SIZE * SCALE_FACTOR)
)
