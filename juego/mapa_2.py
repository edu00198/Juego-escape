# mapa_2.py
import pygame
import sys
import os
from juego.mapa_3 import ejecutar_mapa3
from juego.menu_pausa import pause_menu

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador
from assets.mapas.mapa2_data import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT, 
    OFFSET_X,
    OFFSET_Y,
    puerta_2_entrada,
    puerta_2_salida,
    colisiones_escaladas
)


pantalla = pygame.display.set_mode((1280, 720))

# =============================
# Sistema de Diálogo (copiado de mapa_1)
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

def ejecutar_mapa2():
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 23
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)

    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2 

    
    puerta2pos = puerta_2_entrada.topleft
    pos_x = puerta2pos[0]
    pos_y = puerta2pos[1] - alto_jugador * 10
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)


    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_pared = os.path.join(BASE_DIR,"assets", "mapas", "pared_mapa_2.png")

    # Cargar imagen
    imagen_pared = pygame.image.load(ruta_pared).convert_alpha()

    # Escalar si querés adaptarla al tamaño de pantalla
    imagen_escalada = pygame.transform.scale(imagen_pared, (1280, 720))


    # Mensaje de felicitación al entrar a mapa2
    dialog_system = DialogSystem(pantalla)
    congrat_texts = [
    "El aire se vuelve más denso mientras avanzás.",
    "Las antorchas parecen encenderse solas, una a una, marcando el camino.",
    "???: Veo que lograste abrir la puerta...",
    "Jugador: Seguí tu voz. No me dejas muchas opciones.",
    "???: La salida está más cerca... pero también lo está aquello que la protege.",
    "Jugador: ¿Aquello?",
    "???: No lo nombres. Aquí, las cosas que se nombran despiertan.",
    "Un silencio pesado llena el pasillo. El eco de tus pasos se mezcla con un susurro distante."
]

    dialog_system.start_dialog(congrat_texts, "¡Bien hecho!")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Al presionar ESC abrir menú de pausa
                if event.key == pygame.K_ESCAPE:
                    # Preparar estado mínimo para guardar (sprite_pos si existe)
                    try:
                        state = {
                            'mapa': 'mapa2',
                            'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y)
                        }
                    except Exception:
                        state = None
                    pause_menu(pantalla, mapa_actual=2, state=state)

            dialog_system.handle_input(event)

        jugador.manejar_teclas()

        pantalla.fill((0, 0, 0))  # Limpiar pantalla
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))  # Fondo del mapa
        # ...existing code...
        jugador.dibujar(pantalla, offset_x, offset_y)
        pantalla.blit(imagen_escalada, (0, 0))

        dialog_system.draw()

        pygame.display.flip()
        clock.tick(60)

        # Transiciones de mapa
        if jugador.rect.colliderect(puerta_2_salida):
            print("Transición al mapa 3")
            running = False
            ejecutar_mapa3()

    pygame.quit()
    sys.exit()
