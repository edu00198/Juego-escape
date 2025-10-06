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


pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Estado global para persistir el código correcto entre mapas
codigo_ya_ingresado = False


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
        if self.active and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.current_index += 1
                if self.current_index >= len(self.dialogs):
                    self.active = False
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
        "Hace mucho tiempo, en un reino lejano, un valiente aventurero inició su misión.",
        "Las leyendas hablan de una reliquia mágica en lo profundo de un castillo.",
        "Tu aventura comienza aquí, en la entrada de este misterioso lugar...",
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

    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))
    sistema_cofres = SistemaLlavesCofres(codigo_secreto=str(random.randint(1000, 9999)))
    sistema_cofres.agregar_llave(175, 325)
    sistema_cofres.agregar_cofre(1125, 200)
    sistema_cofres.agregar_carta("Bienvenido al escape de la mazmorra!")
    sistema_cofres.crear_panel_codigo(ANCHO_PANTALLA, ALTO_PANTALLA)

    # -------------------------------
    # REINICIAR ESTADO DE INTERFACES
    # -------------------------------
    global codigo_ya_ingresado
    sistema_cofres.codigo_correcto = codigo_ya_ingresado
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
                    pause_menu(pantalla)
                else:
                    resultado = sistema_cofres.manejar_eventos(event)
                    if resultado == "codigo_correcto":
                        ejecutar_mapa2()
                        # Move player back from the door to avoid immediate re-trigger
                        jugador.rect.y -= 10
                        # Reset interfaces after returning from mapa2
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
        jugador.dibujar(pantalla, 0, 0)
        dialog_system.draw()

        # Detectar colisión con la puerta
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
                jugador.rect.y += 5  # retroceso visual
            elif not sistema_cofres.codigo_correcto:
                if not sistema_cofres.panel_codigo.visible:
                    sistema_cofres.mostrar_panel_codigo(jugador.rect.centerx, jugador.rect.centery)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    ejecutar_mapa1()
