import pygame
import os
from ..configuracion import VELOCIDAD_JUGADOR, ANCHO_PANTALLA, ALTO_PANTALLA, VELOCIDAD_ANIMACION

class Jugador:
    def __init__(self, x, y, ancho, alto, escala=1.0):
        # Rectángulo del jugador
        self.rect = pygame.Rect(x, y, int(ancho*escala), int(alto*escala))
        self.velocidad = VELOCIDAD_JUGADOR
        self.escala = escala

        # Cargar animaciones
        self.animaciones = {
            "idle_abajo": self.cargar_sprites("idle_personaje_lvl1_con_sombra", "idle_abajo"),
            "idle_arriba": self.cargar_sprites("idle_personaje_lvl1_con_sombra", "idle_arriba"),
            "idle_izquierda": self.cargar_sprites("idle_personaje_lvl1_con_sombra", "idle_izquierda"),
            "idle_derecha": self.cargar_sprites("idle_personaje_lvl1_con_sombra", "idle_derecha"),
            "run_abajo": self.cargar_sprites("run_personaje_lvl1_con_sombra", "run_abajo"),
            "run_arriba": self.cargar_sprites("run_personaje_lvl1_con_sombra", "run_arriba"),
            "run_izquierda": self.cargar_sprites("run_personaje_lvl1_con_sombra", "run_izquierda"),
            "run_derecha": self.cargar_sprites("run_personaje_lvl1_con_sombra", "run_derecha")
        }

        self.direccion = "abajo"
        self.estado = "idle"
        self.animacion_actual = self.animaciones.get("idle_abajo", [])
        self.frame_actual = 0
        self.contador_tiempo = 0
        self.velocidad_animacion = VELOCIDAD_ANIMACION

        # Escalar sprites si la escala no es 1
        if self.escala != 1.0:
            for clave, lista in self.animaciones.items():
                self.animaciones[clave] = [pygame.transform.scale(img, 
                                           (int(img.get_width()*escala), int(img.get_height()*escala))) 
                                           for img in lista]

    def cargar_sprites(self, carpeta_principal, subcarpeta):
        ruta_base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sprites", carpeta_principal, subcarpeta)
        imagenes = []

        if not os.path.exists(ruta_base):
            print(f"[ADVERTENCIA] Carpeta no encontrada: {ruta_base}")
            return imagenes

        for archivo in sorted(os.listdir(ruta_base)):
            if archivo.lower().endswith(".png"):
                ruta = os.path.join(ruta_base, archivo)
                try:
                    imagen = pygame.image.load(ruta).convert_alpha()
                    imagenes.append(imagen)
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar {ruta}: {e}")

        return imagenes

    def manejar_teclas(self):
        teclas = pygame.key.get_pressed()
        moviendo = False

        izquierda = teclas[pygame.K_a]
        derecha = teclas[pygame.K_d]
        arriba = teclas[pygame.K_w]
        abajo = teclas[pygame.K_s]


        if izquierda:
            self.rect.x -= self.velocidad
            self.direccion = "izquierda"
            moviendo = True
            
        elif derecha:
            self.rect.x += self.velocidad
            self.direccion = "derecha"
            moviendo = True

        if not izquierda and not derecha:
            if arriba:
                self.rect.y -= self.velocidad
                self.direccion = "arriba"
                moviendo = True
            elif abajo:
                self.rect.y += self.velocidad
                self.direccion = "abajo"
                moviendo = True
        else:
            if arriba:
                self.rect.y -= self.velocidad
                moviendo = True
            elif abajo:
                self.rect.y += self.velocidad
                moviendo = True

        self.estado = "run" if moviendo else "idle"
        clave_animacion = f"{self.estado}_{self.direccion}"

        if clave_animacion in self.animaciones and self.animaciones[clave_animacion]:
            if self.animacion_actual != self.animaciones[clave_animacion]:
                self.animacion_actual = self.animaciones[clave_animacion]
                self.frame_actual = 0

        # Limitar jugador en pantalla
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, ANCHO_PANTALLA)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, ALTO_PANTALLA)

    def dibujar(self, pantalla):
        if not self.animacion_actual:
            return

        self.contador_tiempo += 1
        if self.contador_tiempo >= self.velocidad_animacion:
            self.frame_actual = (self.frame_actual + 1) % len(self.animacion_actual)
            self.contador_tiempo = 0

        imagen = self.animacion_actual[self.frame_actual]
        pantalla.blit(imagen, self.rect)
