import pygame
import sys
import os
from .button import Button

def settings_menu(window):
    from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
    ANCHO_PANTALLA, ALTO_PANTALLA = window.get_size()
    clock = pygame.time.Clock()
    BASE_DIR = os.path.dirname(__file__)

    # Fondo
    ruta_fondo = os.path.join(BASE_DIR, "assets", "options_fondo.png")
    if os.path.exists(ruta_fondo):
        fondo = pygame.image.load(ruta_fondo).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    else:
        fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        fondo.fill((40, 40, 40))  


    # Fuente
    font = pygame.font.SysFont("Consolas", 36, bold=True)

    # Opciones de menú
    settings = ["VOLUMEN", "RESOLUCION", "CONTROLES", "HELP"]
    start_y = ALTO_PANTALLA - 100
    gap = 250
    buttons_pos = [(150 + i * gap, start_y) for i in range(len(settings))]
    selected_index = 0
    active_setting = None

    # --- Volumen ---
    volume_value = 100
    slider_rect = pygame.Rect(450, 150, 300, 8)
    slider_knob = pygame.Rect(0, 0, 20, 30)
    slider_knob.center = (slider_rect.right, slider_rect.centery)

    while True:
        events = pygame.event.get()

        # --- EVENTOS ---
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Escape → volver al menú principal o salir del ajuste
                if event.key == pygame.K_ESCAPE:
                    if active_setting is None:
                        return   # salís de settings por completo
                    else:
                        active_setting = None  # salís del ajuste actual

                # --- Si NO estoy dentro de un ajuste ---
                if active_setting is None:
                    if event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % len(settings)
                    elif event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % len(settings)
                    elif event.key == pygame.K_RETURN:
                        active_setting = settings[selected_index]

                # --- Si estoy en VOLUMEN ---
                elif active_setting == "VOLUMEN":
                    if event.key == pygame.K_RIGHT:
                        volume_value = min(100, volume_value + 5)
                    elif event.key == pygame.K_LEFT:
                        volume_value = max(0, volume_value - 5)
                    slider_knob.centerx = slider_rect.left + int((volume_value / 100) * slider_rect.w)

                # --- Si estoy en RESOLUCION ---
                elif active_setting == "RESOLUCION":
                    if event.key == pygame.K_UP:
                        selected_res = (selected_res - 1) % (len(resoluciones) + 1)  # incluye "APLICAR"
                    elif event.key == pygame.K_DOWN:
                        selected_res = (selected_res + 1) % (len(resoluciones) + 1)
                    elif event.key == pygame.K_RETURN:
                        if selected_res < len(resoluciones):
                            res_index = selected_res  # marcar resolución elegida
                        else:
                            # Opción "APLICAR"
                            ancho, alto = map(int, resoluciones[res_index].split("x"))
                            window = pygame.display.set_mode((ancho, alto))
                            ANCHO_PANTALLA, ALTO_PANTALLA = ancho, alto

        # --- DIBUJADO ---
        window.blit(fondo, (0, 0))

        # Dibujar botones
        for i, name in enumerate(settings):
            x, y = buttons_pos[i]

            if active_setting == name:
                color = (255, 0, 0)  # activo → rojo
            else:
                color = (255, 255, 255)  # inactivo → blanco

            text_surf = font.render(name, True, color)
            text_rect = text_surf.get_rect(center=(x, y))
            window.blit(text_surf, text_rect.topleft)

            # Subrayado verde si seleccionado pero no activo
            if selected_index == i and active_setting != name:
                pygame.draw.line(window, (0, 255, 0),
                                 (text_rect.x, text_rect.bottom + 5),
                                 (text_rect.right, text_rect.bottom + 5), 3)


        # --- Apartado VOLUMEN ---
        if active_setting == "RESOLUCION":
            # Margen superior general para la lista (resoluciones)
            offset_y = 250  # la lista y demás quedan igual

            # Texto principal centrado y en rojo (lo bajamos un poco más)
            res_text = font.render("AJUSTE LA RESOLUCION", True, (255, 0, 0))
            title_rect = res_text.get_rect(center=(ANCHO_PANTALLA // 2, offset_y - 30))  # subimos la lista pero bajamos título
            window.blit(res_text, title_rect)

            # Lista de resoluciones disponibles
            resoluciones = ["1920x1080", "1280x720", "800x600"]
            if "res_index" not in locals():
                res_index = 1
            if "selected_res" not in locals():
                selected_res = res_index

            # Dibujar opciones
            start_y = offset_y + 80  # posición inicial de la lista
            spacing = 50

            for i, res in enumerate(resoluciones):
                color = (255, 255, 255)
                text = font.render(res, True, color)
                text_rect = text.get_rect(center=(ANCHO_PANTALLA // 2, start_y + i * spacing))
                window.blit(text, text_rect)

                if i == res_index:
                    tick = font.render("✔", True, (0, 255, 0))
                    window.blit(tick, (text_rect.right + 20, text_rect.y))

                if i == selected_res:
                    pygame.draw.line(window, (0, 255, 0),
                                    (text_rect.x, text_rect.bottom + 5),
                                    (text_rect.right, text_rect.bottom + 5), 3)

            # Botón APLICAR (lo subimos un poco)
            aplicar_color = (0, 0, 255) if selected_res == len(resoluciones) else (255, 255, 255)
            aplicar_text = font.render("APLICAR", True, aplicar_color)
            aplicar_rect = aplicar_text.get_rect(center=(ANCHO_PANTALLA // 2, start_y + len(resoluciones) * spacing + 60))  # antes era +80
            window.blit(aplicar_text, aplicar_rect)


        # --- Apartado CONTROLES ---
        if active_setting == "CONTROLES":
            ctrl_text = font.render("Configura controles aquí", True, (255, 255, 255))
            window.blit(ctrl_text, (450, 200))

        # --- Apartado HELP ---
        if active_setting == "HELP":
            help_text = font.render("Ayuda del juego", True, (255, 255, 255))
            window.blit(help_text, (450, 200))

        pygame.display.flip()
        clock.tick(60)
