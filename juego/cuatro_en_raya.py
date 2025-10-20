import pygame
import sys
import random
import math
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
pygame.init()

# -------------------
# Configuración
# -------------------
ROWS, COLS = 6, 7
SQUARE_SIZE = 100
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

FPS = 60
clock = pygame.time.Clock()

# -------------------
# Funciones del tablero
# -------------------
def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_static_board(board, board_x, board_y):
    """Dibuja solo el tablero y las fichas ya colocadas, sin el cursor."""
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(SCREEN, BLUE, (board_x + c*SQUARE_SIZE, board_y + r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            pygame.draw.circle(SCREEN, color, 
                              (board_x + c*SQUARE_SIZE + SQUARE_SIZE//2, 
                               board_y + r*SQUARE_SIZE + SQUARE_SIZE//2), RADIUS)

def draw_board(board, cursor_col):
    """Dibuja toda la escena: tablero, fichas y el cursor del jugador."""
    # Calcular la posición del tablero para centrarlo
    board_width = COLS * SQUARE_SIZE
    board_height = (ROWS + 1) * SQUARE_SIZE
    board_x = (WIDTH - board_width) // 2
    board_y = (HEIGHT - board_height) // 2 + SQUARE_SIZE // 2
    
    # Dibujar el tablero estático
    draw_static_board(board, board_x, board_y)
    
    # Dibujar cursor del jugador solo si es su turno
    if cursor_col != -1:
        pygame.draw.circle(SCREEN, RED, 
                          (board_x + cursor_col * SQUARE_SIZE + SQUARE_SIZE//2, 
                           board_y - SQUARE_SIZE//2), RADIUS)
    
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
    x = board_x + col * SQUARE_SIZE + SQUARE_SIZE//2
    y = board_y - SQUARE_SIZE // 2 # Posición inicial de la animación
    color = RED if piece == 1 else YELLOW
    
    # Bucle de animación
    while y < board_y + target_row*SQUARE_SIZE + SQUARE_SIZE//2:
        SCREEN.fill(BLACK)
        # Dibujar solo el tablero estático, SIN el cursor
        draw_static_board(board, board_x, board_y)
        # Dibujar la ficha que está cayendo
        pygame.draw.circle(SCREEN, color, (x, int(y)), RADIUS)
        pygame.display.update()
        y += 15  # Velocidad de caída
        clock.tick(FPS)
        
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
    
    # Cargar imagen de fondo (descomenta la siguiente línea cuando tengas la imagen)
    # fondo = pygame.image.load("fondo.png").convert()
    # fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    
    while True:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        
        # Dibujar fondo si está disponible
        # SCREEN.blit(fondo, (0, 0))
        
        # Dibujar el tablero y el cursor (si es el turno del jugador)
        board_x, board_y = draw_board(board, cursor_col if turn == 0 else -1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not game_over and turn == 0:
                if event.key == pygame.K_LEFT:
                    cursor_col = max(0, cursor_col - 1)
                elif event.key == pygame.K_RIGHT:
                    cursor_col = min(COLS - 1, cursor_col + 1)
                elif event.key == pygame.K_RETURN:
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
            draw_board(board, -1) # Dibujar tablero final sin cursor
            draw_winning_line(board_x, board_y, winning_line)
            msg_txt = font.render(f"{winner} gana!", True, RED if winner=="Jugador" else YELLOW)
            SCREEN.blit(msg_txt, (WIDTH//2 - msg_txt.get_width()//2, 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
        
        pygame.display.update()