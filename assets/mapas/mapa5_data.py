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

l_paredes_exteriores = [
   [15,15,15,15,15,15,15,15,15,4,5,5,5,5,5,5,5,5,5,6],
   [0,0,0,0,0,0,0,15,15,10,11,18,18,18,18,18,18,18,18,19],
   [4,5,0,0,0,0,0,0,0,23,24,31,31,31,31,31,31,31,31,27],
   [17,18,15,15,0,0,0,0,0,36,37,0,0,0,0,0,0,0,0,40],
   [30,31,0,0,0,0,0,0,0,49,50,0,0,0,0,0,0,0,0,53],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [43,2,2,2,2,2,2,2,2,2,2,2,2,2,3,0,0,1,2,45],
   [15,15,15,15,15,15,15,15,15,15,15,15,15,15,16,0,0,14,15,15]
]
l_New_Layer_7 = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
collisions = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1]
]
l_roturas = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,7,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,122,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17],
   [23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,52,0,0,51,0,49,0,0,49,50,51,52,0,13,0,0,11,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,21,0,0,19,0,0]
]
l_sombra = [
   [0,0,132,132,0,132,132,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,132,132,132,132,132,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,132,132,132,0,0,0,0,0,0,0,0,0,145,0,0,0,0],
   [0,0,132,132,0,0,132,132,0,0,121,145,145,145,145,145,145,145,145,145],
   [0,0,132,132,0,0,132,132,132,132,133,0,0,0,0,0,0,0,0,0],
   [0,132,121,145,145,145,145,145,145,145,146,0,0,0,0,0,0,0,0,0],
   [0,288,133,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,132,133,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,274,133,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,132,0,0,0,0,0,0,0,0,0,0,0,0,119,119,119,119,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,132,132,0,0,0]
]
l_hitbox_js = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1]
]
l_uerta = [
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [15,15,15,15,15,15,15,15,15,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,28,28,28,28,28,28,28,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,41,41,279,280,41,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,54,54,292,293,54,0,0,0,299,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,286,0,0,0,0],
   [0,0,0,285,0,298,0,0,0,0,0,0,0,0,0,0,286,0,0,0],
   [0,0,0,0,0,0,0,285,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,299,0,299,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
l_piso_js = [
   [80,80,80,80,298,80,299,299,80,80,80,299,80,80,298,80,298,80,80,80],
   [80,286,80,80,299,299,80,80,299,286,80,80,298,298,80,80,80,80,80,80],
   [80,298,299,80,286,80,80,298,80,80,80,80,298,285,298,298,80,285,80,298],
   [299,80,299,80,285,285,80,80,299,80,299,80,80,298,299,80,80,80,80,298],
   [299,80,80,299,80,80,298,80,285,286,286,298,80,80,298,285,298,298,80,80],
   [80,298,80,298,80,80,299,80,286,80,80,80,299,80,298,285,80,298,80,80],
   [80,286,286,80,80,80,80,299,80,285,286,80,80,298,80,285,286,80,298,80],
   [299,80,80,80,298,298,80,80,80,298,299,298,80,299,299,299,286,80,80,80],
   [80,80,285,285,80,80,80,285,286,286,80,80,299,298,80,299,299,80,286,80],
   [80,298,298,80,80,285,285,286,80,80,298,80,299,286,286,286,298,299,80,80],
   [80,80,80,80,80,80,80,286,80,80,80,80,80,80,80,80,80,80,80,80]
]

# --- Tilesets para cada capa ---
def cargar_tileset(path_relativo, tile_size):
    carpeta_actual = os.path.dirname(__file__)
    ruta_completa = os.path.join(carpeta_actual, path_relativo)
    if not os.path.exists(ruta_completa):
        print(f"Advertencia: No se encontró la imagen: {ruta_completa}")
        # Crear una superficie vacía como fallback
        superficie = pygame.Surface((tile_size, tile_size))
        superficie.fill((128, 128, 128))  # Gris como indicador visual de error
        return [superficie]
    try:
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
    except Exception as e:
        print(f"Error cargando tileset {path_relativo}: {e}")
        # Crear una superficie vacía como fallback
        superficie = pygame.Surface((tile_size, tile_size))
        superficie.fill((128, 128, 128))  # Gris como indicador visual de error
        return [superficie]

# ...existing code...

layersData = {
    "l_piso_js": l_piso_js,                   # Piso (fondo)
    "l_sombra": l_sombra,                     # Sombras
    "l_roturas": l_roturas,                   # Roturas
    "l_paredes_exteriores": l_paredes_exteriores, # Paredes exteriores
    "l_New_Layer_7": l_New_Layer_7,           # Otra capa de paredes
    "l_uerta": l_uerta,                       # Puertas
    "collisions": collisions,                 # Colisiones (debug o lógica)
    "l_hitbox_js": l_hitbox_js                # Hitbox (debug o lógica)
}

IMAGENES_PATH = "imagenes/"


tilesets = {
    "l_piso_js": cargar_tileset(IMAGENES_PATH + "paredes.png", TILE_SIZE),
    "l_sombra": cargar_tileset(IMAGENES_PATH + "paredes.png", TILE_SIZE),
    "l_roturas": cargar_tileset(IMAGENES_PATH + "4bd1f88f-bae1-45cb-9eb2-ae60f831a400.png", TILE_SIZE),
    "l_paredes_exteriores": cargar_tileset(IMAGENES_PATH + "paredes.png", TILE_SIZE),
    "l_New_Layer_7": cargar_tileset(IMAGENES_PATH + "paredes.png", TILE_SIZE),
    "l_uerta": cargar_tileset(IMAGENES_PATH + "paredes.png", TILE_SIZE),
    "l_hitbox_js": cargar_tileset(IMAGENES_PATH + "tablero.png", TILE_SIZE),
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
    l_hitbox_js, 
    TILE_SIZE, 
    SCALE_FACTOR, 
    OFFSET_X, 
    OFFSET_Y
)

puerta_4_entrada = pygame.Rect(
    OFFSET_X + 15 * TILE_SIZE * SCALE_FACTOR,
    OFFSET_Y + 10 * TILE_SIZE * SCALE_FACTOR,
    TILE_SIZE * 2 * SCALE_FACTOR,
    TILE_SIZE * 1 * SCALE_FACTOR
)
puerta_4_salida = pygame.Rect(
    OFFSET_X + 18 * TILE_SIZE * SCALE_FACTOR,
    OFFSET_Y + 4 * TILE_SIZE * SCALE_FACTOR,
    TILE_SIZE * 2 * SCALE_FACTOR,
    TILE_SIZE * 1 * SCALE_FACTOR
)