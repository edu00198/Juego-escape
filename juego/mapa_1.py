import pygame
import sys
import os
import random

# Ajustes de paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR, BLANCO
from juego.jugador import Jugador
from assets.mapas.mapa1_data import (
    fondo_mapa,
    SCALED_HEIGHT,
    SCALED_WIDTH,
    OFFSET_X,
    OFFSET_Y,
    puerta_1,
    colisiones_escaladas,
)
from .puzzle_cofre import SistemaLlavesCofres
from .menu_pausa import pause_menu
from .mapa_2 import ejecutar_mapa2
from . import puzzle_cofre
from .save_system import save_game


def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')



pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Usamos la variable persistente definida en `juego.puzzle_cofre` para saber
# si el código ya fue ingresado en sesiones anteriores.


# =============================
# Sistema de Diálogo
# =============================
class DialogSystem:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
        self.active = False
        self.dialogs = []
        self.current_index = 0
        self.current_title = ""
        self.dialog_rect = pygame.Rect(50, 450, 1180, 220)
        self.text_rect = pygame.Rect(70, 490, 1140, 140)
        self.title_rect = pygame.Rect(70, 460, 500, 30)

    def start_dialog(self, dialogs, title="Historia"):
        self.dialogs = dialogs
        self.current_index = 0
        self.current_title = title
        self.active = True

    def handle_input(self, event):
        if not self.active:
            return False

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.current_index += 1
            if self.current_index >= len(self.dialogs):
                self.active = False
                # Limpiar solo eventos específicos del diálogo para evitar efectos secundarios
                for e in pygame.event.get([pygame.K_SPACE, pygame.K_RETURN]):
                    pass
                return True
        return False

    def draw(self):
        if not self.active or self.current_index >= len(self.dialogs):
            return

        dialog_surface = pygame.Surface((self.dialog_rect.width, self.dialog_rect.height))
        dialog_surface.set_alpha(220)
        dialog_surface.fill((20, 20, 40))
        self.pantalla.blit(dialog_surface, self.dialog_rect.topleft)

        pygame.draw.rect(self.pantalla, (255, 255, 255), self.dialog_rect, 3)

        title_surface = self.title_font.render(self.current_title, True, (255, 215, 0))
        self.pantalla.blit(title_surface, self.title_rect.topleft)

        text = self.dialogs[self.current_index]
        words = text.split(" ")
        lines, current_line = [], ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < self.text_rect.width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())

        y_offset = 0
        for line in lines:
            if y_offset + self.font.get_linesize() <= self.text_rect.height:
                text_surface = self.font.render(line, True, (255, 255, 255))
                self.pantalla.blit(text_surface, (self.text_rect.left, self.text_rect.top + y_offset))
                y_offset += self.font.get_linesize()

        indicator = self.font.render("Espacio/Enter para continuar...", True, (200, 200, 200))
        self.pantalla.blit(
            indicator,
            (self.dialog_rect.right - indicator.get_width() - 20, self.dialog_rect.bottom - 30),
        )


