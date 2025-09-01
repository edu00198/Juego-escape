"""este codigo define las colisiones"""
import pygame

  


# Lista de rectángulos de colisión
colisiones = [
    pygame.Rect(0, 0, 320, 270), #cuadrado arriba a la derecha/ celda

    pygame.Rect(0, 270, 60, 400), # borde izq
    pygame.Rect(1220, 130, 60, 550),#borde derecha

    pygame.Rect(320, 0, 340, 150),# borde superior izq
    pygame.Rect(750, 0, 530, 150),# borde superior der
    
    pygame.Rect(60, 660, 1200, 40),# borde inferior

    pygame.Rect(860, 480, 370, 190),  # cajas der

    pygame.Rect(660, 0, 90, 20)  # parte atras cajas
]

puerta = pygame.Rect(660, 15, 90, 115)  # Definición de la puerta

def probar_colisiones():
    import pygame
    import sys

    # Inicializar Pygame
    pygame.init()

    # Crear la ventana
    ANCHO = 1280
    ALTO = 720
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Visualización de Colisiones")

    # Reloj para controlar los FPS
    reloj = pygame.time.Clock()

    # Lista de rectángulos de colisión
    colisiones_mapa_1 = [
        pygame.Rect(0, 0, 320, 270),       # cuadrado arriba a la derecha/ celda
        pygame.Rect(0, 260, 60, 420),      # borde izq
        pygame.Rect(1220, 130, 60, 560),   # borde derecha
        pygame.Rect(320, 0, 340, 150),     # borde superior izq
        pygame.Rect(750, 0, 530, 150),     # borde superior der
        pygame.Rect(60, 650, 1200, 40),    # borde inferior
        pygame.Rect(835, 480, 390, 190),   # cajas der
        pygame.Rect(660, 0, 90, 50)        # parte atras puerta
    ]

    # Rectángulo de la puerta
    puerta_1 = pygame.Rect(660, 0, 90, 115)

    # Bucle principal (solo para hacer tests)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dibujar fondo
        pantalla.fill((30, 30, 30))  # Fondo oscuro

        # Dibujar colisiones
        for rect in colisiones:
            pygame.draw.rect(pantalla, (255, 0, 0), rect, 2)  # Rojo

        # Dibujar la puerta
        pygame.draw.rect(pantalla, (0, 0, 255), puerta, 2)  # Azul

        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(60)
