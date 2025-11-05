import pygame
import sys
import math
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(BASE_DIR)
candidate_paths = [
    os.path.join(BASE_DIR, "assets", "mapas"),
    os.path.join(parent_dir, "assets", "mapas"),
]
# Carpeta base donde están las imágenes
carpeta_mapas = next((p for p in candidate_paths if os.path.exists(p)), os.path.abspath(candidate_paths[-1]))

foto = os.path.join(carpeta_mapas, "engranajes.png")
bola8_path = os.path.join(carpeta_mapas, "bola8.png")
bola12_path = os.path.join(carpeta_mapas, "bola12.png")
bola16_path = os.path.join(carpeta_mapas, "bola16.png")

# ============================
# CONFIGURACIÓN
# ============================
ANCHO, ALTO = 1280, 720
FPS = 60

# ============================
# CLASE ENGRANAJE
# ============================
class Engranaje:
    def __init__(self, x, y, radio, velocidad, tolerancia, ref_radio, imagen):
        self.x = x
        self.y = y
        self.radio = radio
        self.velocidad = velocidad
        self.tolerancia = tolerancia
        self.ref_radio = ref_radio
        self.angulo = random.randint(0, 360)
        self.detenido = False

        size = radio * 2
        self.original_img = pygame.transform.smoothscale(imagen, (size, size))
        self.img = self.original_img
        self.rect = self.img.get_rect(center=(x, y))

    def actualizar(self):
        if not self.detenido:
            self.angulo = (self.angulo + self.velocidad) % 360

    def detener(self):
        self.detenido = True

    def reiniciar(self):
        self.detenido = False
        self.angulo = random.randint(0, 360)

    def alineado(self):
        angulo_mod = self.angulo % 360
        return abs(angulo_mod - 270) < self.tolerancia or abs(angulo_mod + 90) < self.tolerancia

    def dibujar(self, pantalla):
        # Rotar y dibujar el engranaje
        self.img = pygame.transform.rotate(self.original_img, -self.angulo)
        rect_rotado = self.img.get_rect(center=(self.x, self.y))
        pantalla.blit(self.img, rect_rotado.topleft)

        # Línea de posición actual
        punta_x = self.x + math.cos(math.radians(self.angulo)) * self.radio
        punta_y = self.y + math.sin(math.radians(self.angulo)) * self.radio
        pygame.draw.line(pantalla, (255, 0, 0), (self.x, self.y), (punta_x, punta_y), 4)


# ============================
# FUNCIÓN PRINCIPAL
# ============================
def minijuego_engranajes():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("🌀 Alinear los Engranajes")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Cargar imágenes
    if not os.path.exists(foto):
        print("⚠️ No se encontró la imagen del engranaje:", foto)
        pygame.quit()
        return

    try:
        imagen_engranaje = pygame.image.load(foto).convert_alpha()
        bola8 = pygame.image.load(bola8_path).convert_alpha()
        bola12 = pygame.image.load(bola12_path).convert_alpha()
        bola16 = pygame.image.load(bola16_path).convert_alpha()
    except Exception as e:
        print("⚠️ Error cargando imágenes:", e)
        pygame.quit()
        return

    # Crear engranajes
    radio_engranaje = 100
    espaciado = 300
    engranajes = [
        Engranaje(ANCHO//2 - espaciado, ALTO//2, radio_engranaje, 2, tolerancia=25, ref_radio=15, imagen=imagen_engranaje),
        Engranaje(ANCHO//2, ALTO//2, radio_engranaje, 3, tolerancia=18, ref_radio=12, imagen=imagen_engranaje),
        Engranaje(ANCHO//2 + espaciado, ALTO//2, radio_engranaje, 4, tolerancia=12, ref_radio=8, imagen=imagen_engranaje)
    ]

    # Escalar bolas según tamaño
    bola8_scaled = pygame.transform.smoothscale(bola8, (25,25))
    bola12_scaled = pygame.transform.smoothscale(bola12, (20,20))
    bola16_scaled = pygame.transform.smoothscale(bola16, (10,10))

    bolas = [
        (bola8_scaled, (ANCHO//2 - espaciado, ALTO//2)),
        (bola12_scaled, (ANCHO//2, ALTO//2)),
        (bola16_scaled, (ANCHO//2 + espaciado, ALTO//2)),
    ]

    indice_actual = 0
    terminado = False
    exito = False
    mensaje_final = ""

    # ============================
    # LOOP PRINCIPAL
    # ============================
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

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
                        pygame.quit()
                        return "completado"
                    else:
                        for engranaje in engranajes:
                            engranaje.reiniciar()
                        indice_actual = 0
                        terminado = False
                        mensaje_final = ""

        # Actualizar engranaje actual
        if not terminado:
            engranajes[indice_actual].actualizar()

        # Fondo
        pantalla.fill((15, 15, 30))

        # Dibujar bolas detrás
        for bola, (x, y) in bolas:
            # x, y = centro del engranaje
            rect_bola = bola.get_rect(center=(x, y -radio_engranaje))  # mover hacia arriba
            pantalla.blit(bola, rect_bola)


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
# EJECUCIÓN AUTOMÁTICA
# ============================
if __name__ == "__main__":
    minijuego_engranajes()
