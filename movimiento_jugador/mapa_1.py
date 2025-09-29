import pygame
import sys
import os
from .mapa_2 import ejecutar_mapa2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from movimiento_jugador.jugador import Jugador
from mapas.mapa1_data import fondo_mapa, SCALED_HEIGHT, SCALED_WIDTH, OFFSET_X, OFFSET_Y, puerta_1, colisiones_escaladas

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

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

        # Fondo del diálogo
        dialog_surface = pygame.Surface((self.dialog_rect.width, self.dialog_rect.height))
        dialog_surface.set_alpha(220)
        dialog_surface.fill((20, 20, 40))
        self.pantalla.blit(dialog_surface, self.dialog_rect.topleft)

        # Borde
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.dialog_rect, 3)

        # Título
        title_surface = self.title_font.render(self.current_title, True, (255, 215, 0))
        self.pantalla.blit(title_surface, self.title_rect.topleft)

        # Texto dividido en líneas
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

        # Dibujar texto línea por línea
        y_offset = 0
        for line in lines:
            if y_offset + self.font.get_linesize() <= self.text_rect.height:
                text_surface = self.font.render(line, True, (255, 255, 255))
                self.pantalla.blit(text_surface, (self.text_rect.left, self.text_rect.top + y_offset))
                y_offset += self.font.get_linesize()

        # Indicador para continuar
        indicator = self.font.render("Espacio/Enter para continuar...", True, (200, 200, 200))
        self.pantalla.blit(indicator, (self.dialog_rect.right - indicator.get_width() - 20, self.dialog_rect.bottom - 30))


# =============================
# Ejecutar Mapa
# =============================
def ejecutar_mapa1():
    clock = pygame.time.Clock()
    running = True
    dialog_system = DialogSystem(pantalla)

    # Historia inicial
    intro_texts = [
        "Hace mucho tiempo, en un reino lejano, un valiente aventurero inició su misión.",
        "Las leyendas hablan de una reliquia mágica en lo profundo de un castillo.",
        "Tu aventura comienza aquí, en la entrada de este misterioso lugar..."
    ]
    dialog_system.start_dialog(intro_texts, "El Comienzo de la Aventura")

    # Posición inicial fija del jugador (centrado)
    ancho_jugador, alto_jugador = 23, 15
    pos_x = (ANCHO_PANTALLA - ancho_jugador) // 2
    pos_y = (ALTO_PANTALLA - alto_jugador) // 2

    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador,
                      escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)

    # Fondo escalado
    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    puerta_dialog_shown = False
    puerta_abierta = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Manejo de diálogos
            if dialog_system.handle_input(event):
                if puerta_dialog_shown:
                    puerta_abierta = True

        # Movimiento solo si no hay diálogo activo
        if not dialog_system.active:
            jugador.manejar_teclas()

        # ---------------------------
        # Dibujar fondo y jugador
        # ---------------------------
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
        jugador.dibujar(pantalla, 0, 0)
        dialog_system.draw()  # cuadro de diálogo encima

        # Detectar colisión con la puerta y mostrar diálogo
        if not dialog_system.active and not puerta_dialog_shown and jugador.rect.colliderect(puerta_1):
            puerta_dialog_shown = True
            puerta_texts = [
                "Has encontrado una puerta misteriosa.",
                "Un aura mágica emana de ella...",
                "Te preguntas qué habrá al otro lado..."
            ]
            dialog_system.start_dialog(puerta_texts, "Puerta Misteriosa")

        # Cambiar de mapa solo después de cerrar el diálogo
        if puerta_abierta and jugador.rect.colliderect(puerta_1):
            ejecutar_mapa2()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    ejecutar_mapa1()
