import pygame
import os
import sys

# Inicialización
pygame.init()

# Configuración
ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
FPS = 60

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Test Colisiones con Sprites")

BLANCO = (255, 255, 255)
ROJO   = (255, 0, 0)
AZUL   = (0, 0, 255)
VERDE  = (0, 255, 0)

VELOCIDAD_JUGADOR = 5
VELOCIDAD_ANIMACION = 10

# Lista de rectángulos de colisión
colisiones = [
    pygame.Rect(0, 0, 320, 270), #cuadrado arriba a la derecha/ celda
    pygame.Rect(0, 270, 60, 360), # borde izq
    pygame.Rect(1220, 130, 60, 550),#borde derech
    pygame.Rect(320, 0, 340, 150),# borde superior izq
    pygame.Rect(750, 0, 500, 150),# borde superior der
    pygame.Rect(60, 650, 1200, 40),# borde inferior
    pygame.Rect(860, 480, 370, 190)  # cajas der
]
puerta = pygame.Rect(660, 0, 90, 115)  # Definición de la puerta


# Clase Jugador
class Jugador:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.velocidad = VELOCIDAD_JUGADOR
        self.animacion = self.cargar_sprites("sprites/idle")
        self.frame_actual = 0
        self.contador_animacion = 0

    def cargar_sprites(self, ruta_carpeta):
        imagenes = []
        if not os.path.exists(ruta_carpeta):
            print(f"[ERROR] No se encontró la carpeta: {ruta_carpeta}")
            return imagenes
        for archivo in sorted(os.listdir(ruta_carpeta)):
            if archivo.lower().endswith(".png"):
                ruta = os.path.join(ruta_carpeta, archivo)
                img = pygame.image.load(ruta).convert_alpha()
                imagenes.append(img)
        return imagenes

    def manejar_teclas(self):
        teclas = pygame.key.get_pressed()
        izquierda = teclas[pygame.K_LEFT]
        derecha   = teclas[pygame.K_RIGHT]
        arriba    = teclas[pygame.K_UP]
        abajo     = teclas[pygame.K_DOWN]

        moviendo = False

        if izquierda:
            pos_anterior = self.rect.x
            self.rect.x -= self.velocidad
            for col in colisiones:
                if self.rect.colliderect(col):
                    self.rect.x = pos_anterior
                    break
            moviendo = True

        elif derecha:
            pos_anterior = self.rect.x
            self.rect.x += self.velocidad
            for col in colisiones:
                if self.rect.colliderect(col):
                    self.rect.x = pos_anterior
                    break
            moviendo = True

        if not izquierda and not derecha:
            if arriba:
                pos_anterior = self.rect.y
                self.rect.y -= self.velocidad
                for col in colisiones:
                    if self.rect.colliderect(col):
                        self.rect.y = pos_anterior
                        break
                moviendo = True

            elif abajo:
                pos_anterior = self.rect.y
                self.rect.y += self.velocidad
                for col in colisiones:
                    if self.rect.colliderect(col):
                        self.rect.y = pos_anterior
                        break
                moviendo = True

        # Animación
        if moviendo and self.animacion:
            self.contador_animacion += 1
            if self.contador_animacion >= VELOCIDAD_ANIMACION:
                self.frame_actual = (self.frame_actual + 1) % len(self.animacion)
                self.contador_animacion = 0
        else:
            self.frame_actual = 0
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        if self.animacion:
            imagen = self.animacion[self.frame_actual]
            pantalla.blit(imagen, self.rect.topleft)
        pygame.draw.rect(pantalla, VERDE, self.rect, 2)  # hitbox

# Crear jugador
jugador = Jugador(600, 500, 48, 64)  # Tamaño estimado del sprite

# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    reloj.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Lógica de movimiento
    jugador.manejar_teclas()

    # Comprobar colisión con puerta
    if jugador.rect.colliderect(puerta):
        print("¡Tocó la puerta!")

    # Dibujos
    pantalla.fill(BLANCO)

    for rect in colisiones:
        pygame.draw.rect(pantalla, ROJO, rect)

    pygame.draw.rect(pantalla, AZUL, puerta)

    jugador.dibujar(pantalla)

    pygame.display.flip()

pygame.quit()
sys.exit()
