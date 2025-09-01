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
    ruta_fondo = os.path.join(BASE_DIR, "assets", "settings_fondo.png")
    if os.path.exists(ruta_fondo):
        fondo = pygame.image.load(ruta_fondo).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    else:
        fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        fondo.fill((40, 40, 40))  

    # Botón Back (solo imagen)
    ruta_back = os.path.join(BASE_DIR, "assets", "back.png")
    back_button = Button(ruta_back, (1250, 30), scale=0.3)

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
                # Escape → volver al menú
                if event.key == pygame.K_ESCAPE:
                    active_setting = None

                if active_setting is None:
                    # Navegación entre botones
                    if event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % len(settings)
                    elif event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % len(settings)
                    elif event.key == pygame.K_RETURN:
                        active_setting = settings[selected_index]
                else:
                    # Control de VOLUMEN con flechas
                    if active_setting == "VOLUMEN":
                        if event.key == pygame.K_RIGHT:
                            volume_value = min(100, volume_value + 5)
                        elif event.key == pygame.K_LEFT:
                            volume_value = max(0, volume_value - 5)
                        slider_knob.centerx = slider_rect.left + int((volume_value / 100) * slider_rect.w)

        # --- DIBUJADO ---
        window.blit(fondo, (0, 0))

        # Botón Back
        back_button.update()
        back_button.draw(window)

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
        if active_setting == "VOLUMEN":
            pygame.draw.rect(window, (200, 200, 200), slider_rect, 2)
            pygame.draw.line(window, (150, 150, 150),
                             (slider_rect.left, slider_rect.centery),
                             (slider_rect.right, slider_rect.centery), 4)
            pygame.draw.rect(window, (255, 0, 0), slider_knob)
            vol_text = font.render(f"{volume_value}%", True, (255, 255, 255))
            window.blit(vol_text, (slider_rect.right + 40, slider_rect.y - 12))

        # --- Apartado RESOLUCION ---
        if active_setting == "RESOLUCION":
            res_text = font.render("Ajusta la resolución aquí", True, (255, 255, 255))
            window.blit(res_text, (450, 200))

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
