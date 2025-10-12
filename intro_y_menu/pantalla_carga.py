import pygame
import os
import sys
import time
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
pygame.init()


screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Pantalla de carga")
clock = pygame.time.Clock()


BASE_DIR = os.path.dirname(__file__)
ruta_fondo = os.path.join(BASE_DIR, "menu","assets", "carga.png")

fondo = pygame.image.load(ruta_fondo).convert()
fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

def get_font(size):
    return pygame.font.Font("intro_y_menu/menu/assets/nueva.otf", size)
font=get_font(25)
text_surface = font.render("PRESS ANY KEY TO START", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2+250))

def press_any_key_screen():
    start_time = time.time()
    show_text = True

    while True:
        screen.blit(fondo, (0, 0))

        # --- Control de parpadeo cada 0.5 segundos ---
        if time.time() - start_time > 0.5:
            show_text = not show_text
            start_time = time.time()

        if show_text:
            screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Detecta cualquier tecla
                return  # Sale de la pantalla de carga

        pygame.display.flip()
        clock.tick(60)

def main_menu():
    print("Entrando al menú...")  