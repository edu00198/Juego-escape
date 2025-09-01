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

<<<<<<< HEAD
    # Botón Back (solo imagen)
=======
    # Botón Back
>>>>>>> 8275473a99cf906fb0c7be558649b2e8ee03e9cb
    ruta_back = os.path.join(BASE_DIR, "assets", "back.png")
    back_button = Button(ruta_back, (1250, 30), scale=0.3)

    # Fuente
    font = pygame.font.SysFont("Consolas", 36, bold=True)

    # Opciones de menú
    settings = ["VOLUMEN", "RESOLUCION", "CONTROLES", "HELP"]
    start_y = 150
    gap = 140
    buttons_pos = [(150, start_y + i * gap) for i in range(len(settings))]
    active_setting = None

    # --- Volumen ---
    volume_value = 100
    slider_rect = pygame.Rect(450, 150, 300, 8)      # barra
    slider_knob = pygame.Rect(0, 0, 20, 30)          # perilla
    slider_knob.center = (slider_rect.right, slider_rect.centery)
    dragging = False

    # Botones de mute/full
    ruta_vol_full = os.path.join(BASE_DIR, "assets", "vol_full.png")
    ruta_mute = os.path.join(BASE_DIR, "assets", "mute.png")
    vol_button_full = Button(ruta_vol_full, (910, 150), scale=0.35, hover_effect=False)
    vol_button_mute = Button(ruta_mute, (870, 150), scale=0.1, hover_effect=False)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()

        # --- EVENTOS ---
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Botón volver
            if back_button.is_clicked(events):
                return

            # Detectar clic en las opciones del menú
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, name in enumerate(settings):
                    x, y = buttons_pos[i]
                    text_surf = font.render(name, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(topleft=(x, y - text_surf.get_height() // 2))
                    if text_rect.collidepoint(event.pos):
                        active_setting = name

            # --- Si estamos en VOLUMEN ---
            if active_setting == "VOLUMEN":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Click en knob → empezar drag
                    if slider_knob.collidepoint(event.pos):
                        dragging = True

                    # Click en icono volumen full → mute
                    elif vol_button_full.is_clicked([event]):
                        volume_value = 0
                        slider_knob.centerx = slider_rect.left

                    # Click en icono mute → volumen full
                    elif vol_button_mute.is_clicked([event]):
                        volume_value = 100
                        slider_knob.centerx = slider_rect.right
            

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = False

                if event.type == pygame.MOUSEMOTION and dragging:
                    # Mover knob dentro de los límites de la barra
                    new_x = max(slider_rect.left, min(mouse_pos[0], slider_rect.right))
                    slider_knob.centerx = new_x
                    # Calcular valor según la posición
                    volume_value = int(((new_x - slider_rect.left) / slider_rect.w) * 100)

<<<<<<< HEAD
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
=======
>>>>>>> 8275473a99cf906fb0c7be558649b2e8ee03e9cb

        # --- DIBUJADO ---
        window.blit(fondo, (0, 0))

        # Botón Back
        back_button.update()
        back_button.draw(window)

        # Dibujar lista de ajustes
        for i, name in enumerate(settings):
            x, y = buttons_pos[i]
<<<<<<< HEAD

            if active_setting == name:
                color = (255, 0, 0)  # activo → rojo
            else:
                color = (255, 255, 255)  # inactivo → blanco
=======
            color = (255, 0, 0) if active_setting == name else (255, 255, 255)
>>>>>>> 8275473a99cf906fb0c7be558649b2e8ee03e9cb

            text_surf = font.render(name, True, color)
            text_rect = text_surf.get_rect(topleft=(x, y - text_surf.get_height() // 2))
            window.blit(text_surf, text_rect.topleft)

            # Subrayado si el mouse está encima
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.line(window, color,
                                 (text_rect.x, text_rect.bottom + 5),
                                 (text_rect.right, text_rect.bottom + 5), 2)

        # Línea separadora
        pygame.draw.line(window, (80, 80, 80), (420, 130), (420, 650), 4)

        # --- Apartado VOLUMEN ---
        if active_setting == "VOLUMEN":
            pygame.draw.rect(window, (200, 200, 200), slider_rect, 2)
            pygame.draw.line(window, (150, 150, 150),
                             (slider_rect.left, slider_rect.centery),
                             (slider_rect.right, slider_rect.centery), 4)
            pygame.draw.rect(window, (255, 0, 0), slider_knob)
            vol_text = font.render(f"{volume_value}%", True, (255, 255, 255))
            window.blit(vol_text, (slider_rect.right + 40, slider_rect.y - 12))

            # Mostrar icono correspondiente
            if volume_value == 100:
                vol_button_full.draw(window)
            elif volume_value == 0:
                vol_button_mute.draw(window)

        pygame.display.flip()
        clock.tick(60)
