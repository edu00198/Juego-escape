import pygame
import sys
import os
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, m1_opciones, m2_opciones
from intro_y_menu.menu.button import Button
from intro_y_menu.menu.settings import settings_menu
from intro_y_menu.menu.menuzaso import menus
from assets.mapas.fondo import resume_button, help_button, settings_button, save_button, quit_button, menu_pause
from .save_system import save_game, list_saves

# ==========================
# MENÚ DE PAUSA
# ==========================

def pause_menu(pantalla, mapa_actual=1, state=None):
    """
    Menú de pausa que aparece al presionar ESC.
    Usa imágenes de fondo y botones personalizados.
    Solo se mueve con ↑ y ↓, y ENTER para interactuar.
    """

    # --- FONDO SEGÚN EL MAPA ---
    try:
        if mapa_actual == 1:
            fondo = pygame.image.load(m1_opciones).convert()
        elif mapa_actual == 2:
            fondo = pygame.image.load(m2_opciones).convert()
        else:
            raise ValueError("Mapa no válido")
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        fondo.fill(BLANCO)

    # --- CONTENEDOR CENTRAL (menu_pause) ---
    try:
        menu_fondo = pygame.image.load(menu_pause).convert_alpha()
    except Exception as e:
        print(f"No se pudo cargar menu_pause: {e}")
        menu_fondo = None

    # --- CREAR BOTONES ---
    btn_width = 300
    btn_height = 70
    spacing = 20
    start_y = (ALTO_PANTALLA - (btn_height * 5 + spacing * 4)) // 2

    # Cada botón usa su imagen importada
    reanudar_button = Button(resume_button, (ANCHO_PANTALLA // 2, start_y))
    ayuda_button = Button(help_button, (ANCHO_PANTALLA // 2, start_y + (btn_height + spacing)))
    config_button = Button(settings_button, (ANCHO_PANTALLA // 2, start_y + 2 * (btn_height + spacing)))
    guardar_button = Button(save_button, (ANCHO_PANTALLA // 2, start_y + 3 * (btn_height + spacing)))
    salir_button = Button(quit_button, (ANCHO_PANTALLA // 2, start_y + 4 * (btn_height + spacing)))

    buttons = [reanudar_button, ayuda_button, config_button, guardar_button, salir_button]

    selected_index = 0
    buttons[selected_index].selected = True

    clock = pygame.time.Clock()
    paused = True

    # ==========================
    # LOOP PRINCIPAL DEL MENÚ
    # ==========================
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # --- Navegación solo con ↑ y ↓ ---
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_ESCAPE:
                    return  # vuelve al juego
                elif event.key == pygame.K_RETURN:
                    # --- Acción del botón seleccionado ---
                    clicked_button = buttons[selected_index]

                    if clicked_button == reanudar_button:
                        return
                    elif clicked_button == guardar_button:
                        if state:
                            # Mostrar submenu para elegir slot
                            slot = select_save_slot(pantalla, mapa_actual)
                            if slot:
                                save_game(state, slot)
                                print(f"Partida guardada en slot {slot}.")
                        else:
                            print("No hay estado para guardar.")
                        menus()
                    elif clicked_button == ayuda_button:
                        print("Abrir ayuda...")
                    elif clicked_button == config_button:
                        settings_menu(pantalla)
                    elif clicked_button == salir_button:
                        menus()

        # --- DIBUJAR FONDO ---
        pantalla.blit(fondo, (0, 0))

        # --- DIBUJAR CONTENEDOR CENTRAL ---
        if menu_fondo:
            pantalla.blit(menu_fondo, ((ANCHO_PANTALLA - 500) // 2, (ALTO_PANTALLA - 715) // 2))

        # --- DIBUJAR BOTONES ---
        for i, btn in enumerate(buttons):
            btn.selected = (i == selected_index)
            btn.update()  # esto aplica el efecto de agrandado
            btn.draw(pantalla)

        pygame.display.flip()
        clock.tick(60)


def select_save_slot(pantalla, mapa_actual):
    """
    Submenú para seleccionar el slot de guardado.
    """
    # --- FONDO SEGÚN EL MAPA ---
    try:
        if mapa_actual == 1:
            fondo = pygame.image.load(m1_opciones).convert()
        elif mapa_actual == 2:
            fondo = pygame.image.load(m2_opciones).convert()
        else:
            raise ValueError("Mapa no válido")
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        fondo.fill(BLANCO)

    # --- CONTENEDOR CENTRAL ---
    try:
        menu_fondo = pygame.image.load(menu_pause).convert_alpha()
    except Exception as e:
        print(f"No se pudo cargar menu_pause: {e}")
        menu_fondo = None

    # --- CREAR BOTONES PARA SLOTS ---
    btn_width = 300
    btn_height = 70
    spacing = 20
    start_y = (ALTO_PANTALLA - (btn_height * 5 + spacing * 4)) // 2

    slots = list_saves()
    buttons = []
    for i in range(1, 6):
        # Crear botón para cada slot
        # Usar una imagen genérica o texto, pero como no hay imágenes específicas, usar texto
        # Para simplicidad, usar Button con texto
        # Pero Button espera imagen, así que crear una superficie de texto
        font = pygame.font.Font(None, 36)
        text = f"Slot {i}" + (" (Guardado)" if i in slots else "")
        text_surf = font.render(text, True, BLANCO)
        # Crear un botón con la superficie de texto como imagen
        button = Button(text_surf, (ANCHO_PANTALLA // 2, start_y + (i-1) * (btn_height + spacing)))
        buttons.append(button)

    selected_index = 0
    buttons[selected_index].selected = True

    clock = pygame.time.Clock()
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_ESCAPE:
                    return None  # Cancelar
                elif event.key == pygame.K_RETURN:
                    return selected_index + 1  # Slot seleccionado (1-5)

        # --- DIBUJAR ---
        pantalla.blit(fondo, (0, 0))
        if menu_fondo:
            pantalla.blit(menu_fondo, ((ANCHO_PANTALLA - 500) // 2, (ALTO_PANTALLA - 715) // 2))

        # Dibujar título
        font_title = pygame.font.Font(None, 48)
        title_surf = font_title.render("Seleccionar Slot de Guardado", True, BLANCO)
        pantalla.blit(title_surf, (ANCHO_PANTALLA // 2 - title_surf.get_width() // 2, start_y - 100))

        for i, btn in enumerate(buttons):
            btn.selected = (i == selected_index)
            btn.update()
            btn.draw(pantalla)

        pygame.display.flip()
        clock.tick(60)
