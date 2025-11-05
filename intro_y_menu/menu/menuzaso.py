import pygame
import sys
import os
import fnmatch
from .button import Button
from .settings import settings_menu
from juego.save_system import load_game, list_saves, delete_save
from juego import mapa_1

BASE_RES = (1280, 720)
base_surface = pygame.Surface(BASE_RES)
fullscreen = False


def aplicar_resolucion(window, nueva_res):
    global fullscreen

    if nueva_res == "PANTALLA COMPLETA":
        fullscreen = True
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        ancho, alto = info.current_w, info.current_h
    else:
        fullscreen = False
        ancho, alto = map(int, nueva_res.split("x"))
        window = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)

    print(f"✅ Resolución aplicada: {ancho}x{alto} | fullscreen={fullscreen}")
    return window, ancho, alto


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


def select_load_slot(window):
    """
    Submenú para seleccionar el slot de carga.
    Permite eliminar un slot con la tecla R (libera el slot).
    """
    from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
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

    # obtener raw_slots (lo que devuelva list_saves)
    try:
        raw_slots = list_saves() or []
    except Exception:
        raw_slots = []

    # construir lista booleana de existencia por slot (1..5)
    exists = [False] * 5
    for i in range(1, 6):
        try:
            exists[i-1] = i in raw_slots
        except Exception:
            exists[i-1] = False

    # Mostrar instrucciones para eliminar
    instructions_font = pygame.font.Font(None, 24)
    instructions_surf = instructions_font.render("Presiona 'R' para eliminar el slot seleccionado", True, (255, 255, 255))
    instructions_rect = instructions_surf.get_rect(center=(ANCHO_PANTALLA // 2, 150))

    # crear botones con texto dinámico
    buttons = []
    font = pygame.font.Font(None, 36)
    for i in range(1, 6):
        text = f"Slot {i}" + (" (Guardado)" if exists[i-1] else "")
        text_surf = font.render(text, True, (255, 255, 255))
        btn = Button(text_surf, (ANCHO_PANTALLA // 2, 300 + (i-1) * 80))
        buttons.append(btn)

    back_button = Button(None, (ANCHO_PANTALLA // 2, 300 + 5 * 80), scale=1.0, text="Volver")
    buttons.append(back_button)

    selected_index = 0
    buttons[selected_index].selected = True

    # Mensajes temporales en pantalla (texto, tiempo_inicio, duracion_ms)
    message = None
    message_start = 0
    message_dur = 1500  # ms

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
                    if selected_index < 5:  # Slots 1-5
                        return selected_index + 1
                    else:  # Back
                        return None

                # --- ELIMINAR SLOT CON R ---
                elif event.key == pygame.K_r:
                    if selected_index < 5:  # Solo para slots
                        target_slot = selected_index + 1
                        if exists[target_slot - 1]:
                            deleted = False
                            try:
                                deleted = delete_save(target_slot)
                            except Exception as e:
                                print(f"Error al eliminar slot {target_slot}: {e}")
                                deleted = False

                            # refrescar existencia usando list_saves
                            try:
                                raw_slots = list_saves() or []
                            except Exception:
                                raw_slots = []
                            for i in range(1, 6):
                                exists[i-1] = i in raw_slots

                            # actualizar textos de botones
                            for idx in range(5):
                                txt = f"Slot {idx+1}" + (" (Guardado)" if exists[idx] else "")
                                txt_surf = font.render(txt, True, (255, 255, 255))
                                buttons[idx].image = txt_surf
                                buttons[idx].rect = buttons[idx].image.get_rect(center=(ANCHO_PANTALLA // 2, 300 + idx * 80))

                            if deleted:
                                message = f"Slot {target_slot} eliminado"
                                message_start = pygame.time.get_ticks()
                            else:
                                message = f"No se pudo eliminar slot {target_slot}"
                                message_start = pygame.time.get_ticks()
                        else:
                            message = f"Slot {target_slot} está vacío"
                            message_start = pygame.time.get_ticks()

        window.blit(fondo, (0, 0))

        # Dibujar instrucciones
        window.blit(instructions_surf, instructions_rect)

        # Dibujar título
        font_title = pygame.font.Font(None, 48)
        title_surf = font_title.render("Seleccionar Slot de Carga", True, (255, 255, 255))
        window.blit(title_surf, (ANCHO_PANTALLA // 2 - title_surf.get_width() // 2, 200))

        for i, btn in enumerate(buttons):
            btn.selected = (i == selected_index)
            btn.update()
            btn.draw(window)

        # Mostrar mensaje temporal si existe
        if message:
            now = pygame.time.get_ticks()
            if now - message_start <= message_dur:
                msg_font = pygame.font.Font(None, 30)
                msg_surf = msg_font.render(message, True, (255, 100, 100))
                window.blit(msg_surf, (ANCHO_PANTALLA // 2 - msg_surf.get_width() // 2, 300 + 5 * 80 + 50))
            else:
                message = None

        pygame.display.flip()
        clock.tick(60)


def game_selection_menu(window):
    """Menú para seleccionar nueva partida o cargar partida."""
    from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
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

    # Botones
    new_game_button = Button(None, (ANCHO_PANTALLA // 2, 400), scale=1.0, text="Nueva Partida")
    load_game_button = Button(None, (ANCHO_PANTALLA // 2, 500), scale=1.0, text="Cargar Partida")
    back_button = Button(None, (ANCHO_PANTALLA // 2, 600), scale=1.0, text="Volver")

    buttons = [new_game_button, load_game_button, back_button]
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
                    if buttons[selected_index] == new_game_button:
                        print("Nueva partida")
                        mapa_1.ejecutar_mapa1()
                        return
                    elif buttons[selected_index] == load_game_button:
                        slot = select_load_slot(window)
                        if slot:
                            state = load_game(slot)
                            if state:
                                # Cargar el mapa correspondiente basado en el estado
                                mapa = state.get('mapa')
                                if mapa == 'mapa1':
                                    mapa_1.ejecutar_mapa1_con_estado(state)
                                elif mapa == 'mapa2':
                                    from juego import mapa_2
                                    mapa_2.ejecutar_mapa2_con_estado(state)
                                elif mapa == 'mapa3':
                                    from juego import mapa_3
                                    mapa_3.ejecutar_mapa3_con_estado(state)
                                elif mapa == 'mapa4':
                                    from juego import mapa_3_2
                                    mapa_3_2.ejecutar_mapa3_2_con_estado(state)
                                elif mapa == 'mapa5':
                                    from juego import mapa_5
                                    mapa_5.ejecutar_mapa5_con_estado(state)
                                else:
                                    print(f"[ERROR] Mapa no reconocido: {mapa}")
                            else:
                                print("[ERROR] No se pudo cargar el estado del juego")
                        return
                    elif buttons[selected_index] == back_button:
                        return

        window.blit(fondo, (0, 0))

        # Actualizar y dibujar botones
        for i, btn in enumerate(buttons):
            btn.selected = (i == selected_index)
            btn.update()
            btn.draw(window)

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
    BASE_DIR = os.path.dirname(__file__)
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
                        game_selection_menu(window)
                    elif buttons[selected_index] == exit_button:
                        pygame.quit()
                        sys.exit()
                    elif buttons[selected_index] == options_button:
                        pygame.event.clear()
                        settings_menu(window)
                        pygame.event.clear()

        window.blit(fondo, (0, 0))

        # Actualizar y dibujar botones
        for i, btn in enumerate(buttons):
            btn.selected = (i == selected_index)
            btn.update()
            btn.draw(window)

        pygame.display.flip()
        clock.tick(60)
