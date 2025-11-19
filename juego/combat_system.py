import pygame
import math
import random


class CombatSystem:
    def __init__(self):
        self.enemies = []
        self.projectiles = []
<<<<<<< Updated upstream
        self.hit_effects = []  # Efectos de impacto visuales

=======
        self.hit_effects = []
        self.damage_numbers = []  # Números flotantes de daño
        
>>>>>>> Stashed changes
    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
<<<<<<< Updated upstream

=======
    
    def add_damage_number(self, x, y, damage, is_critical=False):
        """Agregar número de daño flotante"""
        self.damage_numbers.append({
            'x': x,
            'y': y,
            'damage': int(damage),
            'time': pygame.time.get_ticks(),
            'duration': 1000,  # ms
            'is_critical': is_critical
        })
    
>>>>>>> Stashed changes
    def add_hit_effect(self, x, y, effect_type="impact"):
        """Agregar efecto visual de impacto"""
        self.hit_effects.append({
            'x': x,
            'y': y,
            'time': pygame.time.get_ticks(),
            'type': effect_type,
            'duration': 300  # ms
        })

    def update_effects(self, current_time):
        """Actualizar y limpiar efectos de combate"""
<<<<<<< Updated upstream
        self.hit_effects = [e for e in self.hit_effects if current_time - e['time'] < e['duration']]

=======
        self.hit_effects = [e for e in self.hit_effects 
                           if current_time - e['time'] < e['duration']]
        self.damage_numbers = [d for d in self.damage_numbers
                              if current_time - d['time'] < d['duration']]
    
>>>>>>> Stashed changes
    def draw_effects(self, screen, camera_offset_x=0, camera_offset_y=0):
        """Dibujar efectos visuales y números de daño"""
        current_time = pygame.time.get_ticks()
        
        # Dibujar efectos de impacto
        for effect in self.hit_effects:
            elapsed = current_time - effect['time']
            progress = elapsed / effect['duration']

            if effect['type'] == "impact":
<<<<<<< Updated upstream
                radius = int(10 + progress * 20)
                color = (255, int(150 * (1 - progress)), 0)
                pygame.draw.circle(screen, color,
                                   (int(effect['x'] + camera_offset_x), int(effect['y'] + camera_offset_y)),
                                   radius, 2)
            elif effect['type'] == "heal":
                offset_y = int(progress * -30)
                pygame.draw.circle(screen, (0, 255, 0),
                                   (int(effect['x'] + camera_offset_x), int(effect['y'] + camera_offset_y + offset_y)),
                                   3)
            elif effect['type'] == "crit":
                size = int(5 + progress * 5)
                pygame.draw.polygon(screen, (255, 255, 0),
                                    [(int(effect['x'] + camera_offset_x), int(effect['y'] + camera_offset_y - size)),
                                     (int(effect['x'] + camera_offset_x + size), int(effect['y'] + camera_offset_y)),
                                     (int(effect['x'] + camera_offset_x), int(effect['y'] + camera_offset_y + size)),
                                     (int(effect['x'] + camera_offset_x - size), int(effect['y'] + camera_offset_y))], 2)


class HitEffect:
    """Efecto visual simple para impactos"""

    def __init__(self, x, y, lifetime=300):
        self.x = x
        self.y = y
        self.lifetime = lifetime
        self.creation_time = pygame.time.get_ticks()

    def is_alive(self):
        return pygame.time.get_ticks() - self.creation_time < self.lifetime

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0):
        elapsed = pygame.time.get_ticks() - self.creation_time
        progress = elapsed / self.lifetime
        radius = int(10 + progress * 15)
        color = (255, 100, 0)
        pygame.draw.circle(screen, color,
                           (int(self.x + camera_offset_x), int(self.y + camera_offset_y)),
                           radius, 2)

