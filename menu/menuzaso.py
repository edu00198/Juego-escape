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


def get_font(size):
    BASE_DIR = os.path.dirname(__file__)  # carpeta donde está este .py
    ruta_fuente = os.path.join(BASE_DIR, "assets", "font.ttf")
    return pygame.font.Font(ruta_fuente, size)


def menus():
    from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
    """Función para mostrar el menú principal del juego."""
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

    # Rutas de imágenes
    ruta_start = os.path.join(BASE_DIR, "assets", "DEFINITIVO.png")
    ruta_exit = os.path.join(BASE_DIR, "assets", "salir.png")
    ruta_options_normal = os.path.join(BASE_DIR, "assets", "options.png")
    ruta_options_hover = os.path.join(BASE_DIR, "assets", "algo.png")

    # Crear botones
    start_button = Button(ruta_start, (400, 500), scale=1.25, text=None)
    exit_button = Button(ruta_exit, (800, 500), scale=1.25, text=None)
    options_button = Button(ruta_options_normal, (1200, 40), scale=0.75, text=None)

    # Cargar imágenes como Surface
    img_options_normal = pygame.image.load(ruta_options_normal).convert_alpha()
    img_options_hover = pygame.image.load(ruta_options_hover).convert_alpha()

    # Posiciones iniciales
    hover_anterior = False
    offset_hover = -50  # Desplazamiento hacia la izquierda
    original_pos = options_button.rect.topleft  # Guarda posición original

    while True:
        # Dibujar elementos
        window.blit(fondo, (0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        MENU_TEXT = get_font(100).render("", True, "#cfd8dc")
        MENU_TEXT_2 = get_font(100).render("", True, "#cfd8dc")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 125))
        MENU_RECT_2 = MENU_TEXT_2.get_rect(center=(640, 250))

        if start_button.is_clicked(events):
            print("Iniciar juego")
            return

        if exit_button.is_clicked(events):
            pygame.quit()
            sys.exit()

        if options_button.is_clicked(events):
            pygame.event.clear()
            settings_menu(window)
            pygame.event.clear()

        # Hover sobre botón de opciones
        if options_button.rect.collidepoint(pygame.mouse.get_pos()):
            if not hover_anterior:
                options_button.original_image = img_options_hover
                options_button.rect.topleft = (original_pos[0] + offset_hover, original_pos[1])
                hover_anterior = True
        else:
            if hover_anterior:
                options_button.original_image = img_options_normal
                options_button.rect.topleft = original_pos
                hover_anterior = False

        window.blit(MENU_TEXT, MENU_RECT)
        window.blit(MENU_TEXT_2, MENU_RECT_2)

        start_button.update()
        exit_button.update()
        options_button.update()

        start_button.draw(window)
        exit_button.draw(window)
        options_button.draw(window)

        pygame.display.flip()
        clock.tick(60)