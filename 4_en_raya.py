import pygame
import sys
import random

pygame.init()

# -------------------
# Configuración
# -------------------
ROWS, COLS = 6, 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
WIDTH, HEIGHT = COLS * SQUARE_SIZE, (ROWS + 1) * SQUARE_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4 en línea vs CPU")

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
clock = pygame.time.Clock()

# -------------------
# Dificultad CPU
# -------------------

CPU_DIFICULTAD = 10

# -------------------
# Funciones del tablero
# -------------------
def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(SCREEN, BLUE, (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            pygame.draw.circle(SCREEN, color, (c*SQUARE_SIZE + SQUARE_SIZE//2, (r+1)*SQUARE_SIZE + SQUARE_SIZE//2), RADIUS)
    pygame.display.update()

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r
    return -1

def drop_piece_animated(board, col, piece):
    target_row = get_next_open_row(board, col)
    x = col * SQUARE_SIZE + SQUARE_SIZE//2
    y = SQUARE_SIZE//2
    color = RED if piece == 1 else YELLOW
    while y < (target_row+1)*SQUARE_SIZE + SQUARE_SIZE//2:
        SCREEN.fill(BLACK)
        draw_board(board)
        pygame.draw.circle(SCREEN, color, (x, int(y)), RADIUS)
        pygame.display.update()
        y += 20
        clock.tick(FPS)
    board[target_row][col] = piece

def winning_move(board, piece):
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    return False

# -------------------
# Lógica del juego
# -------------------
def run_game(screen):
    board = create_board()
    game_over = False
    turn = 0
    font = pygame.font.SysFont(None, 50)
    cursor_col = COLS // 2

    while True:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        draw_board(board)

        x_cursor = cursor_col * SQUARE_SIZE + SQUARE_SIZE//2
        pygame.draw.circle(SCREEN, RED, (x_cursor, SQUARE_SIZE//2), RADIUS)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN and not game_over and turn == 0:
                if event.key == pygame.K_LEFT:
                    cursor_col = max(0, cursor_col - 1)
                elif event.key == pygame.K_RIGHT:
                    cursor_col = min(COLS - 1, cursor_col + 1)
                elif event.key == pygame.K_RETURN:
                    if is_valid_location(board, cursor_col):
                        drop_piece_animated(board, cursor_col, 1)
                        if winning_move(board, 1):
                            game_over = True
                            winner = "Jugador"
                        turn = 1

        # ---------------- CPU ----------------
        if turn == 1 and not game_over:
            pygame.time.delay(800)
            valid_cols = [c for c in range(COLS) if is_valid_location(board, c)]

            def can_win(board, piece, col):
                temp = [row[:] for row in board]
                if not is_valid_location(temp, col):
                    return False
                row = get_next_open_row(temp, col)
                temp[row][col] = piece
                return winning_move(temp, piece)

            col = random.choice(valid_cols)  # movimiento base

            # Dificultad media o difícil
            if CPU_DIFICULTAD >= 2:
                # Bloquear si el jugador puede ganar
                for c in valid_cols:
                    if can_win(board, 1, c):
                        col = c
                        break

            # Dificultad difícil
            if CPU_DIFICULTAD >= 3:
                # Jugar para ganar si puede
                for c in valid_cols:
                    if can_win(board, 2, c):
                        col = c
                        break

            drop_piece_animated(board, col, 2)
            if winning_move(board, 2):
                game_over = True
                winner = "CPU"
            turn = 0

        if game_over:
            draw_board(board)
            msg_txt = font.render(f"{winner} gana!", True, RED if winner=="Jugador" else YELLOW)
            SCREEN.blit(msg_txt, (WIDTH//2 - msg_txt.get_width()//2, HEIGHT//2 - msg_txt.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            return

# -------------------
# Main
# -------------------
def main():
    run_game(SCREEN)

if __name__ == "__main__":
    main()
