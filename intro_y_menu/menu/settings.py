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
    volumes = {k: 100 for k in vol_labels}
    vol_selected = 0

    # Resolution state
    resoluciones = ["1920x1080", "1280x720", "800x600"]
    res_index = 1
    # cursor in resolution tab: 0..len(resoluciones) where last index is FULLSCREEN toggle
    res_cursor = 0
    is_fullscreen = False
    # store previous size to revert if needed
    prev_size = window.get_size()
    pending_fullscreen = False
    fullscreen_timer_start = None
    fullscreen_confirm_seconds = 10

    # Controls (simple mapping)
    controls = [
        ("Move Up", pygame.K_w),
        ("Move Down", pygame.K_s),
        ("Move Left", pygame.K_a),
        ("Move Right", pygame.K_d),
        ("Attack", pygame.K_SPACE),
        ("Pause", pygame.K_ESCAPE),
    ]
    control_selected = 0
    rebinding = False

    running = True
    while running:
        ANCHO_PANTALLA, ALTO_PANTALLA = window.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if rebinding and event.type == pygame.KEYDOWN:
                # set new key for selected control
                controls[control_selected] = (controls[control_selected][0], event.key)
                rebinding = False
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
                    elif active_section is not None:
                        # exit the active section without closing settings
                        active_section = None
                    else:
                        running = False

                # If a fullscreen confirmation is pending, Enter keeps the fullscreen
                if pending_fullscreen and event.key == pygame.K_RETURN:
                    pending_fullscreen = False
                    fullscreen_timer_start = None
                    is_fullscreen = True

                # Enter toggles entering/exiting a section
                elif event.key == pygame.K_RETURN:
                    if active_section is None:
                        # enter the current tab
                        active_section = tabs[tab_index]
                        # initialize some cursors when entering a tab
                        if active_section == "RESOLUTION":
                            res_cursor = res_index
                    else:
                        # already inside a section: perform section-specific Enter
                        if active_section == "CONTROLS":
                            rebinding = True
                        elif active_section == "RESOLUTION":
                            # act on the resolution cursor
                            if res_cursor < len(resoluciones):
                                nueva_res = resoluciones[res_cursor]
                                window, ANCHO_PANTALLA, ALTO_PANTALLA = aplicar_resolucion(window, nueva_res)
                                res_index = res_cursor
                            else:
                                if not pending_fullscreen:
                                    prev_size = window.get_size()
                                    window, ANCHO_PANTALLA, ALTO_PANTALLA = aplicar_resolucion(window, "PANTALLA COMPLETA")
                                    pending_fullscreen = True
                                    fullscreen_timer_start = pygame.time.get_ticks()
                                    is_fullscreen = True
                        # for VOLUME, Enter does nothing special (use arrows); for CONTROLS handled above

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
                        elif event.key == pygame.K_LEFT:
                            key = vol_labels[vol_selected]
                            volumes[key] = max(0, volumes[key] - 5)
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
                            control_selected = (control_selected - 1) % len(controls)
                        elif event.key == pygame.K_DOWN:
                            control_selected = (control_selected + 1) % len(controls)

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
            # Use pixel font for VOLUME title and labels if available
            try:
                ruta_fuente = os.path.join(BASE_DIR, "assets", "font.ttf")
                pixel_font = pygame.font.Font(ruta_fuente, 36)
                small_font = pygame.font.Font(ruta_fuente, 20)
            except Exception:
                pixel_font = pygame.font.SysFont("Consolas", 36)
                small_font = pygame.font.SysFont("Consolas", 20)

            title = pixel_font.render("VOLUME", True, (255, 255, 255))
            base_surface.blit(title, (60, 120))

            # draw sliders
            slider_start_x = 120
            slider_y = 200
            slider_gap_y = 120
            for i, lbl in enumerate(vol_labels):
                x = slider_start_x
                y = slider_y + i * slider_gap_y
                # label using pixel font
                lbl_surf = pixel_font.render(lbl, True, (255, 255, 255))
                base_surface.blit(lbl_surf, (x, y))

                # bar
                bar_x = x + 220
                bar_y = y + 8
                bar_w = 500
                bar_h = 12
                pygame.draw.rect(base_surface, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h))
                val = volumes[lbl]
                fill_w = int((val / 100.0) * bar_w)
                pygame.draw.rect(base_surface, (0, 160, 255), (bar_x, bar_y, fill_w, bar_h))

                # knob
                knob_x = bar_x + fill_w
                knob_rect = pygame.Rect(knob_x - 8, bar_y - 8, 16, bar_h + 16)
                pygame.draw.rect(base_surface, (220, 220, 220), knob_rect)

                # value text using small pixel font
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
                pixel_font = pygame.font.Font(ruta_fuente, 36)
                small_font = pygame.font.Font(ruta_fuente, 20)
            except Exception:
                pixel_font = pygame.font.SysFont("Consolas", 36)
                small_font = pygame.font.SysFont("Consolas", 20)

            # Title at original top position using non-pixel font
            title = font.render("RESOLUTION", True, (255, 255, 255))
            base_surface.blit(title, (60, 120))

            # Build entries (resolutions + fullscreen toggle) and center them
            entries = list(resoluciones)
            fs_text = "ON" if is_fullscreen or pending_fullscreen else "OFF"
            entries.append(f"FULLSCREEN: {fs_text}")

            line_h = pixel_font.get_linesize()
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

            # Title at original top position using the non-pixel font
            title = font.render("CONTROLS", True, (255, 255, 255))
            base_surface.blit(title, (60, 120))

            # Center the controls list vertically and horizontally
            line_h = pixel_font.get_linesize()
            total_height = line_h * len(controls)
            start_y = BASE_RES[1] // 2 - total_height // 2
            cx_center = BASE_RES[0] // 2

            for i, (name, key) in enumerate(controls):
                key_name = pygame.key.name(key).upper()
                color = (255, 255, 255) if i == control_selected else (200, 200, 200)
                txt = pixel_font.render(f"{name}: {key_name}", True, color)
                txt_rect = txt.get_rect(center=(cx_center, start_y + i * line_h))
                base_surface.blit(txt, txt_rect)

            if rebinding:
                info = small_font.render("Press new key...", True, (255, 200, 0))
                info_rect = info.get_rect(center=(cx_center, start_y + len(controls) * line_h + 40))
                base_surface.blit(info, info_rect)

        # Escalar superficie base a pantalla actual
        scaled_surface = pygame.transform.smoothscale(base_surface, (ANCHO_PANTALLA, ALTO_PANTALLA))
        window.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    return window
