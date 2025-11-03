#jugador
import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configuracion import VELOCIDAD_JUGADOR, ANCHO_PANTALLA, ALTO_PANTALLA, VELOCIDAD_ANIMACION

class Jugador:
    def __init__(self, x, y, ancho, alto, escala=1.0, colisiones=None):
        self.colisiones = colisiones or []
        self.velocidad = VELOCIDAD_JUGADOR
        self.escala = escala
        # Posición visual del sprite (sin desplazamiento manual)
        self.sprite_pos = pygame.Vector2(x, y)
        # Crear el rectángulo de colisión con offset relativo al sprite
        offset_x = 0  # mueve la hitbox a la derecha
        offset_y = 0  
        # mueve la hitbox hacia abajo
        # Tamaño base del rectángulo
        hitbox_ancho = int(ancho * escala)
        hitbox_alto = int(alto * escala)

        # Crear la hitbox desplazada y ajustada
        self.rect = pygame.Rect(
            self.sprite_pos.x + offset_x,
            self.sprite_pos.y + offset_y,
            hitbox_ancho,
            hitbox_alto
        )
        self.rect.inflate_ip(-30, -10)  # achica la hitbox horizontal y verticalmente


        print("Iniciando carga de animaciones...")
        # Animaciones (como ya tenías)
        self.animaciones = {
            "idle_abajo": self.cargar_sprites("idle_personaje_lvl1", "idle_abajo"),
            "idle_arriba": self.cargar_sprites("idle_personaje_lvl1", "idle_arriba"),
            "idle_izquierda": self.cargar_sprites("idle_personaje_lvl1", "idle_izquierda"),
            "idle_derecha": self.cargar_sprites("idle_personaje_lvl1", "idle_derecha"),
            "run_abajo": self.cargar_sprites("run_personaje_lvl1", "run_abajo"),
            "run_arriba": self.cargar_sprites("run_personaje_lvl1", "run_arriba"),
            "run_izquierda": self.cargar_sprites("run_personaje_lvl1", "run_izquierda"),
            "run_derecha": self.cargar_sprites("run_personaje_lvl1", "run_derecha"),
        }
        print("Animaciones cargadas:", list(self.animaciones.keys()))
        print("Número de frames en idle_abajo:", len(self.animaciones["idle_abajo"]) if "idle_abajo" in self.animaciones else 0)

        self.direccion = "abajo"
        self.estado = "idle"
        self.animacion_actual = self.animaciones.get("idle_abajo", [])
        self.frame_actual = 0
        self.contador_tiempo = 0
        self.velocidad_animacion = VELOCIDAD_ANIMACION
        self.velocidad_animacion_attack = VELOCIDAD_ANIMACION * 1.1  # o *3 si querés más lento
        self.atacando = False  # ya lo tenías, pero asegurate que esté acá


        # Escalar sprites si la escala no es 1
        if self.escala != 1.0:
            for clave, lista in self.animaciones.items():
                self.animaciones[clave] = [pygame.transform.scale(img, 
                                           (int(img.get_width() * escala), int(img.get_height() * escala))) 
                                           for img in lista]

    def cargar_sprites(self, carpeta_principal, subcarpeta):
        ruta_base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites_jugador", carpeta_principal, subcarpeta)
        imagenes = []

        print(f"Intentando cargar sprites desde: {ruta_base}")
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

        return imagenes
  

    def manejar_teclas(self):
        teclas = pygame.key.get_pressed()

        # 1) Si ya está atacando, no proceses movimiento ni otro ataque
        if self.atacando:
            return

        # 2) Detectar inicio de ataque - temporalmente deshabilitado hasta que se agreguen las animaciones
        if teclas[pygame.K_SPACE] and not self.atacando:
            # Por ahora, no cambiamos a animación de ataque ya que no existe
            return

        # 3) Movimiento normal
        moviendo = False
        colisiones = self.colisiones

        izquierda = teclas[pygame.K_LEFT]
        derecha   = teclas[pygame.K_RIGHT]
        arriba    = teclas[pygame.K_UP]
        abajo     = teclas[pygame.K_DOWN]

        if izquierda:
            pos_anterior = self.rect.x
            self.rect.x -= self.velocidad
            self.sprite_pos.x -= self.velocidad
            self.direccion = "izquierda"
            moviendo = True

            for colision in colisiones:
                if self.rect.colliderect(colision):
                    self.rect.x = pos_anterior
                    self.sprite_pos.x += self.velocidad
                    break

        elif derecha:
            pos_anterior = self.rect.x
            self.rect.x += self.velocidad
            self.sprite_pos.x += self.velocidad
            self.direccion = "derecha"
            moviendo = True

            for colision in colisiones:
                if self.rect.colliderect(colision):
                    self.rect.x = pos_anterior
                    self.sprite_pos.x -= self.velocidad
                    break

        if not izquierda and not derecha:
            if arriba:
                pos_anterior = self.rect.y
                self.rect.y -= self.velocidad
                self.sprite_pos.y -= self.velocidad
                self.direccion = "arriba"
                moviendo = True

                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.y = pos_anterior
                        self.sprite_pos.y += self.velocidad
                        break

            elif abajo:
                pos_anterior = self.rect.y
                self.rect.y += self.velocidad
                self.sprite_pos.y += self.velocidad
                self.direccion = "abajo"
                moviendo = True

                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.y = pos_anterior
                        self.sprite_pos.y -= self.velocidad
                        break
        else:
            if arriba:
                pos_anterior = self.rect.y
                self.rect.y -= self.velocidad
                self.sprite_pos.y -= self.velocidad
                moviendo = True

                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.y = pos_anterior
                        self.sprite_pos.y += self.velocidad
                        break

            elif abajo:
                pos_anterior = self.rect.y
                self.rect.y += self.velocidad
                self.sprite_pos.y += self.velocidad
                moviendo = True

                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.y = pos_anterior
                        self.sprite_pos.y -= self.velocidad
                        break

        if not self.atacando:
            self.estado = "run" if moviendo else "idle"
            clave_animacion = f"{self.estado}_{self.direccion}"

            if clave_animacion in self.animaciones and self.animaciones[clave_animacion]:
                if self.animacion_actual != self.animaciones[clave_animacion]:
                    self.animacion_actual = self.animaciones[clave_animacion]
                    self.frame_actual = 0


        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, ANCHO_PANTALLA)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, ALTO_PANTALLA)

        # Synchronize sprite_pos with rect after clamping
        offset_x = 70  # same offset as in __init__
        offset_y = 101
        self.sprite_pos.x = self.rect.x - offset_x
        self.sprite_pos.y = self.rect.y - offset_y

    def dibujar(self, pantalla, offset_x=0, offset_y=0):
        if not self.animacion_actual:
            print("No hay animación actual disponible")
            return
        
        # Actualizar el frame de animación
        self.contador_tiempo += 1

        # Elegir velocidad según estado
        if self.estado == "attack":
            velocidad_actual = self.velocidad_animacion_attack
        else:
            velocidad_actual = self.velocidad_animacion

        if self.contador_tiempo >= velocidad_actual:
            self.frame_actual = (self.frame_actual + 1) % len(self.animacion_actual)
            self.contador_tiempo = 0


        # Obtener el sprite actual
        imagen = self.animacion_actual[self.frame_actual]

        # Dibujar el sprite con desplazamiento
        pantalla.blit(imagen, (self.sprite_pos.x + offset_x, self.sprite_pos.y + offset_y))

        # Dibujar la hitbox (verde) con desplazamiento
        hitbox_offset = self.rect.move(offset_x, offset_y)
        #pygame.draw.rect(pantalla, (0, 255, 0), hitbox_offset, 2)
        if self.estado == "attack" and self.frame_actual == len(self.animacion_actual) - 1:
            self.estado = "idle"