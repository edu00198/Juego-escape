import pygame
import os
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, ESCALA_JUGADOR
from .jugador import Jugador
from .colisiones import colisiones, detectar_colision, dibujar_colisiones

def ejecutar_juego():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("movimiento_jugador")

    from configuracion import fondo_1  
    ruta_fondo = fondo_1
    try:
        fondo = pygame.image.load(ruta_fondo).convert()  
        fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))  
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = None

    ancho_jugador = 50
    alto_jugador = 50
    pos_x = (ANCHO_PANTALLA - ancho_jugador) // 2
    pos_y = (ALTO_PANTALLA - alto_jugador) // 2
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR)

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        reloj.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        jugador.manejar_teclas()
        pantalla.fill((0,0,0))
        dibujar_colisiones(pantalla)
        pygame.display.flip()

        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(BLANCO)  
        
        
        jugador.dibujar(pantalla)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    ejecutar_juego()