# =============================
# Ejecutar Mapa 1
# =============================
def ejecutar_mapa1():
    clock = pygame.time.Clock()
    running = True
    dialog_system = DialogSystem(pantalla)
    has_moved = False

    # Historia inicial
    intro_texts = [
    "…¿Dónde… estoy?",
    "Las paredes húmedas, el aire… pesado.",
    "???: veo que despertaste.",
    "Jugador: ¿Quién habla? Muéstrate.",
    "???: No temas. Todos buscan escapar",
    "Jugador: ¿Donde esta la salida? ",
    "???: Más allá de estas puertas, pero no todo lo que brilla esoro"
]


    escala_x = SCALED_WIDTH / fondo_mapa.get_width()
    escala_y = SCALED_HEIGHT / fondo_mapa.get_height()
    escala_fondo = min(escala_x, escala_y)

    puerta_1_scaled = puerta_1
    colisiones_escaladas_scaled = colisiones_escaladas

    ancho_jugador, alto_jugador = 23, 15
    pos_x = (ANCHO_PANTALLA - ancho_jugador) // 2
    pos_y = (ALTO_PANTALLA - alto_jugador) // 2

    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador,
                      escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas_scaled)

    # Normalize loaded position: detect whether saved pos corresponds to
    # sprite_pos (visual position) or to rect coordinates (older saves).
    saved_x, saved_y = pos_x, pos_y

    # Default offsets used by Jugador for rect relative to sprite_pos
    offset_x = 58
    offset_y = 101

    # If the rect computed from sprite_pos is noticeably outside the visible map area,
    # assume the saved values were rect coordinates. Otherwise keep as sprite_pos.
    map_left = OFFSET_X
    map_top = OFFSET_Y
    map_right = OFFSET_X + SCALED_WIDTH
    map_bottom = OFFSET_Y + SCALED_HEIGHT

    rect_out_of_bounds = (
        jugador.rect.right < map_left or jugador.rect.left > map_right or
        jugador.rect.bottom < map_top or jugador.rect.top > map_bottom
    )

    if rect_out_of_bounds:
        # Interpret saved values as rect coordinates
        try:
            jugador.rect.topleft = (int(saved_x), int(saved_y))
            # Recompute sprite_pos from rect using the known offsets
            jugador.sprite_pos.x = jugador.rect.x - offset_x
            jugador.sprite_pos.y = jugador.rect.y - offset_y
        except Exception:
            # Fallback to clamping sprite_pos inside map
            jugador.sprite_pos.x = max(map_left, min(jugador.sprite_pos.x, map_right))
            jugador.sprite_pos.y = max(map_top, min(jugador.sprite_pos.y, map_bottom))

    # Clamp rect within visible map bounds and sync sprite_pos to avoid breaking collisions/drawing
    old_rect_topleft = jugador.rect.topleft
    jugador.rect.left = max(map_left, min(jugador.rect.left, map_right - jugador.rect.width))
    jugador.rect.top = max(map_top, min(jugador.rect.top, map_bottom - jugador.rect.height))
    jugador.sprite_pos.x = jugador.rect.x - offset_x
    jugador.sprite_pos.y = jugador.rect.y - offset_y

    
    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))
    codigo_secreto = str(random.randint(1000, 9999))
    sistema_cofres = SistemaLlavesCofres(codigo_secreto=codigo_secreto)
    sistema_cofres.agregar_llave(175, 325)
    sistema_cofres.agregar_cofre(1125, 200)
    sistema_cofres.agregar_carta("Bienvenido al escape de la mazmorra!")
    sistema_cofres.crear_panel_codigo((ANCHO_PANTALLA - 400) // 2, (ALTO_PANTALLA - 300) // 2)


    # -------------------------------
    # REINICIAR ESTADO DE INTERFACES
    # -------------------------------
    # Restore the persisted code-correct flag from the puzzle module
    sistema_cofres.codigo_correcto = puzzle_cofre.codigo_ya_ingresado
    if sistema_cofres.panel_codigo:
        sistema_cofres.panel_codigo.ocultar()
    for carta in sistema_cofres.cartas:
        carta.ocultar()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not sistema_cofres.hay_interfaz_visible():
                    # Preparar estado para guardar
                    # Save sprite_pos (visual position) rather than collision rect
                    state = {
                        'mapa': 'mapa1',
                        'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y),
                        'cofres_abiertos': [c.abierto for c in sistema_cofres.cofres],
                        'codigo_correcto': sistema_cofres.codigo_correcto,
                        'llaves_encontradas': sistema_cofres.llaves_encontradas,
                        'codigo_secreto': sistema_cofres.codigo_secreto,
                        'has_moved': has_moved
                    }
                    pause_menu(pantalla, mapa_actual=1, state=state)
                else:
                    # If SPACE is pressed while colliding with the door and a cofre is opened,
                    # open the code panel. Do not forward this event to the UI handlers so
                    # the panel doesn't immediately react to the same SPACE press.
                    skip_forward = False
                    if event.key == pygame.K_SPACE:
                        cerca_puerta = jugador.rect.colliderect(puerta_1_scaled)
                        hay_cofre_abierto = any(c.abierto for c in sistema_cofres.cofres)
                        panel_visible = sistema_cofres.panel_codigo and sistema_cofres.panel_codigo.visible
                        # DEBUG: mostrar estado para diagnosticar transiciones
                        #print(f"DEBUG SPACE: cerca_puerta={cerca_puerta}, hay_cofre_abierto={hay_cofre_abierto}, panel_visible={panel_visible}, codigo_correcto={sistema_cofres.codigo_correcto}")
                        # Más info: rects (jugador vs puerta)
                        
                        # Allow leaving to mapa2 if either a cofre is open (fresh session)
                        # or if the code was already entered in a previous session.
                        if cerca_puerta and (hay_cofre_abierto or sistema_cofres.codigo_correcto):
                            if sistema_cofres.codigo_correcto:
                                # Código ya ingresado: pasar a mapa2 (no retorno a mapa1)
                                limpiar_terminal()
                                ejecutar_mapa2()
                                # Ensure interfaces reset (no return to mapa1)
                                if sistema_cofres.panel_codigo:
                                    sistema_cofres.panel_codigo.ocultar()
                                for carta in sistema_cofres.cartas:
                                    carta.ocultar()
                                skip_forward = True
                            elif not panel_visible:
                                # Abrir panel para ingresar código
                                sistema_cofres.mostrar_panel_codigo(jugador.rect.centerx, jugador.rect.centery)
                                skip_forward = True

                    if not skip_forward:
                        resultado = sistema_cofres.manejar_eventos(event)
                        if resultado == "codigo_correcto":
                            # Autoguardado antes de pasar a mapa2
                            state = {
                                'mapa': 'mapa2',
                                # save sprite position
                                'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y),
                                'cofres_abiertos': [c.abierto for c in sistema_cofres.cofres],
                                'codigo_correcto': True,
                                'llaves_encontradas': sistema_cofres.llaves_encontradas,
                                'codigo_secreto': sistema_cofres.codigo_secreto,
                                'has_moved': has_moved
                            }
                            save_game(state)
                            ejecutar_mapa2()
                            # Reset interfaces after going to mapa2 (no return to mapa1)
                            if sistema_cofres.panel_codigo:
                                sistema_cofres.panel_codigo.ocultar()
                            for carta in sistema_cofres.cartas:
                                carta.ocultar()

            if dialog_system.handle_input(event):
                pygame.event.clear()

        if not dialog_system.active and not sistema_cofres.hay_interfaz_visible():
            pos_anterior = jugador.rect.topleft
            jugador.manejar_teclas()

            colision_pared = any(jugador.rect.colliderect(rect) for rect in colisiones_escaladas_scaled)
            colision_cofre = any((not cofre.abierto) and jugador.rect.colliderect(cofre.rect) for cofre in sistema_cofres.cofres)
            if colision_pared or (colision_cofre and sistema_cofres.llaves_encontradas == 0):
                jugador.rect.topleft = pos_anterior

            resultado = sistema_cofres.verificar_colisiones(jugador.rect)

            if not has_moved and pos_anterior != jugador.rect.topleft:
                has_moved = True
                dialog_system.start_dialog(intro_texts, "El Comienzo de la Aventura")

        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
        sistema_cofres.dibujar(pantalla)
        # Si el panel para insertar el código está visible, NO dibujar al jugador
        panel_visible = sistema_cofres.panel_codigo and sistema_cofres.panel_codigo.visible
        if not panel_visible:
            jugador.dibujar(pantalla, 0, 0)
        dialog_system.draw()

        # Detectar colisión con la puerta
        if jugador.rect.colliderect(puerta_1_scaled):
            if not any(c.abierto for c in sistema_cofres.cofres):
                if not dialog_system.active:
                    dialog_system.start_dialog(
                        [
                            "La puerta está sellada. Encuentra la llave y abre el cofre para continuar..."
                        ],
                        "Puerta Cerrada"
                    )
                jugador.rect.y += 5  # retroceso visual
            elif not sistema_cofres.codigo_correcto:
                # No abrir automáticamente el panel. Mostrar una pista para presionar SPACE
                # si hay al menos un cofre abierto y el código no fue ingresado.
                pass

        # Mostrar pista en pantalla para abrir el panel con SPACE
        cerca_puerta = jugador.rect.colliderect(puerta_1_scaled)
        hay_cofre_abierto = any(c.abierto for c in sistema_cofres.cofres)
        panel_visible = sistema_cofres.panel_codigo and sistema_cofres.panel_codigo.visible
        if cerca_puerta and hay_cofre_abierto and not sistema_cofres.codigo_correcto and not panel_visible:
            # Dibuja una pequeña instrucción sobre el jugador
            font_hint = pygame.font.Font(None, 28)
            hint_surf = font_hint.render("Presiona ESPACIO para ingresar el código", True, (255, 255, 255))
            hint_rect = hint_surf.get_rect(center=(jugador.rect.centerx, jugador.rect.top - 20))
            pantalla.blit(hint_surf, hint_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def ejecutar_mapa1_con_estado(state):
    """Ejecuta mapa1 cargando el estado guardado."""
    clock = pygame.time.Clock()
    running = True
    dialog_system = DialogSystem(pantalla)
    has_moved = False

    # Historia inicial (solo si no ha movido)
    intro_texts = [
    "…¿Dónde… estoy?",
    "Solo escuchás gotas cayendo. Las paredes están húmedas, el aire… pesado.",
    "???: Despertaste al fin. Pocos recuerdan su nombre aquí.",
    "Jugador: ¿Quién habla? Muéstrate.",
    "???: No temas. Soy la voz de lo que fue este lugar.",
    "???: Todos los que entran buscan escapar, pero solo los que escuchan… encuentran la salida.",
    "Jugador: ¿La salida? ¿Dónde está?",
    "???: Más allá de estas puertas, cada una custodiada por pruebas y mentiras.",
    "Jugador: Entonces seguiré adelante.",
    "???: Recordá esto, aventurero: no todo lo que brilla te ayudará… y no todo lo que calla está muerto."
]

    escala_x = SCALED_WIDTH / fondo_mapa.get_width()
    escala_y = SCALED_HEIGHT / fondo_mapa.get_height()
    escala_fondo = min(escala_x, escala_y)

    puerta_1_scaled = puerta_1
    colisiones_escaladas_scaled = colisiones_escaladas

    ancho_jugador, alto_jugador = 23, 15
    # Expect saved 'pos_jugador' to be the sprite_pos (x,y). Provide defaults if missing.
    default_pos = ((ANCHO_PANTALLA - ancho_jugador) // 2, (ALTO_PANTALLA - alto_jugador) // 2)
    pos_x, pos_y = state.get('pos_jugador', default_pos)

    # Create jugador using sprite position
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador,
                      escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas_scaled)

    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))
    codigo_secreto = state.get('codigo_secreto', str(random.randint(1000, 9999)))
    sistema_cofres = SistemaLlavesCofres(codigo_secreto=codigo_secreto)
    sistema_cofres.agregar_llave(175, 325)
    sistema_cofres.agregar_cofre(1125, 200)
    sistema_cofres.agregar_carta("Bienvenido al escape de la mazmorra!")
    sistema_cofres.crear_panel_codigo((ANCHO_PANTALLA - 400) // 2, (ALTO_PANTALLA - 300) // 2)

    # Restaurar estado
    cofres_abiertos = state.get('cofres_abiertos', [])
    for i, abierto in enumerate(cofres_abiertos):
        if i < len(sistema_cofres.cofres):
            sistema_cofres.cofres[i].abierto = abierto
    sistema_cofres.codigo_correcto = state.get('codigo_correcto', False)
    sistema_cofres.llaves_encontradas = state.get('llaves_encontradas', 0)
    has_moved = state.get('has_moved', False)
    puzzle_cofre.codigo_ya_ingresado = sistema_cofres.codigo_correcto

    # Ensure consistency: if any chest is open, the key must have been found
    if any(c.abierto for c in sistema_cofres.cofres):
        sistema_cofres.llaves_encontradas = max(sistema_cofres.llaves_encontradas, 1)

    # Mark key objects as found so they are not drawn again
    if sistema_cofres.llaves_encontradas > 0:
        for i in range(min(sistema_cofres.llaves_encontradas, len(sistema_cofres.llaves))):
            sistema_cofres.llaves[i].encontrada = True

    if sistema_cofres.panel_codigo:
        sistema_cofres.panel_codigo.ocultar()
    for carta in sistema_cofres.cartas:
        carta.ocultar()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not sistema_cofres.hay_interfaz_visible():
                    # Preparar estado para guardar (usar sprite_pos)
                    state = {
                        'mapa': 'mapa1',
                        'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y),
                        'cofres_abiertos': [c.abierto for c in sistema_cofres.cofres],
                        'codigo_correcto': sistema_cofres.codigo_correcto,
                        'llaves_encontradas': sistema_cofres.llaves_encontradas,
                        'codigo_secreto': sistema_cofres.codigo_secreto,
                        'has_moved': has_moved
                    }
                    pause_menu(pantalla, mapa_actual=1, state=state)
                else:
                    skip_forward = False
                    if event.key == pygame.K_SPACE:
                        cerca_puerta = jugador.rect.colliderect(puerta_1_scaled)
                        hay_cofre_abierto = any(c.abierto for c in sistema_cofres.cofres)
                        panel_visible = sistema_cofres.panel_codigo and sistema_cofres.panel_codigo.visible
                        if cerca_puerta and (hay_cofre_abierto or sistema_cofres.codigo_correcto):
                            if sistema_cofres.codigo_correcto:
                                ejecutar_mapa2()
                                if sistema_cofres.panel_codigo:
                                    sistema_cofres.panel_codigo.ocultar()
                                for carta in sistema_cofres.cartas:
                                    carta.ocultar()
                                skip_forward = True
                            elif not panel_visible:
                                sistema_cofres.mostrar_panel_codigo(jugador.rect.centerx, jugador.rect.centery)
                                skip_forward = True

                    if not skip_forward:
                        resultado = sistema_cofres.manejar_eventos(event)
                        if resultado == "codigo_correcto":
                            state = {
                                'mapa': 'mapa2',
                                'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y),
                                'cofres_abiertos': [c.abierto for c in sistema_cofres.cofres],
                                'codigo_correcto': True,
                                'llaves_encontradas': sistema_cofres.llaves_encontradas,
                                'codigo_secreto': sistema_cofres.codigo_secreto,
                                'has_moved': has_moved
                            }
                            save_game(state)
                            ejecutar_mapa2()
                            if sistema_cofres.panel_codigo:
                                sistema_cofres.panel_codigo.ocultar()
                            for carta in sistema_cofres.cartas:
                                carta.ocultar()

            if dialog_system.handle_input(event):
                pygame.event.clear()

        if not dialog_system.active and not sistema_cofres.hay_interfaz_visible():
            pos_anterior = jugador.rect.topleft
            jugador.manejar_teclas()

            colision_pared = any(jugador.rect.colliderect(rect) for rect in colisiones_escaladas_scaled)
            colision_cofre = any((not cofre.abierto) and jugador.rect.colliderect(cofre.rect) for cofre in sistema_cofres.cofres)
            if colision_pared or (colision_cofre and sistema_cofres.llaves_encontradas == 0):
                jugador.rect.topleft = pos_anterior

            resultado = sistema_cofres.verificar_colisiones(jugador.rect)

            if not has_moved and pos_anterior != jugador.rect.topleft:
                has_moved = True
                dialog_system.start_dialog(intro_texts, "El Comienzo de la Aventura")

        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
        sistema_cofres.dibujar(pantalla)
        panel_visible = sistema_cofres.panel_codigo and sistema_cofres.panel_codigo.visible
        # Dibujar al jugador siempre que no esté visible el panel de código
        # y el diálogo no esté activo
        if not panel_visible and not dialog_system.active:
            jugador.dibujar(pantalla, 0, 0)
        dialog_system.draw()

        if jugador.rect.colliderect(puerta_1_scaled):
            if not any(c.abierto for c in sistema_cofres.cofres):
                if not dialog_system.active:
                    dialog_system.start_dialog(
                        [
                            "La puerta está sellada.",
                            "Necesitas encontrar la llave y abrir el cofre antes de continuar..."
                        ],
                        "Puerta Cerrada"
                    )
                jugador.rect.y += 5
            elif not sistema_cofres.codigo_correcto:
                pass

        cerca_puerta = jugador.rect.colliderect(puerta_1_scaled)
        hay_cofre_abierto = any(c.abierto for c in sistema_cofres.cofres)
        panel_visible = sistema_cofres.panel_codigo and sistema_cofres.panel_codigo.visible
        if cerca_puerta and hay_cofre_abierto and not sistema_cofres.codigo_correcto and not panel_visible:
            font_hint = pygame.font.Font(None, 28)
            hint_surf = font_hint.render("Presiona ESPACIO para ingresar el código", True, (255, 255, 255))
            hint_rect = hint_surf.get_rect(center=(jugador.rect.centerx, jugador.rect.top - 20))
            pantalla.blit(hint_surf, hint_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    ejecutar_mapa1()
