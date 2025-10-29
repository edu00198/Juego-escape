import pygame
import math

class CombatSystem:
    def __init__(self):
        self.enemies = []
        self.projectiles = []
        
    def add_enemy(self, enemy):
        self.enemies.append(enemy)
        
    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            
class Enemy:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.rect = pygame.Rect(x, y, 32, 32)  # Tamaño básico del enemigo
        self.speed = 2
        self.attack_range = 40
        self.attack_power = 10
        self.last_attack = 0
        self.attack_cooldown = 1000  # 1 segundo entre ataques
        
    def move_towards_player(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            
    def can_attack(self, current_time):
        return current_time - self.last_attack >= self.attack_cooldown
        
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
        
    def draw(self, screen, camera_offset_x=0, camera_offset_y=0):
        # Dibujar el enemigo (rectángulo rojo por ahora)
        pygame.draw.rect(screen, (255, 0, 0), 
                        self.rect.move(camera_offset_x, camera_offset_y))
        
        # Dibujar barra de vida
        health_bar_width = 32
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        
        # Fondo de la barra de vida (gris)
        pygame.draw.rect(screen, (64, 64, 64),
                        (self.rect.x + camera_offset_x, 
                         self.rect.y + camera_offset_y - 10,
                         health_bar_width, health_bar_height))
        
        # Barra de vida actual (verde)
        pygame.draw.rect(screen, (0, 255, 0),
                        (self.rect.x + camera_offset_x,
                         self.rect.y + camera_offset_y - 10,
                         health_bar_width * health_ratio, health_bar_height))

class CombatPlayer:
    def __init__(self, player):
        self.player = player
        self.health = 100
        self.max_health = 100
        self.attack_power = 25
        self.attack_range = 30  # Reducido de 50 a 30
        self.last_attack = 0
        self.attack_cooldown = 500  # Medio segundo entre ataques
        self.is_attacking = False
        self.invulnerable = False
        self.invulnerable_time = 1000  # 1 segundo de invulnerabilidad después de recibir daño
        self.last_hit = 0
        
    def can_attack(self, current_time):
        return current_time - self.last_attack >= self.attack_cooldown
        
    def attack(self, current_time, enemies):
        if not self.can_attack(current_time):
            return
            
        self.is_attacking = True
        self.last_attack = current_time
        
        # Crear un rectángulo de ataque en la dirección que mira el jugador
        attack_rect = self.get_attack_rect()
        
        # Comprobar colisiones con enemigos
        for enemy in enemies:
            if attack_rect.colliderect(enemy.rect):
                if enemy.take_damage(self.attack_power):
                    enemies.remove(enemy)
                    
    def get_attack_rect(self):
        # Simplemente devolver el mismo rectángulo del jugador
        return self.player.rect.copy()
            
        return attack_rect
        
    def take_damage(self, amount, current_time):
        if self.invulnerable:
            return False
            
        self.health -= amount
        self.invulnerable = True
        self.last_hit = current_time
        return self.health <= 0
        
    def update(self, current_time):
        # Actualizar estado de invulnerabilidad
        if self.invulnerable and current_time - self.last_hit >= self.invulnerable_time:
            self.invulnerable = False
            
    def draw_health(self, screen):
        # Dibujar barra de vida del jugador
        bar_width = 200
        bar_height = 20
        x = 10
        y = 10
        
        # Fondo de la barra (rojo)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        
        # Vida actual (verde)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health_width, bar_height))
        
        # Borde de la barra
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)