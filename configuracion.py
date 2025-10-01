""" configuracion.py
este archivo contiene la configuracion de movimiento del jugador,
incluyendo las dimensiones de la ventana del juego, los colores y la velocidad del jugador.
"""


from assets.mapas.fondo import mapa1_abierta,mapa1_cerrada,m1_opciones,mapa2,m2_opciones

m1_abierta=mapa1_abierta
m1_cerrado=mapa1_cerrada
mapa2 = mapa2
m1_opciones=m1_opciones
m2_opciones=m2_opciones

# game_state.py
class GameState:
    def __init__(self):
        self.mapa_actual = "mapa1"

mapa_actual = GameState()

# Colores en formato RGB
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)

# Velocidad con la que se moverá el jugador
VELOCIDAD_JUGADOR = 4
# Velocidad de animación: número más alto = más lento
VELOCIDAD_ANIMACION = 11  # por defecto
# tamaño del jugador
ESCALA_JUGADOR = 3  # 1 = tamaño original, 2 = el doble, etc.

#dimensiones de la ventana del juego
ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720

# Colores
BLANCO = (255, 255, 255)


FPS = 60

# Escala del jugador

ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720

TILE_SIZE = 16
MAP_WIDTH = 20
MAP_HEIGHT = 11
SCREEN_WIDTH = MAP_HEIGHT * TILE_SIZE
SCREEN_HEIGHT = MAP_WIDTH * TILE_SIZE