import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Parámetros de pantalla y tiles ---
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

pygame.init()

# --- Matrices principales ---
hitbox = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
  [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
  [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
  [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
  [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1]
]
paredes = [
   [15,4,5,28,28,28,28,28,28,28,28,28,28,28,28,28,5,6,15,15],
   [15,17,18,41,41,41,41,41,41,41,41,41,41,41,41,41,18,19,15,15],
   [15,30,31,54,54,54,54,54,54,54,54,54,54,54,54,54,31,32,15,15],
   [15,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15],
   [15,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15],
   [15,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15],
   [15,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15],
   [15,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15],
   [15,43,2,2,2,2,2,2,2,2,3,0,0,1,2,2,2,45,15,15],
   [15,15,15,15,15,15,15,15,15,15,16,0,0,14,15,15,15,15,15,15],
   [15,15,15,15,15,15,15,15,15,15,16,0,0,14,15,15,15,15,15,15]
]
piso = [
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,288,274,274,274,274,274,288,274,288,274,288,288,274,288,288,274,274,274],
   [274,274,274,288,288,274,274,274,274,288,274,274,288,274,288,274,274,274,274,288],
   [274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,288,288,288,274,288,288,274,274,288,274,274,274,274],
   [274,288,274,274,288,288,274,274,274,274,274,274,274,274,288,274,274,288,274,288],
   [274,274,274,274,274,274,274,274,274,274,288,274,288,274,274,274,274,274,274,274],
   [274,274,274,274,274,274,274,288,274,274,288,274,274,274,274,274,274,274,274,274],
   [274,288,274,274,274,274,274,274,274,274,288,274,274,288,274,274,274,274,288,274],
   [274,274,274,274,288,274,274,274,274,288,274,274,274,274,274,274,288,274,274,274],
   [274,274,274,274,274,274,274,274,274,288,274,274,274,274,274,274,274,274,274,274]
]


# --- Tilesets para cada capa ---
def cargar_tileset(path_relativo, tile_size):
    carpeta_actual = os.path.dirname(__file__)
    ruta_completa = os.path.join(carpeta_actual, path_relativo)
    if not os.path.exists(ruta_completa):
        raise FileNotFoundError(f"No se encontró la imagen: {ruta_completa}")
    imagen = pygame.image.load(ruta_completa).convert_alpha()
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

layersData = {
    "piso": piso,
    "paredes": paredes,
    "hitbox": hitbox,       # Hitbox (debug o lógica)
}

tilesets = {
  "piso": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
  "paredes": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
  "hitbox": cargar_tileset("imagenes/paredes.png", TILE_SIZE),
}

# ...resto del código igual...

    

def render_layer(superficie, tilesData, tileset):
    
    for y, fila in enumerate(tilesData):
        for x, symbol in enumerate(fila):
            
            if symbol != 0:
                tile_index = symbol - 1
                if 0 <= tile_index < len(tileset):
                    tile = tileset[tile_index]
                    superficie.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
                    print(f"-------------------- symbol={symbol}, tile_index={symbol - 1}, tileset size={len(tileset)}")

                else:
                    print(f"Advertencia: Tile con índice {tile_index} no encontrado en el tileset. Posición: ({x}, {y})")
                print(f"symbol={symbol}, tile_index={tile_index}, len(tileset)={len(tileset)}")
                print(f" symbol={symbol}, tile_index={symbol - 1}, tileset size={len(tileset)}")

                

def generar_fondo():
    fondo = pygame.Surface((MAP_REAL_WIDTH, MAP_REAL_HEIGHT), pygame.SRCALPHA)
    for layer_name, tilesData in layersData.items():
        if layer_name != "hitbox":  # 👈 Evita dibujar la hitbox
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
    hitbox, 
    TILE_SIZE, 
    SCALE_FACTOR,
    OFFSET_X,
    OFFSET_Y
)

puerta_4 = pygame.Rect(
    OFFSET_X + 11 * TILE_SIZE * SCALE_FACTOR,
    OFFSET_Y + 10 * TILE_SIZE * SCALE_FACTOR,
    TILE_SIZE * 2 * SCALE_FACTOR,
    TILE_SIZE * 1 * SCALE_FACTOR
)
