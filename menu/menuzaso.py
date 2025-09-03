import pygame
import sys
import os
from .button import Button
from .settings import settings_menu


def loading_screen(window):
    from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
    ANCHO_PANTALLA, ALTO_PANTALLA = window.get_size()
    clock = pygame.time.Clock()

    fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
    fondo.fill((0, 0, 0))

    pixel_size = 8
    bar_width = 600
    bar_height = 16
    bar_x = (ANCHO_PANTALLA - bar_width) // 2
    bar_y = ALTO_PANTALLA // 2
    progress = 0
    max_progress = 100

    try:
        font = pygame.font.Font(None, 24)
    except:
        font = pygame.font.SysFont("Courier New", 16)

    while progress <= max_progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if progress < max_progress:
            progress += 1

        window.blit(fondo, (0, 0))

        if progress == max_progress:
            loading_text = font.render("CARGADO", True, (0, 255, 0))
        else:
            loading_text = font.render("CARGANDO...", True, (255, 255, 255))

        text_rect = loading_text.get_rect(center=(ANCHO_PANTALLA // 2, bar_y - 40))
        window.blit(loading_text, text_rect)

        fill_pixels = int(bar_width * (progress / max_progress))
        pygame.draw.rect(window, (100, 100, 100), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)
        pygame.draw.rect(window, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))

        for x in range(0, fill_pixels, pixel_size):
            for y in range(0, bar_height, pixel_size):
                pygame.draw.rect(window, (0, 255, 0), (bar_x + x, bar_y + y, pixel_size, pixel_size))

        percent_text = font.render(f"{progress}%", True, (255, 255, 255))
        percent_rect = percent_text.get_rect(center=(ANCHO_PANTALLA // 2, bar_y + bar_height + 30))
        window.blit(percent_text, percent_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.time.wait(500)
    return True


import pygame
import sys
import os
from .button import Button
from .settings import settings_menu


def get_font(size):
    BASE_DIR = os.path.dirname(__file__)  # carpeta donde está este .py
    ruta_fuente = os.path.join(BASE_DIR, "assets", "font.ttf")
    return pygame.font.Font(ruta_fuente, size)


def menus():
    from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
    """Función para mostrar el menú principal del juego (solo con flechas)."""
    pygame.init()
    window = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("MENÚ")
    clock = pygame.time.Clock()
    BASE_DIR = os.path.dirname(__file__)

    # Fondo
    ruta_fondo = os.path.join(BASE_DIR, "assets", "fondo_titulo.png")
    if os.path.exists(ruta_fondo):
        fondo = pygame.image.load(ruta_fondo).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    else:
        fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        fondo.fill((50, 50, 50))

    # Botones (con las posiciones que ya tenías)
    ruta_start = os.path.join(BASE_DIR, "assets", "DEFINITIVO.png")
    ruta_exit = os.path.join(BASE_DIR, "assets", "salir.png")
    ruta_options = os.path.join(BASE_DIR, "assets", "options.png")

    start_button = Button(ruta_start if os.path.exists(ruta_start) else None,
                          (400, 500), scale=1.25, text=None)
    exit_button = Button(ruta_exit if os.path.exists(ruta_exit) else None,
                         (800, 500), scale=1.25, text=None)
    options_button = Button(ruta_options if os.path.exists(ruta_options) else None,
                            (1200, 40), scale=0.75, text=None)

    buttons = [start_button, exit_button, options_button]
    selected_index = 0
    buttons[selected_index].selected = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key in [pygame.K_UP, pygame.K_LEFT]:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    # Acción según el botón seleccionado
                    if buttons[selected_index] == start_button:
                        print("Iniciar juego")
                        return
                    elif buttons[selected_index] == exit_button:
                        pygame.quit()
                        sys.exit()
                    elif buttons[selected_index] == options_button:
                        pygame.event.clear()
                        settings_menu(window)
                        pygame.event.clear()

        # Dibujar fondo
        window.blit(fondo, (0, 0))

        # Actualizar y dibujar botones
        for i, btn in enumerate(buttons):
            btn.selected = (i == selected_index)
            btn.update()
            btn.draw(window)

        pygame.display.flip()
        clock.tick(60)
