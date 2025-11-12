import pygame
import sys
import random
import math
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
from juego.menu_pausa import pause_menu
pygame.init()

# -------------------
# Configuración
# -------------------
ROWS, COLS = 6, 7
SQUARE_SIZE = 100
PIECE_SIZE = int(SQUARE_SIZE * 0.8)  # Tamaño consistente para todas las fichas
RADIUS = SQUARE_SIZE // 2 - 5

# Resolución de 1280x720
WIDTH= ANCHO_PANTALLA
HEIGHT= ALTO_PANTALLA
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4 en Línea")

# Colores
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# --- después de crear SCREEN y antes del loop ---
USE_PIECE_IMAGES = True

try:
    TABLERO_IMG = pygame.image.load("intro_y_menu/menu/assets/tablero.png").convert_alpha()
    print("✓ Tablero cargado correctamente")
except Exception as e:
    print(f"✗ Error al cargar tablero: {e}")
    TABLERO_IMG = None
    USE_PIECE_IMAGES = False

try:
    ficha_r = pygame.image.load("intro_y_menu/menu/assets/ficha_roja.png").convert_alpha()
    ficha_a = pygame.image.load("intro_y_menu/menu/assets/ficha_amarilla.png").convert_alpha()
    print("✓ Fichas cargadas correctamente")
except Exception as e:
    print(f"✗ Error al cargar fichas: {e}")
    ficha_r = None
    ficha_a = None
    USE_PIECE_IMAGES = False



FPS = 60
clock = pygame.time.Clock()

