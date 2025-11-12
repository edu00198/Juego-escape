import pygame
import sys
import os
import json
from .button import Button

BASE_RES = (1280, 720)
base_surface = pygame.Surface(BASE_RES)
fullscreen = False

# Ruta al archivo de configuración
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_settings():
    """Carga las configuraciones guardadas"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
    # Configuración por defecto
    return {
        "volumes": {
            "MUSIC": 100,
            "SFX": 100,
            "MASTER": 100
        }
    }

def save_settings(settings):
    """Guarda las configuraciones en el archivo"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        print("✅ Configuración guardada correctamente")
    except Exception as e:
        print(f"❌ Error al guardar configuración: {e}")


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
    ruta_fondo = os.path.join(BASE_DIR, "assets", "fondo_s.png")

    fondo_base = pygame.image.load(ruta_fondo).convert() if os.path.exists(ruta_fondo) else pygame.Surface(BASE_RES)
    if not os.path.exists(ruta_fondo):
        fondo_base.fill((40, 40, 40))

    # Fuente
    font = pygame.font.SysFont("Consolas", 32, bold=True)

    # Tabs
    tabs = ["VOLUME", "RESOLUTION", "CONTROLS"]
    tab_index = 0
    active_section = None

    # Volume sliders (values 0-100)
    vol_labels = ["MUSIC", "SFX", "MASTER"]
    # Cargar configuraciones guardadas
    saved_settings = load_settings()
    volumes = saved_settings["volumes"]
    volumes_original = volumes.copy()  # Guardar copia de los valores originales
    vol_selected = 0
    has_volume_changes = False

    # Resolution state
    resoluciones = ["1920x1080", "1280x720", "800x600"]
    res_index = 1
    res_index_original = res_index  # Guardar copia del valor original
    has_resolution_changes = False
    # cursor in resolution tab: 0..len(resoluciones) where last index is FULLSCREEN toggle
    res_cursor = 0
    is_fullscreen = False
    # store previous size to revert if needed
    prev_size = window.get_size()
    pending_fullscreen = False
    fullscreen_timer_start = None
    fullscreen_confirm_seconds = 10

    # Controls organized by categories
    controls = {
        "pause": [("Pause", pygame.K_ESCAPE)],
        "movement": [
            ("Move Forward", pygame.K_UP),
            ("Move Left", pygame.K_LEFT),
            ("Move Backward", pygame.K_DOWN),
            ("Move Right", pygame.K_RIGHT),
        ],
        "combat": [
            ("Attack", pygame.K_SPACE),
            ("Use", pygame.K_SPACE),
        ]
    }
    # Total count for navigation
    total_controls = sum(len(section) for section in controls.values())
    control_selected = 0
    rebinding = False

    # Variables para el sistema de advertencias
    advertencia = False
    tiempo_advertencia = 0

    running = True
    while running:
        ANCHO_PANTALLA, ALTO_PANTALLA = window.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if rebinding and event.type == pygame.KEYDOWN:
                # Find the correct control to update based on control_selected
                current_idx = 0
                for section in ["pause", "movement", "combat"]:
                    for i, (name, _) in enumerate(controls[section]):
                        if current_idx == control_selected:
                            # Update the key for this control
                            controls[section][i] = (name, event.key)
                            rebinding = False
                            break
                        current_idx += 1
                    if not rebinding:  # If we found and updated the control, break the outer loop
                        break
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # if in a pending fullscreen confirm, revert
                    if pending_fullscreen:
                        # revert
                        window, _, _ = aplicar_resolucion(window, f"{prev_size[0]}x{prev_size[1]}")
                        pending_fullscreen = False
                        fullscreen_timer_start = None
                        is_fullscreen = False
                    elif advertencia:
                        # Si hay advertencia activa, salir sin guardar
                        if active_section == "VOLUME":
                            volumes = volumes_original.copy()
                            has_volume_changes = False
                        elif active_section == "RESOLUTION":
                            res_index = res_index_original
                            has_resolution_changes = False
                        active_section = None
                        advertencia = False
                    elif active_section is not None:
                        # Verificar si hay cambios sin guardar
                        if (active_section == "VOLUME" and has_volume_changes) or \
                           (active_section == "RESOLUTION" and has_resolution_changes):
                            # Mostrar advertencia y esperar confirmación
                            advertencia = True
                            tiempo_advertencia = pygame.time.get_ticks()
                        else:
                            active_section = None
                    else:
                        running = False

                # If a fullscreen confirmation is pending, Enter keeps the fullscreen
                if pending_fullscreen and event.key == pygame.K_RETURN:
                    pending_fullscreen = False
                    fullscreen_timer_start = None
                    is_fullscreen = True

                # Enter toggles entering/exiting a section or saves changes
                elif event.key == pygame.K_RETURN:
                    if advertencia:
                        # Si hay advertencia activa, guardar y salir
                        if active_section == "VOLUME":
                            settings = load_settings()
                            settings["volumes"] = volumes.copy()
                            save_settings(settings)
                            volumes_original = volumes.copy()
                            has_volume_changes = False
                        elif active_section == "RESOLUTION":
                            res_index_original = res_index
                            has_resolution_changes = False
                        active_section = None
                        advertencia = False
                    elif active_section is None:
                        # enter the current tab (except CONTROLS which is read-only)
                        if tabs[tab_index] != "CONTROLS":
                            active_section = tabs[tab_index]
                            # initialize some cursors when entering a tab
                            if active_section == "RESOLUTION":
                                res_cursor = res_index
                    else:
                        # already inside a section: perform section-specific Enter actions
                        if active_section == "RESOLUTION":
                            # act on the resolution cursor
                            if res_cursor < len(resoluciones):
                                nueva_res = resoluciones[res_cursor]
                                window, ANCHO_PANTALLA, ALTO_PANTALLA = aplicar_resolucion(window, nueva_res)
                                res_index = res_cursor
                                res_index_original = res_index  # Actualizar valor original
                                has_resolution_changes = False  # Reiniciar bandera de cambios
                                print("Resolución guardada:", nueva_res)
                            else:
                                if not pending_fullscreen:
                                    prev_size = window.get_size()
                                    window, ANCHO_PANTALLA, ALTO_PANTALLA = aplicar_resolucion(window, "PANTALLA COMPLETA")
                                    pending_fullscreen = True
                                    fullscreen_timer_start = pygame.time.get_ticks()
                                    is_fullscreen = True
                        elif active_section == "VOLUME":
                            # Guardar el volumen actual
                            settings = load_settings()
                            settings["volumes"] = volumes.copy()
                            save_settings(settings)
                            volumes_original = volumes.copy()  # Actualizar valores originales
                            has_volume_changes = False  # Reiniciar bandera de cambios
                            print("Valores actuales:")
                            for lbl in vol_labels:
                                print(f"  {lbl}: {volumes[lbl]}%")

                # tab navigation (only when not inside a section) - LEFT/RIGHT only
                elif active_section is None and event.key == pygame.K_RIGHT:
                    tab_index = (tab_index + 1) % len(tabs)
                elif active_section is None and event.key == pygame.K_LEFT:
                    tab_index = (tab_index - 1) % len(tabs)

                # Volume adjustments when in VOLUME tab and inside the section
                if active_section == "VOLUME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            key = vol_labels[vol_selected]
                            volumes[key] = min(100, volumes[key] + 5)
                            has_volume_changes = any(volumes[k] != volumes_original[k] for k in vol_labels)
                        elif event.key == pygame.K_LEFT:
                            key = vol_labels[vol_selected]
                            volumes[key] = max(0, volumes[key] - 5)
                            has_volume_changes = any(volumes[k] != volumes_original[k] for k in vol_labels)
                        elif event.key == pygame.K_UP:
                            vol_selected = (vol_selected - 1) % len(vol_labels)
                        elif event.key == pygame.K_DOWN:
                            vol_selected = (vol_selected + 1) % len(vol_labels)

                # Resolution list navigation when in RESOLUTION tab and not pending fullscreen
                if active_section == "RESOLUTION" and not pending_fullscreen:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            res_cursor = (res_cursor - 1) % (len(resoluciones) + 1)
                        elif event.key == pygame.K_DOWN:
                            res_cursor = (res_cursor + 1) % (len(resoluciones) + 1)

                # Controls navigation (only when inside CONTROLS section)
                if active_section == "CONTROLS" and not rebinding:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            control_selected = (control_selected - 1) % total_controls
                        elif event.key == pygame.K_DOWN:
                            control_selected = (control_selected + 1) % total_controls

        # ---- confirmation timer for fullscreen ----
        if pending_fullscreen and fullscreen_timer_start is not None:
            elapsed = (pygame.time.get_ticks() - fullscreen_timer_start) / 1000.0
            if elapsed >= fullscreen_confirm_seconds:
                # time out: revert
                window, _, _ = aplicar_resolucion(window, f"{prev_size[0]}x{prev_size[1]}")
                pending_fullscreen = False
                fullscreen_timer_start = None
                is_fullscreen = False

        # ---- DIBUJADO ----
        base_surface.blit(pygame.transform.scale(fondo_base, BASE_RES), (0, 0))

        # draw tabs as simple labels at top
        tab_font = pygame.font.SysFont("Consolas", 28, bold=True)
        gap = 30
        start_x = 60
        y_tab = 60
        for i, t in enumerate(tabs):
            color = (255, 255, 255) if i == tab_index else (180, 180, 180)
            t_surf = tab_font.render(t, True, color)
            t_rect = t_surf.get_rect(topleft=(start_x + i * 220, y_tab))
            base_surface.blit(t_surf, t_rect)

        # Prepare scaled mouse position (map window coords -> BASE_RES coords)
        mx_win, my_win = pygame.mouse.get_pos()
        win_w, win_h = window.get_size()
        scale_x = BASE_RES[0] / win_w if win_w else 1.0
        scale_y = BASE_RES[1] / win_h if win_h else 1.0
        mx = int(mx_win * scale_x)
        my = int(my_win * scale_y)

        # Draw content for each tab
        if tabs[tab_index] == "VOLUME":
            # Volume control layout starts here

            # draw sliders
            slider_y = 200
            slider_gap_y = 120
            
            # Use pixel font for labels and numbers if available
            try:
                ruta_fuente = os.path.join(BASE_DIR, "assets", "font.ttf")
                label_font = pygame.font.Font(ruta_fuente, 36)
                small_font = pygame.font.Font(ruta_fuente, 24)  # Pixel font for numbers
            except Exception:
                label_font = pygame.font.SysFont("Consolas", 36)
                small_font = pygame.font.SysFont("Consolas", 24)
            
            # Calcular el ancho total de todos los elementos para centrarlos
            bar_w = 500  # Ancho de la barra
            label_gap = 40  # Espacio entre etiqueta y barra
            value_gap = 20  # Espacio entre barra y valor
            
            # Centrar todo el conjunto de elementos
            total_width = bar_w + label_gap + value_gap + 100  # +100 para el valor numérico
            center_x = BASE_RES[0] // 2
            slider_start_x = center_x - (total_width // 2)
            
            for i, lbl in enumerate(vol_labels):
                y = slider_y + i * slider_gap_y
                
                # label using pixel font
                lbl_surf = label_font.render(lbl, True, (255, 255, 255))
                lbl_rect = lbl_surf.get_rect(right=slider_start_x + label_gap, centery=y + 8)
                base_surface.blit(lbl_surf, lbl_rect)

                # bar
                bar_x = slider_start_x + label_gap
                bar_y = y + 8
                bar_h = 12
                pygame.draw.rect(base_surface, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h))
                val = volumes[lbl]
                fill_w = int((val / 100.0) * bar_w)
                pygame.draw.rect(base_surface, (0, 160, 255), (bar_x, bar_y, fill_w, bar_h))

                # knob
                knob_x = bar_x + fill_w
                knob_rect = pygame.Rect(knob_x - 8, bar_y - 8, 16, bar_h + 16)
                pygame.draw.rect(base_surface, (220, 220, 220), knob_rect)

                # value text using small font
                val_surf = small_font.render(f"{val}", True, (255, 255, 255))
                base_surface.blit(val_surf, (bar_x + bar_w + 20, y))

                # highlight: green only when mouse is over the bar; keyboard selection has a neutral highlight
                bar_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
                hovered = bar_rect.collidepoint(mx, my)
                if hovered:
                    pygame.draw.rect(base_surface, (0, 255, 0), (bar_x - 4, bar_y - 4, bar_w + 8, bar_h + 8), 2)
                elif i == vol_selected and active_section == "VOLUME":
                    # keyboard-selected but not hovered: neutral highlight
                    pygame.draw.rect(base_surface, (200, 200, 200), (bar_x - 4, bar_y - 4, bar_w + 8, bar_h + 8), 2)

        elif tabs[tab_index] == "RESOLUTION":
            # Use pixel font for the list, but keep the title at the top using the regular 'font'
            try:
                ruta_fuente = os.path.join(BASE_DIR, "assets", "font.ttf")
                pixel_font = pygame.font.Font(ruta_fuente, 48)  # Aumentado de 36 a 48
                small_font = pygame.font.Font(ruta_fuente, 24)  # Aumentado de 20 a 24
            except Exception:
                pixel_font = pygame.font.SysFont("Consolas", 48)  # Aumentado de 36 a 48
                small_font = pygame.font.SysFont("Consolas", 24)  # Aumentado de 20 a 24

            # Resolution list layout starts here

            # Build entries (resolutions + fullscreen toggle) and center them
            entries = list(resoluciones)
            fs_text = "ON" if is_fullscreen or pending_fullscreen else "OFF"
            entries.append(f"FULLSCREEN: {fs_text}")

            line_h = pixel_font.get_linesize() + 20  # Añadido espacio extra entre líneas
            total_height = line_h * len(entries)
            start_y = BASE_RES[1] // 2 - total_height // 2
            cx_center = BASE_RES[0] // 2

            for i, entry in enumerate(entries):
                # Decide color: when inside section use res_cursor, otherwise highlight applied resolution or fullscreen state
                if active_section == "RESOLUTION":
                    if i == res_cursor:
                        color = (255, 255, 255)
                    else:
                        color = (200, 200, 200)
                else:
                    if i < len(resoluciones):
                        color = (255, 255, 255) if i == res_index else (200, 200, 200)
                    else:
                        # fullscreen line: highlight if fullscreen currently on / pending
                        color = (255, 255, 255) if (is_fullscreen or pending_fullscreen) else (200, 200, 200)

                r_surf = pixel_font.render(entry, True, color)
                r_rect = r_surf.get_rect(center=(cx_center, start_y + i * line_h))
                base_surface.blit(r_surf, r_rect)

            # indicate currently applied resolution below the list (small font)
            applied_surf = small_font.render(f"Applied: {resoluciones[res_index]}", True, (150, 150, 150))
            applied_rect = applied_surf.get_rect(center=(cx_center, start_y + len(entries) * line_h + 20))
            base_surface.blit(applied_surf, applied_rect)

            # pending fullscreen overlay
            if pending_fullscreen and fullscreen_timer_start:
                elapsed = (pygame.time.get_ticks() - fullscreen_timer_start) / 1000.0
                left = max(0, int(fullscreen_confirm_seconds - elapsed))
                overlay = pygame.Surface((BASE_RES[0], BASE_RES[1]), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                msg = pygame.font.SysFont("Consolas", 28).render(f"Press ENTER to KEEP or ESC to REVERT ({left}s)", True, (255, 255, 255))
                msg_rect = msg.get_rect(center=(BASE_RES[0] // 2, BASE_RES[1] // 2))
                overlay.blit(msg, msg_rect)
                base_surface.blit(overlay, (0, 0))

        elif tabs[tab_index] == "CONTROLS":
            # Pixel font for list, but the title stays at the top using the regular 'font'
            try:
                ruta_fuente = os.path.join(BASE_DIR, "assets", "font.ttf")
                pixel_font = pygame.font.Font(ruta_fuente, 36)
                small_font = pygame.font.Font(ruta_fuente, 24)
            except Exception:
                pixel_font = pygame.font.SysFont("Consolas", 36)
                small_font = pygame.font.SysFont("Consolas", 24)

            # Controls list layout starts here

            # Center the controls list vertically and horizontally, but moved down
            line_h = pixel_font.get_linesize()
            gap_after_section = line_h * 2  # Increased gap between sections
            
            # Calculate total height including section titles and gaps
            total_lines = total_controls + (1 if controls["movement"] else 0) + (1 if controls["combat"] else 0) + 4  # +4 for larger gaps
            total_height = line_h * total_lines
            # Ajustado para mover todo 100 píxeles más abajo
            start_y = (BASE_RES[1] // 2 - total_height // 2) + 50
            cx_center = BASE_RES[0] // 2
            
            current_y = start_y
            current_control = 0
            
            # First render PAUSE at the top with extra spacing
            for i, (name, key) in enumerate(controls["pause"]):
                key_name = pygame.key.name(key).upper()
                txt = pixel_font.render(f"{name}: {key_name}", True, (215, 215, 215))
                txt_rect = txt.get_rect(center=(cx_center, current_y))
                base_surface.blit(txt, txt_rect)
                current_control += 1
            
            current_y += line_h * 3  # Triple the space after PAUSE
            
            # MOVEMENT section
            if controls["movement"]:
                # Title right-aligned
                title = pixel_font.render("MOVEMENT", True, (150, 150, 150))
                title_rect = title.get_rect(midright=(cx_center - 320, current_y))
                base_surface.blit(title, title_rect)
                current_y += line_h
                
                for name, key in controls["movement"]:
                    key_name = pygame.key.name(key).upper()
                    txt = pixel_font.render(f"{name}: {key_name}", True, (215, 215, 215))
                    txt_rect = txt.get_rect(center=(cx_center, current_y))
                    base_surface.blit(txt, txt_rect)
                    current_y += line_h
                    current_control += 1
                
                current_y += gap_after_section
            
            # COMBAT section
            if controls["combat"]:
                # Title right-aligned
                title = pixel_font.render("COMBAT", True, (150, 150, 150))
                title_rect = title.get_rect(midright=(cx_center - 400, current_y))
                base_surface.blit(title, title_rect)
                current_y += line_h
                
                for name, key in controls["combat"]:
                    key_name = pygame.key.name(key).upper()
                    txt = pixel_font.render(f"{name}: {key_name}", True, (215, 215, 215))
                    txt_rect = txt.get_rect(center=(cx_center, current_y))
                    base_surface.blit(txt, txt_rect)
                    current_y += line_h
                    current_control += 1
                    
                current_y += line_h  # Extra space after last section

            if rebinding:
                info = small_font.render("Press new key...", True, (255, 200, 0))
                info_rect = info.get_rect(center=(cx_center, start_y + len(controls) * line_h + 40))
                base_surface.blit(info, info_rect)

        # Mostrar mensajes de ayuda según la sección activa
        if active_section in ["VOLUME", "RESOLUTION"]:
            help_font = pygame.font.SysFont("Consolas", 20)
            help_text = help_font.render("Press ENTER to save changes", True, (150, 150, 150))
            help_rect = help_text.get_rect(bottomright=(BASE_RES[0] - 20, BASE_RES[1] - 20))
            base_surface.blit(help_text, help_rect)

            if ((active_section == "VOLUME" and has_volume_changes) or 
                (active_section == "RESOLUTION" and has_resolution_changes)):
                unsaved_text = help_font.render("* Unsaved changes", True, (255, 200, 0))
                unsaved_rect = unsaved_text.get_rect(bottomright=(BASE_RES[0] - 20, BASE_RES[1] - 50))
                base_surface.blit(unsaved_text, unsaved_rect)

        # Escalar superficie base a pantalla actual
        scaled_surface = pygame.transform.smoothscale(base_surface, (ANCHO_PANTALLA, ALTO_PANTALLA))
        window.blit(scaled_surface, (0, 0))

        # Mostrar advertencia si es necesario
        if advertencia:
            # Crear superficie semi-transparente para el fondo
            overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            window.blit(overlay, (0, 0))

            # Mostrar mensaje de advertencia
            warning_font = pygame.font.SysFont("Consolas", 32)
            warning_text = warning_font.render("Exit without saving changes?", True, (255, 255, 255))
            warning_help = warning_font.render("Press ENTER to save, ESC to exit without saving", True, (200, 200, 200))
            
            # Centrar los mensajes
            warning_rect = warning_text.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 20))
            help_rect = warning_help.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 20))
            
            window.blit(warning_text, warning_rect)
            window.blit(warning_help, help_rect)

        pygame.display.flip()
        clock.tick(60)

    return window
