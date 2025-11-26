import pygame
import sys
import os
import fnmatch
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, m1_opciones, m2_opciones, m3_opciones, m4_opciones, m4_2_opciones
from intro_y_menu.menu.button import Button
from intro_y_menu.menu.settings import settings_menu
# Removed top-level import of menus to avoid circular import.
# We'll import menus() locally when needed to prevent circular import errors.
from assets.mapas.fondo import resume_button, help_button, settings_button, save_button, quit_button, menu_pause
from .save_system import save_game, list_saves
NEGRO = (0, 0, 0)   
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
        elif mapa_actual == 3:
            fondo = pygame.image.load(m3_opciones).convert()
        elif mapa_actual == 4:
            fondo = pygame.image.load(m4_opciones).convert()
        elif mapa_actual == 5:
            fondo = pygame.image.load(m4_opciones).convert()
        elif mapa_actual == 6:
            fondo = pygame.image.load(m4_2_opciones).convert()
        else:
            raise ValueError("Mapa no válido")
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        fondo.fill(NEGRO)

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

    # Mensajes temporales en pantalla (texto, tiempo_inicio, duracion_ms)
    message = None
    message_start = 0
    message_dur = 2000  # ms

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

                elif event.key == pygame.K_ESCAPE and not mapa_actual == 7:
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
                                # Mostrar mensaje de guardado exitoso y regresar al juego
                                # No salir al menú principal
                                # Agregar mensaje temporal en pantalla
                                message = f"Partida guardada en slot {slot}"
                                message_start = pygame.time.get_ticks()
                                message_dur = 2000  # ms
                                # Dibujar mensaje en el loop
                        else:
                            print("No hay estado para guardar.")
                    elif clicked_button == ayuda_button:
                        print("Abrir ayuda...")
                    elif clicked_button == config_button:
                        settings_menu(pantalla)
                    elif clicked_button == salir_button:
                        # Importar menus() localmente para evitar import circular / NameError
                        try:
                            from intro_y_menu.menu.menuzaso import menus
                        except Exception as e:
                            print(f"No se pudo importar menus(): {e}")
                        else:
                            try:
                                menus()
                            except Exception as e:
                                print(f"Error al ejecutar menus(): {e}")

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

        # Mostrar mensaje temporal si existe
        if message:
            now = pygame.time.get_ticks()
            if now - message_start <= message_dur:
                msg_font = pygame.font.Font(None, 30)
                msg_surf = msg_font.render(message, True, (100, 255, 100))
                pantalla.blit(msg_surf, (ANCHO_PANTALLA // 2 - msg_surf.get_width() // 2, start_y + btn_height * 5 + 50))
            else:
                message = None

        pygame.display.flip()
        clock.tick(60)


# Helper: rutas donde buscar archivos de guardado
def _get_save_dirs():
    here = os.path.dirname(__file__)
    return [
        os.path.join(here, 'saves'),
        os.path.normpath(os.path.join(here, '..', 'saves')),
        here,
        os.path.normpath(os.path.join(here, '..')),
    ]

# Helper: comprobar si un slot tiene guardado (intenta list_saves y archivos)
def _has_save(slot, raw_slots):
    # raw_slots puede ser None, lista de ints o lista de nombres/paths
    if not raw_slots:
        raw_slots = []
    # revisar elementos que sean ints o que contengan el número de slot
    for entry in raw_slots:
        try:
            if int(entry) == slot:
                return True
        except Exception:
            # tratar como string
            if str(slot) in str(entry):
                return True
    # buscar archivos en rutas comunes
    for d in _get_save_dirs():
        try:
            if not os.path.isdir(d):
                continue
            for name in os.listdir(d):
                # patrones comunes: slot_1.sav, slot1.sav, save_slot1.*, *1.sav
                if fnmatch.fnmatch(name.lower(), f"*slot*{slot}*.sav") or \
                   fnmatch.fnmatch(name.lower(), f"*_{slot}.sav") or \
                   fnmatch.fnmatch(name.lower(), f"*{slot}*.sav") or \
                   fnmatch.fnmatch(name.lower(), f"slot{slot}.*"):
                    return True
        except Exception:
            continue
    return False

# Helper: eliminar archivo/entrada del slot; devuelve True si algo fue eliminado
def _delete_save_slot(slot, raw_slots):
    deleted_any = False
    # intentar usar delete_save de save_system si está disponible
    try:
        from .save_system import delete_save
        try:
            delete_save(slot)
            return True
        except Exception:
            # si falla, continuamos con fallback
            pass
    except Exception:
        pass

    # fallback: eliminar archivos en rutas comunes que correspondan al slot
    for d in _get_save_dirs():
        try:
            if not os.path.isdir(d):
                continue
            for name in os.listdir(d):
                lcn = name.lower()
                # patrones comunes
                if fnmatch.fnmatch(lcn, f"*slot*{slot}*.sav") or \
                   fnmatch.fnmatch(lcn, f"*_{slot}.sav") or \
                   fnmatch.fnmatch(lcn, f"*{slot}*.sav") or \
                   fnmatch.fnmatch(lcn, f"slot{slot}.*"):
                    path = os.path.join(d, name)
                    try:
                        os.remove(path)
                        deleted_any = True
                    except Exception:
                        # intentar renombrar para "liberar" si no se puede borrar
                        try:
                            os.rename(path, path + ".deleted")
                            deleted_any = True
                        except Exception:
                            pass
        except Exception:
            continue

    # adicional: si list_saves devuelve nombres que podemos interpretar y eliminar, intentar eliminar referencias
    # (esto depende de la implementación de list_saves; si es puramente informativa, ya manejamos borrado de archivos)
    return deleted_any

# Reemplazo de select_save_slot con manejo robusto de eliminación (R) y refresco UI
def select_save_slot(pantalla, mapa_actual):
    """
    Submenú para seleccionar el slot de guardado.
    Permite eliminar un slot con la tecla R (libera el slot).
    """
    # --- FONDO SEGÚN EL MAPA ---
    try:
        if mapa_actual == 1:
            fondo = pygame.image.load(m1_opciones).convert()
        elif mapa_actual == 2:
            fondo = pygame.image.load(m2_opciones).convert()
        else:
            # Para mapa 3 y superiores usar el mismo recurso (m3_opciones)
            fondo = pygame.image.load(m3_opciones).convert()
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

    # obtener raw_slots (lo que devuelva list_saves)
    try:
        raw_slots = list_saves() or []
    except Exception:
        raw_slots = []

    # construir lista booleana de existencia por slot (1..5)
    exists = [False] * 5
    for i in range(1, 6):
        try:
            exists[i-1] = _has_save(i, raw_slots)
        except Exception:
            exists[i-1] = False

    # crear botones con texto dinámico
    buttons = []
    font = pygame.font.Font(None, 36)
    for i in range(1, 6):
        text = f"Slot {i}" + (" (Guardado)" if exists[i-1] else "")
        text_surf = font.render(text, True, BLANCO)
        btn = Button(text_surf, (ANCHO_PANTALLA // 2, start_y + (i-1) * (btn_height + spacing)))
        buttons.append(btn)

    selected_index = 0
    buttons[selected_index].selected = True

    clock = pygame.time.Clock()
    selecting = True

    # Mensajes temporales en pantalla (texto, tiempo_inicio, duracion_ms)
    message = None
    message_start = 0
    message_dur = 1500  # ms

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

                # --- ELIMINAR SLOT CON R ---
                elif event.key == pygame.K_r:
                    target_slot = selected_index + 1
                    if exists[target_slot - 1]:
                        deleted = False
                        try:
                            deleted = _delete_save_slot(target_slot, raw_slots)
                        except Exception as e:
                            print(f"Error al eliminar slot {target_slot}: {e}")
                            deleted = False

                        # refrescar existencia usando list_saves y comprobación por archivos
                        try:
                            raw_slots = list_saves() or []
                        except Exception:
                            raw_slots = []
                        for i in range(1, 6):
                            exists[i-1] = _has_save(i, raw_slots)

                        # actualizar textos de botones
                        for idx, btn in enumerate(buttons):
                            txt = f"Slot {idx+1}" + (" (Guardado)" if exists[idx] else "")
                            txt_surf = font.render(txt, True, BLANCO)
                            btn.image = txt_surf
                            btn.rect = btn.image.get_rect(center=(ANCHO_PANTALLA // 2, start_y + idx * (btn_height + spacing)))

                        if deleted:
                            message = f"Slot {target_slot} eliminado"
                            message_start = pygame.time.get_ticks()
                            # liberar el slot y mantener el cursor en misma posición (ahora puede quedar vacío)
                        else:
                            message = f"No se pudo eliminar slot {target_slot}"
                            message_start = pygame.time.get_ticks()
                    else:
                        message = f"Slot {target_slot} está vacío"
                        message_start = pygame.time.get_ticks()

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

        # Mostrar mensaje temporal si existe
        if message:
            now = pygame.time.get_ticks()
            if now - message_start <= message_dur:
                msg_font = pygame.font.Font(None, 30)
                msg_surf = msg_font.render(message, True, (255, 100, 100))
                pantalla.blit(msg_surf, (ANCHO_PANTALLA // 2 - msg_surf.get_width() // 2, start_y + btn_height * 5 + 50))
            else:
                message = None

        pygame.display.flip()
        clock.tick(60)