# -------------------
# Funciones del tablero
# -------------------
def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_static_board(board, board_x, board_y):
    board_width = COLS * SQUARE_SIZE
    board_height = (ROWS + 1) * SQUARE_SIZE
    # Si existe la imagen del tablero, escalar y blitear; si no, dibujar un fallback
    if TABLERO_IMG is not None:
        # Calcular el ratio de aspecto original de la imagen
        img_ratio = TABLERO_IMG.get_width() / TABLERO_IMG.get_height()
        # Decidir si ajustar por ancho o por alto para mantener proporción
        if board_width / board_height > img_ratio:
            # Ajustar por altura
            new_height = board_height
            new_width = int(new_height * img_ratio)
            x_offset = board_x + (board_width - new_width) // 2
            tablero_scaled = pygame.transform.smoothscale(TABLERO_IMG, (new_width, new_height))
            SCREEN.blit(tablero_scaled, (x_offset, board_y))
            # Actualizar board_x para alinear las fichas con el tablero
            board_x = x_offset
        else:
            # Ajustar por ancho
            new_width = board_width
            new_height = int(new_width / img_ratio)
            y_offset = board_y + (board_height - new_height) // 2
            tablero_scaled = pygame.transform.smoothscale(TABLERO_IMG, (new_width, new_height))
            SCREEN.blit(tablero_scaled, (board_x, y_offset))
            # Actualizar board_y para alinear las fichas con el tablero
            board_y = y_offset
    else:
        pygame.draw.rect(SCREEN, BLUE, (board_x, board_y, board_width, board_height))
        # Dibujar 'huecos' negros para las casillas
        for c_h in range(COLS):
            for r_h in range(ROWS):
                cx = board_x + c_h * SQUARE_SIZE + SQUARE_SIZE // 2
                cy = board_y + r_h * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(SCREEN, BLACK, (cx, cy), RADIUS)

    # Dibujar fichas ya colocadas: preferir imágenes PNG, si no están disponibles usar círculos
    piece_size = PIECE_SIZE
    use_images = USE_PIECE_IMAGES and ficha_r is not None and ficha_a is not None

    if use_images:
        try:
            ficha_r_scaled = pygame.transform.smoothscale(ficha_r, (piece_size, piece_size))
            ficha_a_scaled = pygame.transform.smoothscale(ficha_a, (piece_size, piece_size))
        except Exception as e:
            use_images = False

    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 1 or board[r][c] == 2:
                draw_x = board_x + c * SQUARE_SIZE + (SQUARE_SIZE - piece_size) // 2
                draw_y = board_y + r * SQUARE_SIZE + (SQUARE_SIZE - piece_size) // 2
                
                if use_images:
                    try:
                        if board[r][c] == 1:
                            SCREEN.blit(ficha_r_scaled, (draw_x, draw_y))
                        else:
                            SCREEN.blit(ficha_a_scaled, (draw_x, draw_y))
                    except Exception as e:
                        # Fallback a círculos si hay error
                        color = RED if board[r][c] == 1 else YELLOW
                        pygame.draw.circle(SCREEN, color, 
                                        (draw_x + piece_size//2, draw_y + piece_size//2), 
                                        int(piece_size * 0.4))
                else:
                    color = RED if board[r][c] == 1 else YELLOW
                    pygame.draw.circle(SCREEN, color, 
                                    (draw_x + piece_size//2, draw_y + piece_size//2), 
                                    int(piece_size * 0.4))
    
    return board_x, board_y

def draw_board(board, cursor_col, board_x, board_y):
    # Usar draw_static_board para pintar el tablero y las fichas
    board_x, board_y = draw_static_board(board, board_x, board_y)

    # Dibujar previsualización de dónde caería la ficha (pieza fantasma)
    if cursor_col != -1:
        next_row = get_next_open_row(board, cursor_col)
        # Si la columna está llena, mostrar el cursor arriba; si no, mostrar dentro del tablero en la fila objetivo
        if next_row == -1:
            draw_y = board_y - SQUARE_SIZE // 2 - PIECE_SIZE // 2
        else:
            draw_y = board_y + next_row * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
        
        # Usar la MISMA fórmula de centrado que draw_static_board
        draw_x = board_x + cursor_col * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2

        # Dibujar la imagen con transparencia si existe, si no dibujar un círculo semitransparente
        if USE_PIECE_IMAGES and ficha_r is not None:
            try:
                ghost = pygame.transform.smoothscale(ficha_r, (PIECE_SIZE, PIECE_SIZE)).copy()
                ghost.set_alpha(140)
                SCREEN.blit(ghost, (draw_x, draw_y))
            except Exception:
                s = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 0, 0, 140), (PIECE_SIZE//2, PIECE_SIZE//2), int(PIECE_SIZE*0.4))
                SCREEN.blit(s, (draw_x, draw_y))
        else:
            s = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 0, 0, 140), (PIECE_SIZE//2, PIECE_SIZE//2), int(PIECE_SIZE*0.4))
            SCREEN.blit(s, (draw_x, draw_y))

    return board_x, board_y


def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r
    return -1

def drop_piece_animated(board, col, piece, board_x, board_y):
    """Hace que la ficha caiga animada hasta su posición final."""
    target_row = get_next_open_row(board, col)
    
    # Si columna llena, salir (seguridad)
    if target_row == -1:
        return
    
    # Bucle de animación
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        SCREEN.fill(BLACK)
        # Dibujar solo el tablero estático, SIN el cursor, y obtener coordenadas ajustadas
        adj_board_x, adj_board_y = draw_static_board(board, board_x, board_y)
        
        # Calcular posición actual de la ficha
        x = adj_board_x + col * SQUARE_SIZE + SQUARE_SIZE//2
        y_current = adj_board_y + target_row * SQUARE_SIZE + SQUARE_SIZE//2
        
        # Posición inicial (arriba del tablero)
        if not hasattr(drop_piece_animated, 'y_anim'):
            drop_piece_animated.y_anim = adj_board_y - SQUARE_SIZE // 2
        
        # Dibujar la ficha que está cayendo
        piece_size = PIECE_SIZE
        use_images = USE_PIECE_IMAGES and ((piece == 1 and ficha_r is not None) or (piece == 2 and ficha_a is not None))
        if use_images:
            if piece == 1:
                ficha_scaled = pygame.transform.smoothscale(ficha_r, (piece_size, piece_size))
            else:
                ficha_scaled = pygame.transform.smoothscale(ficha_a, (piece_size, piece_size))
            draw_x = int(x) - piece_size // 2
            draw_y = int(drop_piece_animated.y_anim) - piece_size // 2
            SCREEN.blit(ficha_scaled, (draw_x, draw_y))
        else:
            pygame.draw.circle(SCREEN, RED if piece == 1 else YELLOW, (int(x), int(drop_piece_animated.y_anim)), RADIUS)

        pygame.display.update()
        
        # Si llegó a la posición final, salir del bucle
        if drop_piece_animated.y_anim >= y_current:
            break
        
        drop_piece_animated.y_anim += 15  # Velocidad de caída
        clock.tick(FPS)
    
    # Limpiar el atributo temporal
    if hasattr(drop_piece_animated, 'y_anim'):
        delattr(drop_piece_animated, 'y_anim')
    
    # Una vez que termina la animación, actualizar el tablero
    board[target_row][col] = piece

def winning_move(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return [(r, c+i) for i in range(4)]
    # Vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return [(r+i, c) for i in range(4)]
    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return [(r-i, c+i) for i in range(4)]
    # Diagonal \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return [(r+i, c+i) for i in range(4)]
    return None

def draw_winning_line(board_x, board_y, positions):
    """Dibuja una línea sobre las fichas ganadoras."""
    if len(positions) < 2:
        return
    
    start_pos = (board_x + positions[0][1] * SQUARE_SIZE + SQUARE_SIZE//2,
                board_y + positions[0][0] * SQUARE_SIZE + SQUARE_SIZE//2)
    end_pos = (board_x + positions[-1][1] * SQUARE_SIZE + SQUARE_SIZE//2,
              board_y + positions[-1][0] * SQUARE_SIZE + SQUARE_SIZE//2)
    
    pygame.draw.line(SCREEN, GREEN, start_pos, end_pos, 10)

def cpu_move(board):
    """Implementa una estrategia de CPU más difícil."""
    # 1. Verificar si la CPU puede ganar
    for c in range(COLS):
        if is_valid_location(board, c):
            temp_board = [row[:] for row in board]
            row = get_next_open_row(temp_board, c)
            temp_board[row][c] = 2
            if winning_move(temp_board, 2):
                return c
    
    # 2. Verificar si necesita bloquear al jugador
    for c in range(COLS):
        if is_valid_location(board, c):
            temp_board = [row[:] for row in board]
            row = get_next_open_row(temp_board, c)
            temp_board[row][c] = 1
            if winning_move(temp_board, 1):
                return c
    
    # 3. Preferir el centro
    if is_valid_location(board, COLS//2):
        return COLS//2
    
    # 4. Elegir una columna aleatoria válida
    valid_cols = [c for c in range(COLS) if is_valid_location(board, c)]
    return random.choice(valid_cols)

# -------------------
# Juego principal
# -------------------
def inicio_juego():
    board = create_board()
    game_over = False
    turn = 0  # 0: jugador, 1: CPU
    cursor_col = COLS // 2  # Posición inicial del cursor
    font = pygame.font.SysFont(None, 50)
    
    # Calcular las coordenadas del tablero UNA SOLA VEZ y mantenerlas constantes
    board_width = COLS * SQUARE_SIZE
    board_height = (ROWS + 1) * SQUARE_SIZE
    board_x = (WIDTH - board_width) // 2
    board_y = (HEIGHT - board_height) // 4
    
    # Cargar imagen de fondo (descomenta la siguiente línea cuando tengas la imagen)
    # fondo = pygame.image.load("fondo.png").convert()
    # fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    
    while True:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        
        # Dibujar fondo si está disponible
        # SCREEN.blit(fondo, (0, 0))
        
        # Dibujar el tablero (devuelve coordenadas ajustadas que se ignoran)
        _, _ = draw_board(board, cursor_col if turn == 0 else -1, board_x, board_y)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Abrir menú de pausa; minijuego no guarda estado por defecto
                    pause_menu(SCREEN, mapa_actual=4, state=None)
                elif not game_over and turn == 0:
                    if event.key == pygame.K_LEFT:
                        cursor_col = max(0, cursor_col - 1)
                    elif event.key == pygame.K_RIGHT:
                        cursor_col = min(COLS - 1, cursor_col + 1)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if is_valid_location(board, cursor_col):
                            drop_piece_animated(board, cursor_col, 1, board_x, board_y)
                            win_positions = winning_move(board, 1)
                            if win_positions:
                                game_over = True
                                winner = "Jugador"
                                winning_line = win_positions
                            else:
                                turn = 1
        
        # Movimiento de la CPU
        if turn == 1 and not game_over:
            pygame.time.delay(500) 
            col = cpu_move(board)
            if is_valid_location(board, col):
                drop_piece_animated(board, col, 2, board_x, board_y)
                win_positions = winning_move(board, 2)
                if win_positions:
                    game_over = True
                    winner = "CPU"
                    winning_line = win_positions
                else:
                    turn = 0
                    # ELIMINADA LA LÍNEA QUE REINICIABA EL CURSOR
        
        # Fin de partida
        if game_over:
            SCREEN.fill(BLACK)
            draw_static_board(board, board_x, board_y)
            msg_txt = font.render(f"{winner} gana!", True, RED if winner=="Jugador" else YELLOW)
            SCREEN.blit(msg_txt, (WIDTH//2 - msg_txt.get_width()//2, 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            # Return True if player won, False if CPU won
            return winner == "Jugador"
        
        pygame.display.update()