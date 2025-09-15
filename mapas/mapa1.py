# mapa1_data.py
import pygame
import sys
import os
# Inicializar Pygame
pygame.init()
# Mismo contenido que pegaste antes, pero en sintaxis Python
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
  [1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1],
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
# Configuración de pantalla
DESIRED_SCREEN_WIDTH = 1280
DESIRED_SCREEN_HEIGHT = 720
TILE_SIZE = 16  # Cambiado a 16
MAP_WIDTH = 20
MAP_HEIGHT = 11
# Calcular tamaño real del mapa (con TILE_SIZE=16)
MAP_REAL_WIDTH = MAP_WIDTH * TILE_SIZE  # 20 * 16 = 320
MAP_REAL_HEIGHT = MAP_HEIGHT * TILE_SIZE  # 11 * 16 = 176
# Calcular factor de escalado para llenar la pantalla
SCALE_X = DESIRED_SCREEN_WIDTH / MAP_REAL_WIDTH  # 1280 / 320 = 4.0
SCALE_Y = DESIRED_SCREEN_HEIGHT / MAP_REAL_HEIGHT  # 720 / 176 ≈ 4.09
# Usar el mismo factor de escalado para ambos ejes para mantener la proporción
SCALE_FACTOR = min(SCALE_X, SCALE_Y)  # 4.0
# Calcular tamaño escalado
SCALED_WIDTH = int(MAP_REAL_WIDTH * SCALE_FACTOR)  # 320 * 4 = 1280
SCALED_HEIGHT = int(MAP_REAL_HEIGHT * SCALE_FACTOR)  # 176 * 4 = 704
# Calcular offset para centrar el mapa
OFFSET_X = (DESIRED_SCREEN_WIDTH - SCALED_WIDTH) // 2
OFFSET_Y = (DESIRED_SCREEN_HEIGHT - SCALED_HEIGHT) // 2
# Crear pantalla con el tamaño deseado
pantalla = pygame.display.set_mode((DESIRED_SCREEN_WIDTH, DESIRED_SCREEN_HEIGHT))
pygame.display.set_caption("Mapa estilo1 matris")
# Cargar tilesets
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
    
    # Calcular cuántos tiles completos hay en cada dimensión
    num_tiles_x = ancho // tile_size
    num_tiles_y = alto // tile_size
    
    print(f"Cargando tileset: {ruta_completa}")
    print(f"Tamaño de la imagen: {ancho}x{alto}")
    print(f"Tamaño del tile: {tile_size}x{tile_size}")
    print(f"Tiles a cargar: {num_tiles_x} x {num_tiles_y} = {num_tiles_x * num_tiles_y}")
    
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
# Diccionario de capas
layersData = {
    "l_piso": l_piso,
    "l_paredes": l_paredes,
    "l_objetos": l_objetos,
    "l_roturs_en_las_paredes": l_roturs_en_las_paredes,
    "l_decoraciones": l_decoraciones,
    "l_fire": l_fire,
}
# Renderizar una capa
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
# Generar fondo como en JS
def generar_fondo():
    fondo = pygame.Surface((MAP_REAL_WIDTH, MAP_REAL_HEIGHT), pygame.SRCALPHA)
    for layer_name, tilesData in layersData.items():
        tileset = tilesets.get(layer_name)
        if tileset:
            render_layer(fondo, tilesData, tileset)
    return fondo
# Generar fondo en tamaño original
fondo_mapa = generar_fondo()
# Escalar el mapa al tamaño deseado
fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

# Generar rects de colisión escalados
def generar_colisiones_escaladas(hitbox_matrix, tile_size, scale_factor, offset_x, offset_y):
    colisiones = []
    for y, fila in enumerate(hitbox_matrix):
        for x, valor in enumerate(fila):
            if valor == 1:  # Si hay colisión
                # Calcular posición y tamaño del tile original
                rect_original = pygame.Rect(
                    x * tile_size, 
                    y * tile_size, 
                    tile_size, 
                    tile_size
                )
                
                # Escalar el rect
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

def conseguir_puerta():
    return puerta_1

def conseguir_colisiones(fondo=None):
    return colisiones_escaladas

# Definir la puerta (ajusta la posición según tu mapa)
puerta_1 = pygame.Rect(
    OFFSET_X + 18 * TILE_SIZE * SCALE_FACTOR,  # Posición x del tile 18
    OFFSET_Y + 8 * TILE_SIZE * SCALE_FACTOR,   # Posición y del tile 8
    TILE_SIZE * 2 * SCALE_FACTOR,              # Ancho (2 tiles)
    TILE_SIZE * SCALE_FACTOR                   # Alto (1 tile)
)

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Limpiar pantalla
    pantalla.fill((0, 0, 0))
    
    # Dibujar el mapa escalado y centrado
    pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
    
    # Dibujar colisiones (para depuración)
    for colision in colisiones_escaladas:
        pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)  # Rojo = colisiones
    
    # Dibujar puerta (para depuración)
    pygame.draw.rect(pantalla, (0, 0, 255), puerta_1, 2)  # Azul = puerta
    
    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()