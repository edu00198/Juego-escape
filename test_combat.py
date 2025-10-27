import pygame
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from juego.combat_system import CombatSystem, Enemy, CombatPlayer

class JugadorTest:
    def __init__(self, x, y, ancho, alto, escala=2.0):
        self.rect = pygame.Rect(x, y, ancho * escala, alto * escala)
        self.direccion = "abajo"
        self.estado = "idle"
        self.velocidad = 5
        self.escala = escala
        self.sprite_pos = pygame.Vector2(x, y)
        self.atacando = False
        self.frame_actual = 0
        self.contador_tiempo = 0
        self.velocidad_animacion = 8
        
        print("Iniciando carga de animaciones...")
        self.animaciones = {
            "idle_abajo": self.cargar_sprites("Idle_personaje_lvl2", "idle_abajo"),
            "idle_arriba": self.cargar_sprites("Idle_personaje_lvl2", "idle_arriba"),
            "idle_izquierda": self.cargar_sprites("Idle_personaje_lvl2", "idle_izquierda"),
            "idle_derecha": self.cargar_sprites("Idle_personaje_lvl2", "idle_derecha"),
            
            "run_abajo": self.cargar_sprites("Run_personaje_lvl2", "run_abajo"),
            "run_arriba": self.cargar_sprites("Run_personaje_lvl2", "run_arriba"),
            "run_izquierda": self.cargar_sprites("Run_personaje_lvl2", "run_izquierda"),
            "run_derecha": self.cargar_sprites("Run_personaje_lvl2", "run_derecha"),
            
            "attack_abajo": self.cargar_sprites("Attack_personaje_lvl2", "attack_abajo"),
            "attack_arriba": self.cargar_sprites("Attack_personaje_lvl2", "attack_arriba"),
            "attack_izquierda": self.cargar_sprites("Attack_personaje_lvl2", "attack_izquierda"),
            "attack_derecha": self.cargar_sprites("Attack_personaje_lvl2", "attack_derecha"),
        }
        
        # Si no hay animaciones de ataque, usar las de Run_Attack
        if not self.animaciones["attack_abajo"]:
            self.animaciones["attack_abajo"] = self.cargar_sprites("Run_Attack_with_personaje_lvl2", "run_attack_abajo")
            self.animaciones["attack_arriba"] = self.cargar_sprites("Run_Attack_with_personaje_lvl2", "run_attack_arriba")
            self.animaciones["attack_izquierda"] = self.cargar_sprites("Run_Attack_with_personaje_lvl2", "run_attack_izquierda")
            self.animaciones["attack_derecha"] = self.cargar_sprites("Run_Attack_with_personaje_lvl2", "run_attack_derecha")
        
        print("Animaciones cargadas:", list(self.animaciones.keys()))
        
        self.animacion_actual = self.animaciones.get("idle_abajo", [])
        
        # Escalar sprites
        if self.escala != 1.0:
            for clave, lista in self.animaciones.items():
                self.animaciones[clave] = [pygame.transform.scale(img, 
                                           (int(img.get_width() * escala), 
                                            int(img.get_height() * escala))) 
                                           for img in lista]
    
    def cargar_sprites(self, carpeta_principal, subcarpeta):
        ruta_base = os.path.join(os.getcwd(), 
                                "assets", "sprites_jugador lvl 2",
                                carpeta_principal, subcarpeta)
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
                    print(f"Cargada imagen: {archivo}")
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar {ruta}: {e}")
                    
        return imagenes
            
    def manejar_teclas(self):
        keys = pygame.key.get_pressed()
        moviendo = False
        
        if self.atacando:
            return
            
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.sprite_pos.x -= self.velocidad
            self.direccion = "izquierda"
            moviendo = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.sprite_pos.x += self.velocidad
            self.direccion = "derecha"
            moviendo = True
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
            self.sprite_pos.y -= self.velocidad
            self.direccion = "arriba"
            moviendo = True
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad
            self.sprite_pos.y += self.velocidad
            self.direccion = "abajo"
            moviendo = True
            
        if not self.atacando:
            self.estado = "run" if moviendo else "idle"
            clave_animacion = f"{self.estado}_{self.direccion}"
            
            if clave_animacion in self.animaciones and self.animaciones[clave_animacion]:
                if self.animacion_actual != self.animaciones[clave_animacion]:
                    self.animacion_actual = self.animaciones[clave_animacion]
                    self.frame_actual = 0
            
    def dibujar(self, pantalla):
        if not self.animacion_actual:
            print("No hay animación actual disponible")
            return
            
        # Actualizar el frame de animación
        self.contador_tiempo += 1
        if self.contador_tiempo >= self.velocidad_animacion:
            self.frame_actual = (self.frame_actual + 1) % len(self.animacion_actual)
            self.contador_tiempo = 0
            
            # Si estamos atacando y llegamos al último frame, terminamos el ataque
            if self.estado == "attack" and self.frame_actual == len(self.animacion_actual) - 1:
                self.estado = "idle"
                self.atacando = False
                clave_animacion = f"{self.estado}_{self.direccion}"
                if clave_animacion in self.animaciones:
                    self.animacion_actual = self.animaciones[clave_animacion]
                    self.frame_actual = 0
        
        # Obtener y dibujar el sprite actual
        imagen = self.animacion_actual[self.frame_actual]
        pantalla.blit(imagen, (self.sprite_pos.x, self.sprite_pos.y))
        
        # Debug: dibujar hitbox
        #pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2)

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Test Sistema de Combate")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

