import pygame
import sys
import os
from .button import Button

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


def settings_menu(window):
    from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
    clock = pygame.time.Clock()

    # Fondo (solo una vez)
    BASE_DIR = os.path.dirname(__file__)
    ruta_fondo = os.path.join(BASE_DIR, "assets", "options_fondo.png")

    fondo_base = pygame.image.load(ruta_fondo).convert() if os.path.exists(ruta_fondo) else pygame.Surface(BASE_RES)
    if not os.path.exists(ruta_fondo):
        fondo_base.fill((40, 40, 40))

    # Fuente
    font = pygame.font.SysFont("Consolas", 36, bold=True)

    # Opciones de menú
    settings = ["VOLUMEN", "RESOLUCION", "CONTROLES", "HELP"]
    selected_index = 0
    active_setting = None

    # Volumen
    volume_value = 100
    slider_rect = pygame.Rect(450, 150, 300, 8)
    slider_knob = pygame.Rect(0, 0, 20, 30)
    slider_knob.center = (slider_rect.right, slider_rect.centery)

    # Resoluciones
    resoluciones = ["1920x1080", "1280x720", "800x600", "PANTALLA COMPLETA"]
    res_index = 1
    selected_res = 1

    # Estado de salida
    running = True

    while running:
        ANCHO_PANTALLA, ALTO_PANTALLA = window.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # ESC para salir o volver al menú anterior
                if event.key == pygame.K_ESCAPE:
                    if active_setting is None:
                        running = False
                    else:
                        active_setting = None

                # Navegación del menú principal
                elif active_setting is None:
                    if event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % len(settings)
                    elif event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % len(settings)
                    elif event.key == pygame.K_RETURN:
                        active_setting = settings[selected_index]

                # Ajuste de volumen
                elif active_setting == "VOLUMEN":
                    if event.key == pygame.K_RIGHT:
                        volume_value = min(100, volume_value + 5)
                    elif event.key == pygame.K_LEFT:
                        volume_value = max(0, volume_value - 5)
                    slider_knob.centerx = slider_rect.left + int((volume_value / 100) * slider_rect.w)

                # Ajuste de resolución
                elif active_setting == "RESOLUCION":
                    if event.key == pygame.K_UP:
                        selected_res = (selected_res - 1) % (len(resoluciones) + 1)
                    elif event.key == pygame.K_DOWN:
                        selected_res = (selected_res + 1) % (len(resoluciones) + 1)
                    elif event.key == pygame.K_RETURN:
                        if selected_res < len(resoluciones):
                            res_index = selected_res
                        else:
                            nueva_res = resoluciones[res_index]
                            window, ANCHO_PANTALLA, ALTO_PANTALLA = aplicar_resolucion(window, nueva_res)

        # ---- DIBUJADO ----
        # Limpiar superficie base
        base_surface.blit(pygame.transform.scale(fondo_base, BASE_RES), (0, 0))

        # Dibujar opciones principales
        start_y = BASE_RES[1] - 100
        gap = 250
        buttons_pos = [(150 + i * gap, start_y) for i in range(len(settings))]

        for i, name in enumerate(settings):
            x, y = buttons_pos[i]
            color = (255, 0, 0) if active_setting == name else (255, 255, 255)
            text_surf = font.render(name, True, color)
            text_rect = text_surf.get_rect(center=(x, y))
            base_surface.blit(text_surf, text_rect.topleft)

            if selected_index == i and active_setting != name:
                pygame.draw.line(base_surface, (0, 255, 0),
                                 (text_rect.x, text_rect.bottom + 5),
                                 (text_rect.right, text_rect.bottom + 5), 3)

        # --- Submenús ---
        if active_setting == "RESOLUCION":
            offset_y = 250
            res_text = font.render("AJUSTE LA RESOLUCION", True, (255, 0, 0))
            title_rect = res_text.get_rect(center=(BASE_RES[0] // 2, offset_y - 30))
            base_surface.blit(res_text, title_rect)

            start_y = offset_y + 80
            spacing = 50
            for i, res in enumerate(resoluciones):
                color = (255, 255, 255)
                text = font.render(res, True, color)
                text_rect = text.get_rect(center=(BASE_RES[0] // 2, start_y + i * spacing))
                base_surface.blit(text, text_rect)

                if i == res_index:
                    tick = font.render("✔", True, (0, 255, 0))
                    base_surface.blit(tick, (text_rect.right + 20, text_rect.y))

                if i == selected_res:
                    pygame.draw.line(base_surface, (0, 255, 0),
                                     (text_rect.x, text_rect.bottom + 5),
                                     (text_rect.right, text_rect.bottom + 5), 3)

            aplicar_color = (0, 0, 255) if selected_res == len(resoluciones) else (255, 255, 255)
            aplicar_text = font.render("APLICAR", True, aplicar_color)
            aplicar_rect = aplicar_text.get_rect(center=(BASE_RES[0] // 2, start_y + len(resoluciones) * spacing + 60))
            base_surface.blit(aplicar_text, aplicar_rect)

        elif active_setting == "CONTROLES":
            ctrl_text = font.render("Configura controles aquí", True, (255, 255, 255))
            base_surface.blit(ctrl_text, (450, 200))

        elif active_setting == "HELP":
            help_text = font.render("Ayuda del juego", True, (255, 255, 255))
            base_surface.blit(help_text, (450, 200))

        # Escalar superficie base a pantalla actual
        scaled_surface = pygame.transform.smoothscale(base_surface, (ANCHO_PANTALLA, ALTO_PANTALLA))
        window.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    # Limpiar bien al salir
    return window
