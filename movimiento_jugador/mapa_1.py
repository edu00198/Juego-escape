#mapa_1.py
import pygame
import sys
print("Importando configuración...")
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
print("Importando clase Jugador...")
from movimiento_jugador.jugador import Jugador
print("Importando recursos del mapa...")
from mapas.mapa1 import fondo_mapa, conseguir_colisiones, conseguir_puerta

print("Obteniendo colisiones del mapa...")
colisiones_mapa_1 = conseguir_colisiones(fondo_mapa)
print(f"Número de colisiones obtenidas: {len(colisiones_mapa_1)}")

def ejecutar_mapa1():
    print("Iniciando ejecución de mapa 1...")
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Juego Escape")

    print("Cargando fondo del mapa...")
    # Obtener el fondo_escalado
    fondo_escalado = pygame.transform.scale(fondo_mapa, (ANCHO_PANTALLA, ALTO_PANTALLA))

    # Calcular offset y factor de escala
    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)
    
    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2

    # Jugador - posicionado relativo al mapa
    ancho_jugador = 26
    alto_jugador = 32
    pos_x = offset_x + (fondo_mapa.get_width() * escala - ancho_jugador) // 2
    pos_y = offset_y + (fondo_mapa.get_height() * escala - alto_jugador) // 2
    
    print(f"Posición inicial del jugador: ({pos_x}, {pos_y})")
    print(f"Escala del mapa: {escala}")
    print(f"Offset del mapa: ({offset_x}, {offset_y})")
    
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR)

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        clock.tick(60)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    from mapas.menu_pausa import pause_menu
                    pause_menu(pantalla)

        # Movimiento del jugador y colisiones
        jugador.manejar_teclas()

        puerta_1 = conseguir_puerta()

        # Chequear si el jugador toca la puerta
        if jugador.rect.colliderect(puerta_1):
            from movimiento_jugador.mapa_2 import ejecutar_mapa2
            ejecutar_mapa2()

        # Limpiar pantalla
        pantalla.fill((0, 0, 0))  # Fondo negro

        # Dibujar fondo escalado
        pantalla.blit(fondo_escalado, (0, 0))

        # DEBUG: Dibujar colisiones y puerta
        for colision in colisiones_mapa_1:
            # Ajustar la posición de las colisiones con el offset
            colision_ajustada = colision.copy()
            colision_ajustada.x += offset_x
            colision_ajustada.y += offset_y
            pygame.draw.rect(pantalla, (255, 0, 0), colision_ajustada, 2)  # Rojo = colisiones

        # Ajustar la puerta con el offset
        puerta_ajustada = puerta_1.copy()
        puerta_ajustada.x += offset_x
        puerta_ajustada.y += offset_y
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_ajustada, 2)  # Azul = puerta

        # Dibujar jugador con offset
        jugador.dibujar(pantalla, offset_x, offset_y)

        # Actualizar pantalla
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    ejecutar_mapa1()
