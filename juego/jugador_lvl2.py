#jugador lv2
import pygame
import os

from .jugador import Jugador  # Importa la clase Jugador desde el módulo jugador.py
from configuracion import VELOCIDAD_JUGADOR, ANCHO_PANTALLA, ALTO_PANTALLA, VELOCIDAD_ANIMACION

class JugadorLvl2(Jugador):
    def __init__(self, x, y, ancho, alto, escala=1.0, colisiones=None):
        super().__init__(x, y, ancho, alto, escala, colisiones)


        # Crear la hitbox desplazada y ajustada
        self.rect = pygame.Rect(
            x, #posision en y
            y, #posision en x
            69,  # ancho fijo de la hitbox
            37 # alto fijo de la hitbox
        )
        self.rect.inflate_ip(-25, -10)  # achica la hitbox horizontal y verticalmente

        # Variables de control de ataque
        self.atacando = False
        self.tiempo_ataque = 0
        self.duracion_ataque = 500  # duración del ataque en milisegundos
        self.velocidad_animacion_attack = 5  # velocidad de animación de ataque (frames más rápidos)
        self.velocidad_animacion = 8  # velocidad de animación normal
        self.contador_tiempo = 0

        # Sobrescribe las animaciones para el nivel 2
        self.animaciones = {
        "idle_abajo": self.cargar_sprites("Idle_personaje_lvl2", "idle_abajo"),
        "idle_arriba": self.cargar_sprites("Idle_personaje_lvl2", "idle_arriba"),
        "idle_izquierda": self.cargar_sprites("Idle_personaje_lvl2", "idle_izquierda"),
        "idle_derecha": self.cargar_sprites("Idle_personaje_lvl2", "idle_derecha"),
        #
        "run_abajo": self.cargar_sprites("Run_personaje_lvl2", "run_abajo"),
        "run_arriba": self.cargar_sprites("Run_personaje_lvl2", "run_arriba"),
        "run_izquierda": self.cargar_sprites("Run_personaje_lvl2", "run_izquierda"),
        "run_derecha": self.cargar_sprites("Run_personaje_lvl2", "run_derecha"),
        #
        "attack_abajo": self.cargar_sprites("Attack_personaje_lvl2", "attack_abajo"),
        "attack_arriba": self.cargar_sprites("Attack_personaje_lvl2", "attack_arriba"),
        "attack_izquierda": self.cargar_sprites("Attack_personaje_lvl2", "attack_izquierda"),
        "attack_derecha": self.cargar_sprites("Attack_personaje_lvl2", "attack_derecha"),
        #
        "hurt_abajo": self.cargar_sprites("Hurt_personaje_lvl2", "hurt_abajo"),
        "hurt_arriba": self.cargar_sprites("Hurt_personaje_lvl2", "hurt_arriba"),
        "hurt_izquierda": self.cargar_sprites("Hurt_personaje_lvl2", "hurt_izquierda"),
        "hurt_derecha": self.cargar_sprites("Hurt_personaje_lvl2", "hurt_derecha"),
        #
        "death_abajo": self.cargar_sprites("Death_personaje_lvl2", "death_abajo"),
        "death_arriba": self.cargar_sprites("Death_personaje_lvl2", "death_arriba"),
        "death_izquierda": self.cargar_sprites("Death_personaje_lvl2", "death_izquierda"),
        "death_derecha": self.cargar_sprites("Death_personaje_lvl2", "death_derecha"),
        #
        "run_attack_abajo": self.cargar_sprites("Run_Attack_personaje_lvl2", "run_attack_abajo"),
        "run_attack_arriba": self.cargar_sprites("Run_Attack_personaje_lvl2", "run_attack_arriba"),
        "run_attack_izquierda": self.cargar_sprites("Run_Attack_personaje_lvl2", "run_attack_izquierda"),
        "run_attack_derecha": self.cargar_sprites("Run_Attack_personaje_lvl2", "run_attack_derecha"),
        }
        


        # Estado inicial
        self.estado = "idle"
        self.direccion = "abajo"
        self.animacion_actual = self.animaciones.get("idle_abajo", [])
        self.frame_actual = 0

        # No necesitamos volver a definir los parámetros de ataque aquí
        # ya que los definimos arriba en el __init__

    def cargar_sprites(self, carpeta_principal, subcarpeta):
        ruta_base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites_jugador lvl 2", carpeta_principal, subcarpeta)
        imagenes = []
        
        if not os.path.exists(ruta_base):
            #print(f"[ADVERTENCIA] Carpeta no encontrada: {ruta_base}")
            return imagenes

        for archivo in sorted(os.listdir(ruta_base)):
            if archivo.lower().endswith(".png"):
                ruta = os.path.join(ruta_base, archivo)
                try:
                    imagen = pygame.image.load(ruta).convert_alpha()
                    
                    # Escalar la imagen según self.escala
                    ancho = int(imagen.get_width() * self.escala)
                    alto = int(imagen.get_height() * self.escala)
                    imagen_escalada = pygame.transform.scale(imagen, (ancho, alto))

                    imagenes.append(imagen_escalada)
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar {ruta}: {e}")

        return imagenes

    
    def manejar_teclas(self):
        teclas = pygame.key.get_pressed()
        tiempo_actual = pygame.time.get_ticks()
        moviendo = False
        colisiones = self.colisiones

        # Detectar ataque con ESPACIO
        if teclas[pygame.K_SPACE] and not self.atacando:
            self.atacando = True
            self.tiempo_ataque = tiempo_actual

            if self.estado == "run":
                clave_animacion = f"run_attack_{self.direccion}"
            else:
                clave_animacion = f"attack_{self.direccion}"

            if clave_animacion in self.animaciones:
                self.animacion_actual = self.animaciones[clave_animacion]
                self.frame_actual = 0

        # Finalizar ataque después de cierto tiempo
        if self.atacando and tiempo_actual - self.tiempo_ataque > self.duracion_ataque:
            self.atacando = False

        # Movimiento solo si no está atacando
        if not self.atacando:
            izquierda = teclas[pygame.K_LEFT]
            derecha   = teclas[pygame.K_RIGHT]
            arriba    = teclas[pygame.K_UP]
            abajo     = teclas[pygame.K_DOWN]

            if izquierda:
                prev_x = self.rect.x
                self.rect.x -= self.velocidad
                self.sprite_pos.x -= self.velocidad
                self.direccion = "izquierda"
                moviendo = True

                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.x = prev_x
                        self.sprite_pos.x = self.rect.x - 10
                        break

            elif derecha:
                prev_x = self.rect.x
                self.rect.x += self.velocidad
                self.sprite_pos.x += self.velocidad
                self.direccion = "derecha"
                moviendo = True

                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.x = prev_x
                        self.sprite_pos.x = self.rect.x - 10
                        break

            if not izquierda and not derecha:
                if arriba:
                    prev_y = self.rect.y
                    self.rect.y -= self.velocidad
                    self.sprite_pos.y -= self.velocidad
                    self.direccion = "arriba"
                    moviendo = True

                    for colision in colisiones:
                        if self.rect.colliderect(colision):
                            self.rect.y = prev_y
                            self.sprite_pos.y = self.rect.y - 0
                            break

                elif abajo:
                    prev_y = self.rect.y
                    self.rect.y += self.velocidad
                    self.sprite_pos.y += self.velocidad
                    self.direccion = "abajo"
                    moviendo = True

                    for colision in colisiones:
                        if self.rect.colliderect(colision):
                            self.rect.y = prev_y
                            self.sprite_pos.y = self.rect.y - 0
                            break
            else:
                if arriba:
                    prev_y = self.rect.y
                    self.rect.y -= self.velocidad
                    self.sprite_pos.y -= self.velocidad
                    moviendo = True

                    for colision in colisiones:
                        if self.rect.colliderect(colision):
                            self.rect.y = prev_y
                            self.sprite_pos.y = self.rect.y - 0
                            break

                elif abajo:
                    prev_y = self.rect.y
                    self.rect.y += self.velocidad
                    self.sprite_pos.y += self.velocidad
                    moviendo = True

                    for colision in colisiones:
                        if self.rect.colliderect(colision):
                            self.rect.y = prev_y
                            self.sprite_pos.y = self.rect.y - 0
                            break

            # Animación según movimiento y estado de ataque
            if not self.atacando:
                self.estado = "run" if moviendo else "idle"
            
            clave_animacion = f"{self.estado}_{self.direccion}"
            if clave_animacion in self.animaciones and self.animaciones[clave_animacion]:
                if self.animacion_actual != self.animaciones[clave_animacion]:
                    self.animacion_actual = self.animaciones[clave_animacion]
                    self.frame_actual = 0
                    self.contador_tiempo = 0  # Resetear el contador de tiempo al cambiar de animación

        # Limitar dentro de pantalla
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, ANCHO_PANTALLA)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, ALTO_PANTALLA)

        # Sincronizar sprite_pos con rect usando el mismo hitbox_offset
        self.sprite_pos.x = self.rect.x - 10
        self.sprite_pos.y = self.rect.y - 0


    def dibujar(self, pantalla, offset_x=0, offset_y=0):
            if not self.animacion_actual:
                print("No hay animación lvl 2 actual disponible")
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
            #pantalla.blit(imagen, (self.sprite_pos.x + offset_x, self.sprite_pos.y + offset_y))
            pantalla.blit(imagen, (self.sprite_pos.x - 32 -28 , self.sprite_pos.y -64 - 45))
            
            # Dibujar la hitbox (verde) con desplazamiento
            #pygame.draw.rect(pantalla, (0, 255, 0), self.rect, 2)
            if self.estado == "attack" and self.frame_actual == len(self.animacion_actual) - 1:
                self.estado = "idle"