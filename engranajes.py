import pygame
import sys
import math
import random

# ============================
# CONFIGURACIÓN
# ============================
ANCHO, ALTO = 800, 600
FPS = 60

# ============================
# CLASE ENGRANAJE
# ============================
class Engranaje:
    def __init__(self, x, y, radio, velocidad, tolerancia, ref_radio):
        self.x = x
        self.y = y
        self.radio = radio
        self.velocidad = velocidad
        self.tolerancia = tolerancia
        self.ref_radio = ref_radio  # tamaño del punto rojo de referencia
        self.angulo = random.randint(0, 360)
        self.detenido = False

    def actualizar(self):
        if not self.detenido:
            self.angulo = (self.angulo + self.velocidad) % 360

    def detener(self):
        self.detenido = True

    def reiniciar(self):
        self.detenido = False
        self.angulo = random.randint(0, 360)

    def alineado(self):
        # 270° representa la dirección "arriba"
        angulo_mod = self.angulo % 360
        return abs(angulo_mod - 270) < self.tolerancia or abs(angulo_mod + 90) < self.tolerancia

    def dibujar(self, pantalla):
        # Engranaje base
        pygame.draw.circle(pantalla, (160, 160, 160), (self.x, self.y), self.radio, 5)
        
        # Línea que marca la posición actual
        punta_x = self.x + math.cos(math.radians(self.angulo)) * self.radio
        punta_y = self.y + math.sin(math.radians(self.angulo)) * self.radio
        pygame.draw.line(pantalla, (255, 215, 0), (self.x, self.y), (punta_x, punta_y), 5)

        # Marca fija de referencia (arriba)
        ref_x = self.x
        ref_y = self.y - self.radio
        pygame.draw.circle(pantalla, (255, 100, 100), (ref_x, ref_y), self.ref_radio)

# ============================
# FUNCIÓN PRINCIPAL
# ============================
def minijuego_engranares():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("🌀 Alinear los Engranajes")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Engranajes con dificultad progresiva (menor referencia y más precisión)
    engranajes = [
        Engranaje(ANCHO//2 - 200, ALTO//2, 80, 2, tolerancia=25, ref_radio=12),  # más fácil
        Engranaje(ANCHO//2, ALTO//2, 80, 3, tolerancia=18, ref_radio=8),         # intermedio
        Engranaje(ANCHO//2 + 200, ALTO//2, 80, 4, tolerancia=12, ref_radio=5)    # difícil
    ]

    indice_actual = 0
    terminado = False
    exito = False
    mensaje_final = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False

                if not terminado and event.key == pygame.K_SPACE:
                    engranaje = engranajes[indice_actual]
                    engranaje.detener()

                    if engranaje.alineado():
                        indice_actual += 1
                        if indice_actual >= len(engranajes):
                            terminado = True
                            exito = True
                            mensaje_final = "✅ ¡Perfecto! Los engranajes se alinearon."
                    else:
                        terminado = True
                        exito = False
                        mensaje_final = "❌ Fallaste el alineamiento. El mecanismo se reinicia..."

                elif terminado and event.key == pygame.K_RETURN:
                    if exito:
                        return "completado"
                    else:
                        # Reiniciar todos los engranajes
                        for engranaje in engranajes:
                            engranaje.reiniciar()
                        indice_actual = 0
                        terminado = False
                        mensaje_final = ""

        # Actualización de engranajes
        if not terminado:
            engranajes[indice_actual].actualizar()

        # Fondo
        pantalla.fill((15, 15, 30))

        # Texto
        titulo = font.render("Alineá cada engranaje con su punto rojo", True, (255, 255, 255))
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 60))

        # Dibujar engranajes
        for i, engranaje in enumerate(engranajes):
            if i == indice_actual and not terminado:
                pygame.draw.circle(pantalla, (255, 255, 100), (engranaje.x, engranaje.y), engranaje.radio + 12, 3)
            engranaje.dibujar(pantalla)

        # Indicador de progreso
        progreso = font.render(f"Engranaje {min(indice_actual + 1, len(engranajes))} / {len(engranajes)}", True, (200, 200, 200))
        pantalla.blit(progreso, (ANCHO//2 - progreso.get_width()//2, ALTO - 100))

        # Mensaje final
        if terminado:
            msg = font.render(mensaje_final, True, (255, 215, 0))
            pantalla.blit(msg, (ANCHO//2 - msg.get_width()//2, ALTO - 60))
            cont = font.render("Presioná ENTER para continuar", True, (200, 200, 200))
            pantalla.blit(cont, (ANCHO//2 - cont.get_width()//2, ALTO - 30))

        pygame.display.flip()
        clock.tick(FPS)

# ============================
# EJECUCIÓN DIRECTA
# ============================
if __name__ == "__main__":
    resultado = minijuego_engranares()
    if resultado == "completado":
        print("✅ ¡Puerta abierta! Has alineado el mecanismo.")
    else:
        print("❌ Saliste del minijuego.")
