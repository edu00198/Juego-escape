import pygame
import sys
import os
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
from .jugador_lvl2 import JugadorLvl2   # ✅ import relativo

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Mapa Ganador")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Fuente más chica
fuente = pygame.font.SysFont("Arial", 48, bold=True)

# Ruta base de las imágenes (ajusta si cambiaste carpeta)
RUTA_BASE = os.path.join("assets", "sprites_jugador lvl 2", "Run_personaje_lvl2", "run_derecha")

def cargar_animacion(ancho, alto):
    frames = []
    for i in range(1, 9):  # del 1 al 8
        ruta = os.path.join(RUTA_BASE, f"personaje_lvl2_run_derecha ({i}).png")
        imagen = pygame.image.load(ruta).convert_alpha()
        imagen = pygame.transform.scale(imagen, (ancho, alto))
        frames.append(imagen)
    return frames

def ejecutar_mapa_final():
    clock = pygame.time.Clock()
    running = True
    visible = True  # controla si se dibuja el jugador

    # Jugador más grande y más rápido
    ancho_jugador = 160   # 🔼 sprite más grande
    alto_jugador = 160
    velocidad = 5         # 🔼 más rápido

    # Cargar animación
    animacion = cargar_animacion(ancho_jugador, alto_jugador)
    frame_index = 0
    frame_timer = 0
    frame_rate = 6  # cada 6 ticks cambia de frame

    # Rect del jugador
    jugador_rect = pygame.Rect(0, ALTO_PANTALLA // 2, ancho_jugador, alto_jugador)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pantalla.fill(NEGRO)

        if visible:
            # Movimiento de izquierda a derecha
            jugador_rect.x += velocidad

            # Si llega al borde derecho, desaparece
            if jugador_rect.right >= ANCHO_PANTALLA:
                visible = False

            if visible == False:
                
                from juego.menu_pausa import pause_menu
                pause_menu(pantalla, mapa_actual=7)


            # Actualizar animación
            frame_timer += 1
            if frame_timer >= frame_rate:
                frame_timer = 0
                frame_index = (frame_index + 1) % len(animacion)

            # Dibujar jugador con frame actual
            pantalla.blit(animacion[frame_index], jugador_rect.topleft)

        # Mostrar mensaje SIEMPRE, más arriba y más chico
        texto = fuente.render("¡Haz ganado!", True, BLANCO)
        rect_texto = texto.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 4))
        pantalla.blit(texto, rect_texto)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    ejecutar_mapa_final()
