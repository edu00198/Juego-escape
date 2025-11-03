#jugador lv2
import pygame
import os
import sys

from jugador import Jugador  # Importa la clase Jugador desde el módulo jugador.py
from configuracion import VELOCIDAD_JUGADOR, ANCHO_PANTALLA, ALTO_PANTALLA, VELOCIDAD_ANIMACION

class JugadorLvl2(Jugador):
    def __init__(self, x, y, ancho, alto, escala=1.0, colisiones=None):
        super().__init__(x, y, ancho, alto, escala, colisiones)

        self.atacando = False
        self.tiempo_ataque = 0
        self.duracion_ataque = 300  # duración del ataque en milisegundos
        



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
        "run_attack_abajo": self.cargar_sprites("Run_attack_personaje_lvl2", "run_attack_abajo"),
        "run_attack_arriba": self.cargar_sprites("Run_attack_personaje_lvl2", "run_attack_arriba"),
        "run_attack_izquierda": self.cargar_sprites("Run_attack_personaje_lvl2", "run_attack_izquierda"),
        "run_attack_derecha": self.cargar_sprites("Run_attack_personaje_lvl2", "run_attack_derecha"),
        #
        "idle_attack_abajo": self.cargar_sprites("Attack_personaje_lvl2", "idle_attack_abajo"),
        "idle_attack_arriba": self.cargar_sprites("Attack_personaje_lvl2", "idle_attack_arriba"),
        "idle_attack_izquierda": self.cargar_sprites("Attack_personaje_lvl2", "idle_attack_izquierda"),
        "idle_attack_derecha": self.cargar_sprites("Attack_personaje_lvl2", "idle_attack_derecha")}

        # Estado inicial
        self.estado = "idle"
        self.direccion = "abajo"
        self.animacion_actual = self.animaciones.get("idle_abajo", [])
        self.frame_actual = 0

        # Parámetros de ataque
        self.atacando = False
        self.tiempo_ataque = 0
        self.duracion_ataque = 300  

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

            # Animación según movimiento
            self.estado = "run" if moviendo else "idle"
            clave_animacion = f"{self.estado}_{self.direccion}"

            if clave_animacion in self.animaciones and self.animaciones[clave_animacion]:
                if self.animacion_actual != self.animaciones[clave_animacion]:
                    self.animacion_actual = self.animaciones[clave_animacion]
                    self.frame_actual = 0

        # Limitar dentro de pantalla
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, ANCHO_PANTALLA)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, ALTO_PANTALLA)

        # Sincronizar sprite_pos con rect
        offset_x = 70
        offset_y = 101
        self.sprite_pos.x = self.rect.x - offset_x
        self.sprite_pos.y = self.rect.y - offset_y