=======
                radius = int(15 + progress * 25)
                alpha = int(255 * (1 - progress))
                color = (255, int(150 * (1 - progress)), 0)
                pygame.draw.circle(screen, color,
                                 (int(effect['x'] + camera_offset_x),
                                  int(effect['y'] + camera_offset_y)),
                                 radius, 3)
            elif effect['type'] == "heal":
                offset_y = int(progress * -40)
                size = int(5 * (1 - progress))
                pygame.draw.circle(screen, (0, 255, 100),
                                 (int(effect['x'] + camera_offset_x),
                                  int(effect['y'] + camera_offset_y + offset_y)),
                                 size)
            elif effect['type'] == "crit":
                size = int(8 + math.sin(progress * math.pi) * 10)
                for i in range(4):
                    angle = (progress * 360 + i * 90) * (math.pi / 180)
                    x_offset = math.cos(angle) * size
                    y_offset = math.sin(angle) * size
                    pygame.draw.circle(screen, (255, 255, 0),
                                     (int(effect['x'] + camera_offset_x + x_offset),
                                      int(effect['y'] + camera_offset_y + y_offset)),
                                     3)
            elif effect['type'] == "parry":
                # Efecto de parry exitoso
                radius = int(20 + progress * 30)
                for i in range(3):
                    r = radius + i * 5
                    alpha = int(200 * (1 - progress))
                    pygame.draw.circle(screen, (100, 100, 255),
                                     (int(effect['x'] + camera_offset_x),
                                      int(effect['y'] + camera_offset_y)),
                                     r, 2)
        
        # Dibujar números de daño flotantes
        font = pygame.font.Font(None, 32)
        for dmg in self.damage_numbers:
            elapsed = dmg['time'] - current_time + dmg['duration']
            progress = elapsed / dmg['duration']
            
            # Movimiento hacia arriba
            offset_y = int((1 - progress) * -50)
            alpha = int(255 * progress)
            
            # Color según tipo
            if dmg['is_critical']:
                color = (255, 215, 0)  # Dorado para críticos
                size = 40
            else:
                color = (255, 255, 255)
                size = 32
            
            # Renderizar texto
            text = font.render(str(dmg['damage']), True, color)
            if size != 32:
                text = pygame.transform.scale(text, 
                    (int(text.get_width() * size / 32), 
                     int(text.get_height() * size / 32)))
            
            pos = (int(dmg['x'] + camera_offset_x - text.get_width() // 2),
                   int(dmg['y'] + camera_offset_y + offset_y))
            screen.blit(text, pos)
>>>>>>> Stashed changes

class Enemy:
    def __init__(self, x, y, health=100, difficulty=1.0):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
<<<<<<< Updated upstream
        self.scale = 3  # Mismo tamaño que en el cuatro en raya

        # Velocidad ligeramente reducida por defecto
        self.speed = 2.0
        self.attack_range = 40
        self.attack_power = 10

        # Inicializar last_attack para evitar ataques inmediatos
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 2500  # ms (2.5 segundos entre ataques)

        # Knockback
        self.knockback_velocity_x = 0
        self.knockback_velocity_y = 0
        self.is_knocked_back = False
        self.knockback_duration = 300
        self.knockback_end_time = 0
        self.knockback_resistance = 0.85

=======
        self.scale = 3
        self.rect = pygame.Rect(x, y, 32 * self.scale, 32 * self.scale)
        
        # Estadísticas escaladas por dificultad
        self.difficulty = difficulty
        self.speed = 2.5 * difficulty
        self.attack_range = 45
        self.attack_power = int(10 * difficulty)
        self.defense = int(5 * difficulty)  # Reducción de daño
        
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = max(1500, int(2500 / difficulty))  # Más rápido con mayor dificultad
        
>>>>>>> Stashed changes
        # Sistema de knockback mejorado
        self.knockback_velocity_x = 0
        self.knockback_velocity_y = 0
        self.is_knocked_back = False
        self.knockback_duration = 300
        self.knockback_end_time = 0
        self.knockback_resistance = 0.85

        # Cargar sprites
        self.load_sprites()

<<<<<<< Updated upstream
        # Inicializar rect basado en el sprite cargado (fallback seguro)
        # Si hay una animación disponible, usar el primer frame como tamaño; si no, usar un tamaño por defecto
        try:
            first_image = None
            # Preferir idle/down si existe
            if self.animations.get("idle", {}).get("down"):
                lst = self.animations["idle"]["down"]
                if lst:
                    first_image = lst[0]
            # Si no hay idle/down, buscar cualquier frame cargado
            if first_image is None:
                for state in self.animations.values():
                    if isinstance(state, dict):
                        for dir_list in state.values():
                            if dir_list:
                                first_image = dir_list[0]
                                break
                        if first_image:
                            break

            if first_image:
                w, h = first_image.get_width(), first_image.get_height()
            else:
                # fallback razonable (32px * scale)
                w, h = 32 * self.scale, 32 * self.scale
        except Exception:
            w, h = 32 * self.scale, 32 * self.scale


        # Crear el rect en la posición inicial
        self.rect = pygame.Rect(int(self.x), int(self.y), int(w), int(h))

        # Protección breve tras aparecer para evitar que el enemigo "nazca encima" del jugador
        self.spawn_time = pygame.time.get_ticks()
        self.spawn_protection_time = 800  # ms durante los cuales no perseguirá activamente al jugador

        # Flag de muerte
=======
        # Estados
>>>>>>> Stashed changes
        self.is_dead = False
        self.death_animation_played = False
        self.is_stunned = False
        self.stun_end_time = 0

        # Animación
        self.current_sprite = 0
        self.animation_speed = 0.13
        self.last_update = pygame.time.get_ticks()
        self.state = "idle"
        self.direction = "down"
        self.is_moving = False
<<<<<<< Updated upstream

        # Parámetros de hitbox de ataque (ajustables)
        # attack_width: profundidad/alcance del área en la dirección que mira
        # attack_height: tamaño perpendicular (alto para ataques verticales o ancho para horizontales)
=======
        
        # Hitbox de ataque
>>>>>>> Stashed changes
        self.attack_width = int(self.attack_range * 0.8)
        self.attack_height = int(self.rect.height * 0.6)
        
        # IA mejorada
        self.decision_timer = 0
        self.decision_interval = 1500
        self.behavior_state = "chase"
        self.aggro_range = 300  # Rango de detección
        self.retreat_threshold = 0.3  # Retroceder si HP < 30%
        
        # Sistema de telegrafía de ataques
        self.telegraph_time = 0
        self.telegraph_duration = 400  # Tiempo antes de atacar (ms)
        self.is_telegraphing = False
        
    def load_sprites(self):
        """Cargar sprites del vampiro"""
        self.animations = {
            "idle": {"up": [], "down": [], "left": [], "right": []},
            "attack": {"up": [], "down": [], "left": [], "right": []},
            "death": {"up": [], "down": [], "left": [], "right": []}
        }
        
        dirs = {
            "up": "arriba",
            "down": "abajo",
            "left": "izquierda",
            "right": "derecha"
        }
        
        # Cargar animaciones (idle, death, attack)
        for direction in ["up", "down", "left", "right"]:
            # Idle (4 frames)
            for i in range(1, 5):
                try:
                    path = f"assets/sprites_vampiro1/Vampires1_Idle/idle_{dirs[direction]}/vampiro1_idle_{dirs[direction]} ({i}).png"
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))
                    self.animations["idle"][direction].append(image)
                except FileNotFoundError:
                    continue

            # Death (11 frames)
            for i in range(1, 12):
                try:
                    path = f"assets/sprites_vampiro1/Vampires1_Death/death_{dirs[direction]}/vampiro1_death_{dirs[direction]} ({i}).png"
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))
                    self.animations["death"][direction].append(image)
                except FileNotFoundError:
                    continue
        
            # Attack (12 frames)
            for i in range(1, 13):
                try:
                    path = f"assets/sprites_vampiro1/Vampires1_Attack/attack_{dirs[direction]}/vampiro1_attack_{dirs[direction]} ({i}).png"
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))
                    self.animations["attack"][direction].append(image)
                except FileNotFoundError:
                    continue
        
        # Establecer animación inicial
        if self.animations["idle"]["down"]:
            self.current_animation = self.animations["idle"]["down"]
        
    def move_towards_player(self, player_rect):
        """IA mejorada con comportamientos tácticos"""
        current_time = pygame.time.get_ticks()
        # Si acabó de aparecer, darle una breve protección para no perseguir inmediatamente
        if (hasattr(self, 'spawn_time') and hasattr(self, 'spawn_protection_time')
                and player_rect is not None):
            if current_time - self.spawn_time < self.spawn_protection_time:
                # Si está muy cerca o colisiona con el jugador, empujarle ligeramente hacia atrás
                dx = player_rect.centerx - self.rect.centerx
                dy = player_rect.centery - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist == 0:
                    # Si coinciden exactamente, desplazar en X negativo
                    nx, ny = -1, 0
                else:
                    nx, ny = -dx / dist, -dy / dist

                # Si están superpuestos o a distancia muy corta, empujar
                if self.rect.colliderect(player_rect) or dist < max(1, self.attack_range * 0.6):
                    push_amount = int(self.speed * 8)
                    self.rect.x += int(nx * push_amount)
                    self.rect.y += int(ny * push_amount)

                # No perseguir durante la protección: actualizar animación y salir
                self.update_animation()
                self.is_moving = False
                return
        
        if self.is_dead:
            self.state = "death"
            self.update_animation()
            return

        # Aplicar stun
        if self.is_stunned:
            if current_time >= self.stun_end_time:
                self.is_stunned = False
            else:
                self.update_animation()
                return

        # Aplicar knockback
        if self.is_knocked_back:
            self.apply_knockback(current_time)
            self.update_animation()
            return

        # Si está atacando o telegrafando, no moverse
        if self.state == "attack" or self.is_telegraphing:
            return

        # Calcular distancia y dirección
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)

        # Actualizar comportamiento
        self.decision_timer += 16  # ~60 FPS
        if self.decision_timer > self.decision_interval:
            self.decision_timer = 0
            health_ratio = self.health / self.max_health
            
            if health_ratio < self.retreat_threshold:
                # Retroceder si HP bajo
                self.behavior_state = "retreat"
            elif dist < self.attack_range * 1.5:
                # Comportamiento agresivo cerca
                self.behavior_state = "dash" if random.random() > 0.5 else "circle"
            elif dist > self.aggro_range:
                # Patrullar si está lejos
                self.behavior_state = "patrol"
            else:
                # Perseguir normalmente
                self.behavior_state = "chase"

        # Actualizar dirección (siempre mirar al jugador)
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"

        # Ejecutar comportamiento
        should_move = dist > self.attack_range
        
        if should_move and dist != 0:
            dx_norm, dy_norm = dx / dist, dy / dist
            
            if self.behavior_state == "retreat":
                # Retroceder del jugador
                dx_norm, dy_norm = -dx_norm, -dy_norm
                speed_mult = 1.3
            elif self.behavior_state == "dash":
                # Embestida rápida
                speed_mult = 1.8
            elif self.behavior_state == "circle":
                # Movimiento circular
                dx_norm, dy_norm = -dy_norm, dx_norm
                speed_mult = 0.9
            elif self.behavior_state == "patrol":
                # Movimiento aleatorio
                angle = random.random() * 2 * math.pi
                dx_norm = math.cos(angle)
                dy_norm = math.sin(angle)
                speed_mult = 0.5
            else:
                # Chase normal
                speed_mult = 1.0

            self.rect.x += dx_norm * self.speed * speed_mult
            self.rect.y += dy_norm * self.speed * speed_mult
            self.is_moving = True
        else:
            self.is_moving = False

        if not self.is_dead:
            self.state = "idle"

        self.update_animation()
    
    def apply_knockback(self, current_time):
        """Aplicar efecto de knockback"""
        if not self.is_knocked_back:
            return
        
        self.rect.x += self.knockback_velocity_x
        self.rect.y += self.knockback_velocity_y
        
        self.knockback_velocity_x *= self.knockback_resistance
        self.knockback_velocity_y *= self.knockback_resistance
        
        if (current_time >= self.knockback_end_time or 
            (abs(self.knockback_velocity_x) < 0.1 and abs(self.knockback_velocity_y) < 0.1)):
            self.is_knocked_back = False
            self.knockback_velocity_x = 0
            self.knockback_velocity_y = 0
    
    def apply_knockback_force(self, force_x, force_y, duration=300):
        """Aplicar fuerza de knockback"""
        self.is_knocked_back = True
        self.knockback_velocity_x = force_x
        self.knockback_velocity_y = force_y
        self.knockback_end_time = pygame.time.get_ticks() + duration
        self.knockback_duration = duration
    
    def apply_stun(self, duration=500):
        """Aplicar efecto de aturdimiento"""
        self.is_stunned = True
        self.stun_end_time = pygame.time.get_ticks() + duration
            
    def can_attack(self, current_time, player_rect=None):
        """Determinar si puede atacar con sistema de telegrafía"""
        # Si está telegrafando, esperar a que termine
        if self.is_telegraphing:
            if current_time >= self.telegraph_time + self.telegraph_duration:
                self.is_telegraphing = False
                self.state = "attack"
                self.current_sprite = 0
                self.last_attack = current_time
                return True
            return False
        
        # Si está atacando, esperar a que termine
        if self.state == "attack":
            if len(self.animations.get("attack", {}).get(self.direction, [])) > 0:
                attack_frames = len(self.animations["attack"][self.direction])
                time_in_attack = current_time - self.last_attack
                attack_duration = attack_frames * (self.animation_speed * 1000 * 1.5)
                if time_in_attack < attack_duration:
                    return False
                else:
                    self.state = "idle"

        # Comprobar si puede iniciar telegraph
        in_range = False
        if player_rect is not None:
            if self.rect.colliderect(player_rect):
                in_range = True
            else:
                attack_rect = self.get_attack_rect()
                if attack_rect.colliderect(player_rect):
                    in_range = True
                else:
                    dx = player_rect.centerx - self.rect.centerx
                    dy = player_rect.centery - self.rect.centery
                    dist = (dx*dx + dy*dy) ** 0.5
                    in_range = dist <= self.attack_range * 1.5

        cooldown_ok = (current_time - self.last_attack) >= self.attack_cooldown
        facing_ok = self.is_facing_player(player_rect) if player_rect else True

        if cooldown_ok and in_range and facing_ok:
            # Iniciar telegrafía del ataque
            self.is_telegraphing = True
            self.telegraph_time = current_time
            return False

        return False
        
    def take_damage(self, amount, is_critical=False):
        """Recibir daño con sistema de defensa"""
        # Aplicar defensa
        actual_damage = max(1, amount - self.defense)
        
        # Crítico ignora defensa
        if is_critical:
            actual_damage = amount
        
        self.health -= actual_damage
        
        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.state = "death"
            self.current_sprite = 0
            self.last_update = pygame.time.get_ticks()
        
        return self.health <= 0, actual_damage

    def get_attack_rect(self):
        """Obtener rectángulo de ataque"""
        attack_width = self.rect.width * 1.0
        attack_height = self.rect.height * 1.0

        if self.direction == "right":
            rect = pygame.Rect(self.rect.right, self.rect.top, attack_width, attack_height)
        elif self.direction == "left":
            rect = pygame.Rect(self.rect.left - attack_width, self.rect.top, attack_width, attack_height)
        elif self.direction == "up":
            rect = pygame.Rect(self.rect.left, self.rect.top - attack_height, attack_width, attack_height)
        else:
            rect = pygame.Rect(self.rect.left, self.rect.bottom, attack_width, attack_height)

        return rect

    def set_attack_hitbox(self, attack_range=None, attack_width=None, attack_height=None):
        """Ajusta parámetros de la hitbox de ataque del enemigo.

        Uso externo (p. ej. mapas) puede llamar a esto para configurar
        attack_range/attack_width/attack_height sin acceder a atributos internos.
        """
        if attack_range is not None:
            try:
                self.attack_range = int(attack_range)
            except Exception:
                pass
        if attack_width is not None:
            try:
                self.attack_width = int(attack_width)
            except Exception:
                pass
        else:
            self.attack_width = int(self.attack_range * 0.8)

        if attack_height is not None:
            try:
                self.attack_height = int(attack_height)
            except Exception:
                pass
        else:
            self.attack_height = int(self.rect.height * 0.6)

    def is_facing_player(self, player_rect):
        """Verificar si está mirando al jugador"""
        if not player_rect:
            return False
            
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery

        if self.direction == "right":
            return dx > 0 and abs(dx) >= abs(dy)
        if self.direction == "left":
            return dx < 0 and abs(dx) >= abs(dy)
        if self.direction == "down":
            return dy > 0 and abs(dy) >= abs(dx)
        if self.direction == "up":
            return dy < 0 and abs(dy) >= abs(dx)
        return False
        
    def update_animation(self):
        """Actualizar animación"""
        current_time = pygame.time.get_ticks()
        if self.state == "death":
            anim_list = self.animations["death"][self.direction]
            if anim_list and current_time - self.last_update > self.animation_speed * 1000:
                self.last_update = current_time
                if self.current_sprite < len(anim_list) - 1:
                    self.current_sprite += 1
                self.current_animation = anim_list
        else:
            if current_time - self.last_update > self.animation_speed * 1000:
                self.last_update = current_time
                anim_list = self.animations.get(self.state, {}).get(self.direction, [])
                
                if not anim_list:
                    anim_list = self.animations.get("idle", {}).get(self.direction, [])

                if anim_list:
                    self.current_sprite = (self.current_sprite + 1) % len(anim_list)
                    self.current_animation = anim_list
                else:
                    self.current_animation = []

    def update_rect(self):
        """Actualizar rectángulo de colisión"""
        try:
            anim = self.animations[self.state][self.direction]
            if anim:
                self.current_animation = anim
            else:
                self.current_animation = self.animations[self.state]["down"]
        except (KeyError, IndexError):
            self.current_animation = self.animations["idle"]["down"] if self.animations["idle"]["down"] else []

        if self.current_animation and len(self.current_animation) > 0:
            current_sprite_index = self.current_sprite % len(self.current_animation)
            current_image = self.current_animation[current_sprite_index]
            self.rect.width = current_image.get_width()
            self.rect.height = current_image.get_height()

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0):
        """Dibujar enemigo con indicadores visuales"""
        current_time = pygame.time.get_ticks()
        
        # Actualizar animación
        animation_speed = self.animation_speed * 1000
        if self.state == "attack":
            animation_speed = animation_speed * 1.5
        elif self.is_moving:
            animation_speed = animation_speed * 0.8

        if self.state == "death":
            self.update_animation()
        else:
            if current_time - self.last_update > animation_speed:
                self.last_update = current_time
                if self.current_animation:
                    self.current_sprite = (self.current_sprite + 1) % len(self.current_animation)

        # Obtener sprite actual
        try:
            anim = self.animations[self.state][self.direction]
            if anim:
                self.current_animation = anim
            else:
                self.current_animation = self.animations[self.state]["down"]
        except (KeyError, IndexError):
            self.current_animation = self.animations["idle"]["down"] if self.animations["idle"]["down"] else []

        if self.current_animation:
            current_sprite_index = self.current_sprite % len(self.current_animation)
            current_image = self.current_animation[current_sprite_index]
            
            self.rect.width = current_image.get_width()
            self.rect.height = current_image.get_height()
            
            # Aplicar tint si está aturdido
            if self.is_stunned:
                tinted = current_image.copy()
                tinted.fill((100, 100, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted, (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))
            else:
                screen.blit(current_image, (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))

        if self.state == "death":
            return

<<<<<<< Updated upstream
        # Dibujar rectángulo del área de ataque (debug) — solo si está habilitado explícitamente
        try:
            if getattr(self, 'show_attack_debug', False):
                attack_rect = self.get_attack_rect()
                # dibujar como contorno rojo
                pygame.draw.rect(screen, (255, 0, 0), attack_rect.move(camera_offset_x, camera_offset_y), 2)
        except Exception:
            pass
=======
        # Dibujar indicador de telegrafía (advertencia de ataque)
        if self.is_telegraphing:
            progress = (current_time - self.telegraph_time) / self.telegraph_duration
            alpha = int(128 + 127 * math.sin(progress * math.pi * 4))
            attack_rect = self.get_attack_rect()
            s = pygame.Surface((attack_rect.width, attack_rect.height), pygame.SRCALPHA)
            s.fill((255, 0, 0, alpha))
            screen.blit(s, (attack_rect.x + camera_offset_x, attack_rect.y + camera_offset_y))
>>>>>>> Stashed changes
        
        # Barra de vida
        health_bar_width = int(self.rect.width * 0.8)
        health_bar_height = 6
        health_ratio = self.health / self.max_health
        
        health_x = self.rect.x + camera_offset_x + (self.rect.width - health_bar_width) // 2
        health_y = self.rect.y + camera_offset_y - 15
        
        # Fondo
        pygame.draw.rect(screen, (40, 40, 40), (health_x, health_y, health_bar_width, health_bar_height))
        
        # Color según HP
        if health_ratio > 0.6:
            color = (0, 255, 0)
        elif health_ratio > 0.3:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        
        pygame.draw.rect(screen, color, (health_x, health_y, int(health_bar_width * health_ratio), health_bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (health_x, health_y, health_bar_width, health_bar_height), 1)

class CombatPlayer:
    def __init__(self, player, combat_system=None):
        self.player = player
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.stamina_regen_rate = 15  # por segundo
        
        self.attack_power = 25
        self.attack_range = 30
        self.last_attack = 0
        self.attack_cooldown = 400
        self.is_attacking = False
        
        self.invulnerable = False
        self.invulnerable_time = 1200
        self.last_hit = 0
        
        # Sistema de combos mejorado
        self.combo_window = 1200
        self.combo_hits = 0
        self.combo_multiplier = 1.0
        self.max_combo_multiplier = 2.5
        self.last_successful_hit = 0
        
        self.combat_system = combat_system
        
        # Sistema de parry/defensa
        self.is_defending = False
        self.defense_cooldown = 600
        self.last_defense = 0
        self.parry_window = 250
        self.parry_active = False
        self.parry_end_time = 0
        self.perfect_parry_window = 100  # Ventana para parry perfecto
        
        # Barra de vida
        self.bar_width = 200
        self.bar_height = 12
        self.bar_x = 30
        self.bar_y = 30
        
        # Efectos visuales
        self.damage_flash = 0
        self.damage_flash_duration = 200
        
        # Estadísticas
        self.total_damage_dealt = 0
        self.critical_hits = 0
        self.hits_received = 0
        self.perfect_parries = 0
        self.combo_record = 0
        
        # Sistema de críticos mejorado
        self.crit_chance = 0.15  # 15% base
        self.crit_damage = 1.75  # 175% daño
        
    def can_attack(self, current_time):
        """Verificar si puede atacar (requiere stamina)"""
        stamina_cost = 20
        return (current_time - self.last_attack >= self.attack_cooldown and 
                self.stamina >= stamina_cost)
    
    def can_parry(self, current_time):
        """Verificar si puede defender/parry"""
        stamina_cost = 15
        return (current_time - self.last_defense >= self.defense_cooldown and
                self.stamina >= stamina_cost)
    
    def start_parry(self, current_time):
        """Iniciar ventana de parry"""
        if self.can_parry(current_time):
            self.parry_active = True
            self.parry_end_time = current_time + self.parry_window
            self.last_defense = current_time
            self.stamina -= 15
            return True
        return False
    
    def is_parrying(self, current_time):
        """Comprobar si está en ventana de parry"""
        return self.parry_active and current_time < self.parry_end_time
    
    def is_perfect_parrying(self, current_time):
        """Comprobar si está en ventana de parry perfecto"""
        return (self.parry_active and 
                current_time < self.last_defense + self.perfect_parry_window)
        
    def attack(self, current_time, enemies):
        """Sistema de ataque mejorado con detección más generosa"""
        if not self.can_attack(current_time):
            return False
        
        # Consumir stamina
        self.stamina -= 20
        self.is_attacking = True
        self.last_attack = current_time
        hit_count = 0
        
        # Calcular multiplicador de combo
        if current_time - self.last_successful_hit < self.combo_window:
            self.combo_multiplier = min(
                self.max_combo_multiplier,
                1.0 + (self.combo_hits * 0.15)
            )
        else:
            self.combo_multiplier = 1.0
            self.combo_hits = 0
        
        attack_rect = self.get_attack_rect()
        
        for enemy in enemies[:]:
            if enemy.is_dead:
                continue
            
            # Detección de colisión mejorada: rectángulo + distancia
            hit = False
            
            # 1. Verificar colisión con rectángulo de ataque (método principal)
            if attack_rect.colliderect(enemy.rect):
                hit = True
            else:
                # 2. Verificar distancia como método secundario (más generoso)
                player_center_x = self.player.rect.centerx
                player_center_y = self.player.rect.centery
                enemy_center_x = enemy.rect.centerx
                enemy_center_y = enemy.rect.centery
                
                dx = enemy_center_x - player_center_x
                dy = enemy_center_y - player_center_y
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Verificar si está en rango de ataque generoso (150 píxeles)
                max_attack_distance = 150
                
                if distance < max_attack_distance:
                    # Verificar si está aproximadamente en la dirección correcta
                    if self.player.direccion == "derecha" and dx > 0 and abs(dx) > abs(dy) * 0.5:
                        hit = True
                    elif self.player.direccion == "izquierda" and dx < 0 and abs(dx) > abs(dy) * 0.5:
                        hit = True
                    elif self.player.direccion == "abajo" and dy > 0 and abs(dy) > abs(dx) * 0.5:
                        hit = True
                    elif self.player.direccion == "arriba" and dy < 0 and abs(dy) > abs(dx) * 0.5:
                        hit = True
            
            if hit:
                # Calcular crítico
                is_critical = random.random() < (self.crit_chance + self.combo_hits * 0.02)
                
                # Calcular daño
                base_damage = self.attack_power * self.combo_multiplier
                if is_critical:
                    damage = base_damage * self.crit_damage
                    self.critical_hits += 1
                else:
                    damage = base_damage
                
                # Aplicar knockback
                dx = enemy.rect.centerx - self.player.rect.centerx
                dy = enemy.rect.centery - self.player.rect.centery
                dist_norm = (dx*dx + dy*dy) ** 0.5
                
                if dist_norm > 0:
                    knockback_strength = 10 if is_critical else 8
                    knockback_x = (dx / dist_norm) * knockback_strength
                    knockback_y = (dy / dist_norm) * knockback_strength
                else:
                    knockback_x = 10 if is_critical else 8
                    knockback_y = 0
                
                enemy.apply_knockback_force(knockback_x, knockback_y, duration=300)
                
                # Stun en crítico
                if is_critical:
                    enemy.apply_stun(duration=600)
                
                # Aplicar daño
                is_dead, actual_damage = enemy.take_damage(int(damage), is_critical)
                
                if is_dead:
                    enemies.remove(enemy)
                
                hit_count += 1
                
                # Efectos visuales
                if self.combat_system:
                    effect_type = "crit" if is_critical else "impact"
                    self.combat_system.add_hit_effect(
                        enemy.rect.centerx, 
                        enemy.rect.centery, 
                        effect_type
                    )
                    self.combat_system.add_damage_number(
                        enemy.rect.centerx,
                        enemy.rect.centery - 20,
                        actual_damage,
                        is_critical
                    )
                
                # Actualizar estadísticas
                self.total_damage_dealt += int(actual_damage)
                
                # Debug
                crit_text = " [CRÍTICO]" if is_critical else ""
                combo_text = f" x{self.combo_multiplier:.1f}" if self.combo_multiplier > 1.0 else ""
                print(f"[HIT] Daño: {int(actual_damage)}{crit_text}{combo_text}")
        
        # Actualizar combo
        if hit_count > 0:
            self.combo_hits += hit_count
            self.last_successful_hit = current_time
            self.combo_record = max(self.combo_record, self.combo_hits)
            print(f"[COMBO] {self.combo_hits} golpes - Multiplicador: x{self.combo_multiplier:.2f}")
        
        return hit_count > 0
                    
    def get_attack_rect(self):
        """Crear rectángulo de ataque muy generoso para mejor jugabilidad"""
        # Área de ataque mucho más grande y generosa
        base_width = self.player.rect.width * 2.5  # 250% del tamaño del jugador
        base_height = self.player.rect.height * 2.5
        
        # Alcance extendido en la dirección del ataque
        attack_reach = 80  # Alcance adicional en píxeles
        
        if self.player.direccion == "derecha":
            # Área ancha y alta, extendida hacia la derecha
            return pygame.Rect(
                self.player.rect.right - 20,  # Empieza un poco antes del borde
                self.player.rect.centery - base_height // 2,  # Centrado verticalmente
                base_width + attack_reach, 
                base_height
            )
        elif self.player.direccion == "izquierda":
            # Área ancha y alta, extendida hacia la izquierda
            return pygame.Rect(
                self.player.rect.left - base_width - attack_reach + 20,
                self.player.rect.centery - base_height // 2,
                base_width + attack_reach,
                base_height
            )
        elif self.player.direccion == "arriba":
            # Área ancha y alta, extendida hacia arriba
            return pygame.Rect(
                self.player.rect.centerx - base_width // 2,  # Centrado horizontalmente
                self.player.rect.top - base_height - attack_reach + 20,
                base_width,
                base_height + attack_reach
            )
        else:  # abajo
            # Área ancha y alta, extendida hacia abajo
            return pygame.Rect(
                self.player.rect.centerx - base_width // 2,
                self.player.rect.bottom - 20,
                base_width,
                base_height + attack_reach
            )
        
    def take_damage(self, amount, current_time, attacker_pos=None):
        """Recibir daño con sistema de parry mejorado"""
        if self.invulnerable:
            return False
        
        # Parry perfecto: sin daño + contraataque
        if self.is_perfect_parrying(current_time):
            self.perfect_parries += 1
            self.stamina = min(self.max_stamina, self.stamina + 30)  # Recuperar stamina
            if self.combat_system:
                x = self.player.rect.centerx
                y = self.player.rect.centery
                self.combat_system.add_hit_effect(x, y, "parry")
            print("[PARRY PERFECTO] Sin daño + 30 stamina!")
            self.parry_active = False
            return False
        
        # Parry normal: reducir daño
        if self.is_parrying(current_time):
            amount = int(amount * 0.3)  # Solo 30% del daño
            self.parry_active = False
            if self.combat_system:
                x = self.player.rect.centerx
                y = self.player.rect.centery
                self.combat_system.add_hit_effect(x, y, "parry")
            print(f"[PARRY] Daño reducido a {amount}")
        
        self.health -= amount
        self.invulnerable = True
        self.last_hit = current_time
        self.damage_flash = self.damage_flash_duration
        self.hits_received += 1
        
        # Romper combo al recibir daño
        self.combo_hits = 0
        self.combo_multiplier = 1.0
        
        print(f"[DAÑO RECIBIDO] -{amount} HP | HP restante: {self.health}/{self.max_health}")
        
        return self.health <= 0
        
    def update(self, current_time, delta_time=None):
        """Actualizar estado del jugador.

        delta_time: segundos desde el último frame. Si es None, se asume ~1/60s
        para mantener compatibilidad con llamadas que no pasan delta_time.
        """
        if delta_time is None:
            delta_time = 1.0 / 60.0

        # Actualizar invulnerabilidad
        if self.invulnerable and current_time - self.last_hit >= self.invulnerable_time:
            self.invulnerable = False

        # Actualizar flash de daño
        if self.damage_flash > 0:
            self.damage_flash -= delta_time * 1000

        # Regenerar stamina
        if not self.is_attacking and self.stamina < self.max_stamina:
            regen = self.stamina_regen_rate * delta_time
            self.stamina = min(self.max_stamina, self.stamina + regen)

        # Limpiar combos
        if (current_time - self.last_successful_hit) > self.combo_window:
            if self.combo_hits > 0:
                print(f"[COMBO TERMINADO] {self.combo_hits} golpes")
            self.combo_hits = 0
            self.combo_multiplier = 1.0

        # Terminar parry
        if self.parry_active and current_time >= self.parry_end_time:
            self.parry_active = False
            
    def draw_health(self, screen, show_stats=False):
        """Dibujar interfaz de combate mejorada"""
        x = self.bar_x
        y = self.bar_y
        bar_width = self.bar_width
        bar_height = self.bar_height
        
        # === BARRA DE VIDA ===
        # Fondo
        pygame.draw.rect(screen, (40, 40, 40), (x, y, bar_width, bar_height))
        
        # Vida actual con gradiente
        health_width = int((self.health / self.max_health) * bar_width)
        if health_width > 0:
            health_ratio = self.health / self.max_health
            if health_ratio > 0.6:
                color = (0, 200, 0)
            elif health_ratio > 0.3:
                color = (255, 200, 0)
            else:
                color = (255, 50, 50)
            
            # Flash de daño
            if self.damage_flash > 0:
                flash_intensity = int((self.damage_flash / self.damage_flash_duration) * 100)
                color = tuple(min(255, c + flash_intensity) for c in color)
            
            pygame.draw.rect(screen, color, (x, y, health_width, bar_height))
        
        # Borde
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        # Texto de HP
        font = pygame.font.Font(None, 20)
        hp_text = f"{int(self.health)}/{int(self.max_health)}"
        text_surf = font.render(hp_text, True, (255, 255, 255))
        screen.blit(text_surf, (x + bar_width + 10, y - 2))
        
        # === BARRA DE STAMINA ===
        stamina_y = y + bar_height + 5
        stamina_height = 8
        
        # Fondo
        pygame.draw.rect(screen, (40, 40, 40), (x, stamina_y, bar_width, stamina_height))
        
        # Stamina actual
        stamina_width = int((self.stamina / self.max_stamina) * bar_width)
        if stamina_width > 0:
            stamina_color = (0, 150, 255) if self.stamina > 30 else (100, 100, 100)
            pygame.draw.rect(screen, stamina_color, (x, stamina_y, stamina_width, stamina_height))
        
        # Borde
        pygame.draw.rect(screen, (255, 255, 255), (x, stamina_y, bar_width, stamina_height), 1)
        
        # === ESTADÍSTICAS ===
        if show_stats:
            stats_y = stamina_y + stamina_height + 10
            
            # Combo actual
            if self.combo_hits > 0:
                combo_font = pygame.font.Font(None, 32)
                combo_color = (255, 215, 0) if self.combo_hits >= 5 else (255, 255, 255)
                combo_text = f"COMBO x{self.combo_hits}"
                combo_surf = combo_font.render(combo_text, True, combo_color)
                screen.blit(combo_surf, (x, stats_y))
                
                # Multiplicador
                mult_text = f"Daño: x{self.combo_multiplier:.2f}"
                mult_surf = font.render(mult_text, True, (255, 200, 100))
                screen.blit(mult_surf, (x, stats_y + 30))
            
            # Indicador de parry activo
            if self.parry_active:
                parry_font = pygame.font.Font(None, 28)
                time_left = max(0, self.parry_end_time - pygame.time.get_ticks())
                is_perfect = time_left > (self.parry_window - self.perfect_parry_window)
                
                if is_perfect:
                    parry_text = "¡PARRY PERFECTO!"
                    parry_color = (255, 215, 0)
                else:
                    parry_text = "Parry Activo"
                    parry_color = (100, 150, 255)
                
                parry_surf = parry_font.render(parry_text, True, parry_color)
                screen.blit(parry_surf, (ANCHO_PANTALLA // 2 - parry_surf.get_width() // 2, 100))
        
        # === ESTADÍSTICAS FINALES (esquina superior derecha) ===
        # Dibujar únicamente si se solicitó mostrar estadísticas
        if show_stats:
            stats_x = ANCHO_PANTALLA - 250
            stats_font = pygame.font.Font(None, 22)

            stats_lines = [
                f"Daño Total: {int(self.total_damage_dealt)}",
                f"Críticos: {self.critical_hits}",
                f"Combo Máximo: {self.combo_record}",
                f"Parries Perfectos: {self.perfect_parries}",
                f"Golpes Recibidos: {self.hits_received}"
            ]

            for i, line in enumerate(stats_lines):
                text_surf = stats_font.render(line, True, (200, 200, 200))
                screen.blit(text_surf, (stats_x, 30 + i * 25))

# Importar ANCHO_PANTALLA para el HUD
try:
    from configuracion import ANCHO_PANTALLA
except:
    ANCHO_PANTALLA = 800  # Fallback