def main():
    clock = pygame.time.Clock()
    running = True
    
    # Crear jugador en el centro de la pantalla
    jugador = JugadorTest(ANCHO_PANTALLA//2 - 64, ALTO_PANTALLA//2 - 64, 64, 64)
    combat_player = CombatPlayer(jugador)
    
    # Inicializar sistema de combate
    combat_system = CombatSystem()
    
    # Crear algunos enemigos iniciales
    for _ in range(5):
        x = random.randint(100, ANCHO_PANTALLA - 100)
        y = random.randint(100, ALTO_PANTALLA - 100)
        enemy = Enemy(x, y)
        combat_system.add_enemy(enemy)
    
    # Loop principal
    while running:
        current_time = pygame.time.get_ticks()
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Manejo de teclas para el jugador
        jugador.manejar_teclas()
        
        # Limpiar pantalla
        pantalla.fill(BLANCO)
        
        # Actualizar y dibujar enemigos
        for enemy in combat_system.enemies[:]:
            enemy.move_towards_player(jugador.rect)
            enemy.draw(pantalla)
            
            # Ataque del enemigo
            if enemy.can_attack(current_time):
                if pygame.Rect(enemy.rect).colliderect(jugador.rect):
                    if combat_player.take_damage(enemy.attack_power, current_time):
                        print("Game Over")
                        running = False
                    enemy.last_attack = current_time
        
        # Manejo del ataque del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and combat_player.can_attack(current_time) and not jugador.atacando:
            jugador.estado = "attack"
            jugador.atacando = True
            jugador.frame_actual = 0
            clave_animacion = f"{jugador.estado}_{jugador.direccion}"
            if clave_animacion in jugador.animaciones:
                jugador.animacion_actual = jugador.animaciones[clave_animacion]
            combat_player.attack(current_time, combat_system.enemies)
        
        # Actualizar jugador y sistema de combate
        combat_player.update(current_time)
        jugador.dibujar(pantalla)
        combat_player.draw_health(pantalla)
        
        # Debug: dibujar área de ataque cuando el jugador está atacando
        if jugador.estado == "attack":
            attack_rect = combat_player.get_attack_rect()
            pygame.draw.rect(pantalla, (255, 255, 0), attack_rect, 2)
            
        # Mostrar instrucciones
        font = pygame.font.Font(None, 36)
        text = font.render("ESPACIO para atacar", True, NEGRO)
        pantalla.blit(text, (10, ALTO_PANTALLA - 40))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()