import pygame
import math


class CombatSystem:
    def __init__(self):
        self.enemies = []
        self.projectiles = []
        self.hit_effects = []  # Efectos de impacto visuales

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def add_hit_effect(self, x, y, effect_type="impact"):
        """Agregar efecto visual de impacto"""
        self.hit_effects.append({
            'x': x,
            'y': y,
            'time': pygame.time.get_ticks(),
            'type': effect_type,
            'duration': 200  # ms
        })

    def update_effects(self, current_time):
        """Actualizar y limpiar efectos de combate"""
        self.hit_effects = [e for e in self.hit_effects if current_time - e['time'] < e['duration']]

    def draw_effects(self, screen, camera_offset_x=0, camera_offset_y=0):
        """Dibujar efectos visuales"""
        current_time = pygame.time.get_ticks()
        for effect in self.hit_effects:
            elapsed = current_time - effect['time']
            progress = elapsed / effect['duration']

            if effect['type'] == "impact":
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


class Enemy:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
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

        # Sistema de knockback mejorado
        self.knockback_velocity_x = 0
        self.knockback_velocity_y = 0
        self.is_knocked_back = False
        self.knockback_duration = 300  # ms
        self.knockback_end_time = 0
        self.knockback_resistance = 0.85  # Fricción de knockback

        # Cargar sprites del vampiro
        self.load_sprites()

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
        self.is_dead = False
        self.death_animation_played = False

        # Variables de animación
        self.current_sprite = 0
        self.animation_speed = 0.15  # Velocidad de animación reducida
        self.last_update = pygame.time.get_ticks()
        self.state = "idle"
        self.direction = "down"

        # Control de movimiento
        self.is_moving = False

        # Parámetros de hitbox de ataque (ajustables)
        # attack_width: profundidad/alcance del área en la dirección que mira
        # attack_height: tamaño perpendicular (alto para ataques verticales o ancho para horizontales)
        self.attack_width = int(self.attack_range * 0.8)
        self.attack_height = int(self.rect.height * 0.6)
        
        # Sistema de comportamiento inteligente
        self.decision_timer = 0
        self.decision_interval = 2000  # Cada 2 segundos toma nuevas decisiones
        self.behavior_state = "chase"  # chase, circle, dash
        
    def load_sprites(self):
        # Diccionario para almacenar las animaciones por dirección
        self.animations = {
            "idle": {"up": [], "down": [], "left": [], "right": []},
            "attack": {"up": [], "down": [], "left": [], "right": []},
            "death": {"up": [], "down": [], "left": [], "right": []}
        }
        
        # Mapeo de nombres de carpetas
        dirs = {
            "up": "arriba",
            "down": "abajo",
            "left": "izquierda",
            "right": "derecha"
        }
        
        # Cargar animación idle (4 frames por dirección)
        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 5):
                try:
                    path = f"assets/sprites_vampiro1/Vampires1_Idle/idle_{dirs[direction]}/vampiro1_idle_{dirs[direction]} ({i}).png"
                    image = pygame.image.load(path)
                    # Escalar la imagen 3 veces su tamaño original, igual que en el cuatro en raya
                    image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))
                    self.animations["idle"][direction].append(image)
                except FileNotFoundError:
                    print(f"No se pudo cargar: {path}")
                    continue

        # Cargar animación death (11 frames por dirección)
        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 12):
                try:
                    path = f"assets/sprites_vampiro1/Vampires1_Death/death_{dirs[direction]}/vampiro1_death_{dirs[direction]} ({i}).png"
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))
                    self.animations["death"][direction].append(image)
                except FileNotFoundError:
                    print(f"No se pudo cargar: {path}")
                    continue
        
        # Cargar animación de ataque (12 frames por dirección)
        for direction in ["up", "down", "left", "right"]:
            for i in range(1, 13):
                try:
                    path = f"assets/sprites_vampiro1/Vampires1_Attack/attack_{dirs[direction]}/vampiro1_attack_{dirs[direction]} ({i}).png"
                    image = pygame.image.load(path)
                    # Escalar la imagen 3 veces su tamaño original
                    image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))
                    self.animations["attack"][direction].append(image)
                except FileNotFoundError:
                    print(f"No se pudo cargar: {path}")
                    continue
        
        # Establecer la animación inicial con fallback
        if self.animations["idle"]["down"]:
            self.current_animation = self.animations["idle"]["down"]
        else:
            # Buscar cualquier animación disponible como fallback
            found = False
            for state_name in self.animations:
                if isinstance(self.animations[state_name], dict):
                    for dir_list in self.animations[state_name].values():
                        if dir_list:
                            self.current_animation = dir_list
                            found = True
                            break
                if found:
                    break
            if not found:
                print("Error: No se pudieron cargar las animaciones básicas")
        
    def move_towards_player(self, player_rect):
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
        
        # Si está muerto, no hacer nada (ni mover, ni cambiar dirección, ni animación)
        if self.is_dead:
            self.state = "death"
            self.update_animation()
            return

        # Aplicar knockback si está activo
        if self.is_knocked_back:
            self.apply_knockback(current_time)
            self.update_animation()
            return

        # Si está atacando, no moverse
        if self.state == "attack":
            return

        # Calcular la dirección hacia el jugador
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)

        # Actualizar comportamiento cada intervalo
        self.decision_timer += 1
        if self.decision_timer > self.decision_interval:
            self.decision_timer = 0
            # IA más agresiva: cambiar comportamiento según situación
            if dist < self.attack_range * 2:
                self.behavior_state = "dash" if self.health > self.max_health * 0.5 else "chase"
            else:
                self.behavior_state = "chase"

        # Determinar si debería moverse
        should_move = dist > self.attack_range

        # Actualizar dirección basada en la posición del jugador (siempre),
        # para que el vampiro "mire" al jugador incluso cuando esté quieto
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"

        if should_move and dist != 0:
            # Normalizar el vector de dirección
            dx_norm, dy_norm = dx / dist, dy / dist
            
            # Aplicar comportamiento
            if self.behavior_state == "dash" and dist > self.attack_range * 1.5:
                # Comportamiento agresivo: embestida rápida
                speed_mult = 1.8
            elif self.behavior_state == "circle":
                # Comportamiento evasivo: movimiento lateral
                dx_norm, dy_norm = -dy_norm, dx_norm
                speed_mult = 0.8
            else:
                # Comportamiento normal: persecución
                speed_mult = 1.0

            # Actualizar posición
            self.rect.x += dx_norm * self.speed * speed_mult
            self.rect.y += dy_norm * self.speed * speed_mult
            self.is_moving = True

        else:
            self.is_moving = False

        # El vampiro siempre está en estado "idle" excepto cuando ataca o está muerto
        if not self.is_dead:
            self.state = "idle"

        self.update_animation()
    
    def apply_knockback(self, current_time):
        """Aplicar efecto de knockback al enemigo"""
        if not self.is_knocked_back:
            return
        
        # Aplicar velocidad de knockback con fricción
        self.rect.x += self.knockback_velocity_x
        self.rect.y += self.knockback_velocity_y
        
        # Aplicar fricción
        self.knockback_velocity_x *= self.knockback_resistance
        self.knockback_velocity_y *= self.knockback_resistance
        
        # Terminar knockback si se acabó el tiempo o la velocidad es muy baja
        if (current_time >= self.knockback_end_time or 
            (abs(self.knockback_velocity_x) < 0.1 and abs(self.knockback_velocity_y) < 0.1)):
            self.is_knocked_back = False
            self.knockback_velocity_x = 0
            self.knockback_velocity_y = 0
    
    def apply_knockback_force(self, force_x, force_y, duration=300):
        """Aplicar fuerza de knockback al enemigo"""
        self.is_knocked_back = True
        self.knockback_velocity_x = force_x
        self.knockback_velocity_y = force_y
        self.knockback_end_time = pygame.time.get_ticks() + duration
        self.knockback_duration = duration
            
    def can_attack(self, current_time, player_rect=None):
        """
        Determina si el enemigo puede iniciar/está en medio de un ataque.
        Si se pasa player_rect, solo iniciará el ataque si el jugador está dentro de attack_range
        o si los rectángulos colisionan.
        """
        # Si ya está en animación de ataque, esperar a que termine
        if self.state == "attack":
            if len(self.animations.get("attack", {}).get(self.direction, [])) > 0:
                attack_frames = len(self.animations["attack"][self.direction])
                time_in_attack = current_time - self.last_attack
                attack_duration = attack_frames * (self.animation_speed * 1000)
                if time_in_attack < attack_duration:
                    return False
                else:
                    self.state = "idle"

        # Comprobar si el jugador está en rango (si se pasó player_rect)
        in_range = False
        if player_rect is not None:
            # Primero comprobar colisión directa con el rect del enemigo
            if self.rect.colliderect(player_rect):
                in_range = True
            else:
                # Construir el rectángulo de ataque y comprobar colisión con él
                attack_rect = self.get_attack_rect()
                if attack_rect.colliderect(player_rect):
                    in_range = True
                else:
                    # Comprobar distancia euclidiana como tercer criterio
                    dx = player_rect.centerx - self.rect.centerx
                    dy = player_rect.centery - self.rect.centery
                    dist = (dx*dx + dy*dy) ** 0.5
                    in_range = dist <= self.attack_range * 1.5  # 50% de margen adicional

        # Verificar cooldown
        cooldown_ok = (current_time - self.last_attack) >= self.attack_cooldown

        # Requerir además que el enemigo esté mirando (aproximadamente) al jugador
        facing_ok = True
        if player_rect is not None:
            facing_ok = self.is_facing_player(player_rect)

        # Solo iniciar ataque si cooldown listo, jugador en rango y enemigo lo está mirando
        if cooldown_ok and (player_rect is None or in_range) and facing_ok:
            if player_rect is not None and not in_range:
                return False
            # iniciar ataque
            self.state = "attack"
            self.current_sprite = 0
            self.last_attack = current_time
            print(f"[ENEMY ATTACK] Enemigo ataca al jugador - Distancia: {((player_rect.centerx - self.rect.centerx)**2 + (player_rect.centery - self.rect.centery)**2)**0.5:.1f}")
            return True

        return False
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.state = "death"
            self.current_sprite = 0
            self.last_update = pygame.time.get_ticks()
        return self.health <= 0

    def get_attack_rect(self):
        """Devuelve un rectángulo que representa el área alcanzable por el ataque.
        Usa el mismo tamaño del rect del enemigo para coherencia con la detección.
        """
        # Usar el tamaño exacto del rect del enemigo actual
        attack_width = self.rect.width * 1.0
        attack_height = self.rect.height * 1.0

        # Crear rectángulo según la dirección - debe tocar exactamente el borde del enemigo
        if self.direction == "right":
            rect = pygame.Rect(self.rect.right, self.rect.top, attack_width, attack_height)
        elif self.direction == "left":
            rect = pygame.Rect(self.rect.left - attack_width, self.rect.top, attack_width, attack_height)
        elif self.direction == "up":
            rect = pygame.Rect(self.rect.left, self.rect.top - attack_height, attack_width, attack_height)
        else:  # down
            rect = pygame.Rect(self.rect.left, self.rect.bottom, attack_width, attack_height)

        return rect

    def set_attack_hitbox(self, attack_range=None, attack_width=None, attack_height=None):
        """Permite ajustar dinámicamente la hitbox del ataque.
        - attack_range: actualiza self.attack_range (distancia máxima considerada)
        - attack_width: profundidad del rectángulo de ataque
        - attack_height: altura (o anchura) del rectángulo de ataque
        """
        if attack_range is not None:
            self.attack_range = int(attack_range)
        if attack_width is not None:
            self.attack_width = int(attack_width)
        else:
            # si no se pasa, mantener relación con attack_range
            self.attack_width = int(self.attack_range * 0.8)
        if attack_height is not None:
            self.attack_height = int(attack_height)
        else:
            self.attack_height = int(self.rect.height * 0.6)

    def is_facing_player(self, player_rect):
        """Comprueba de forma simple si el enemigo está orientado hacia el jugador.
        Usa comparación de ejes: si la dirección es derecha, el jugador debe estar a la derecha, etc.
        Además exige que la componente principal (x o y) sea mayor que la otra para evitar 'mirar' diagonalmente.
        """
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
        current_time = pygame.time.get_ticks()
        if self.state == "death":
            # Animación de muerte: avanzar hasta el último frame y quedarse ahí
            anim_list = self.animations["death"][self.direction]
            if anim_list and current_time - self.last_update > self.animation_speed * 1000:
                self.last_update = current_time
                if self.current_sprite < len(anim_list) - 1:
                    self.current_sprite += 1
                self.current_animation = anim_list
        else:
            if current_time - self.last_update > self.animation_speed * 1000:
                self.last_update = current_time
                # Obtener la lista de frames para el estado y dirección actual
                anim_list = None
                try:
                    state_anim = self.animations.get(self.state)
                    if isinstance(state_anim, dict):
                        anim_list = state_anim.get(self.direction, [])
                    else:
                        anim_list = state_anim
                except Exception:
                    anim_list = None

                # Fallback a idle/down si no hay animación específica
                if not anim_list:
                    anim_list = self.animations.get("idle", {}).get(self.direction, [])

                if anim_list:
                    self.current_sprite = (self.current_sprite + 1) % len(anim_list)
                    self.current_animation = anim_list
                else:
                    # Si no hay ninguna animación, dejar current_animation como lista vacía
                    self.current_animation = []

    def update_rect(self):
        """Actualizar el rect del enemigo basado en el sprite actual.
        Debe llamarse antes de detectar colisiones de ataque para que el rect sea preciso."""
        try:
            # Obtener la animación actual según el estado y dirección
            anim = self.animations[self.state][self.direction]
            if anim:
                self.current_animation = anim
            else:
                self.current_animation = self.animations[self.state]["down"]
        except (KeyError, IndexError):
            self.current_animation = self.animations["idle"]["down"] if self.animations["idle"]["down"] else []

        # Actualizar el rect con el tamaño del sprite actual
        if self.current_animation and len(self.current_animation) > 0:
            current_sprite_index = self.current_sprite % len(self.current_animation)
            current_image = self.current_animation[current_sprite_index]
            # Actualizar width y height del rect sin cambiar la posición
            self.rect.width = current_image.get_width()
            self.rect.height = current_image.get_height()

    def draw(self, screen, camera_offset_x=0, camera_offset_y=0):
        current_time = pygame.time.get_ticks()
        
        # Actualizar animación con velocidad variable
        animation_speed = self.animation_speed * 1000
        if self.state == "attack":
            animation_speed = animation_speed * 1.5  # Ataque más rápido
        elif self.is_moving:
            animation_speed = animation_speed * 0.8  # Movimiento más rápido

        # Si está muerto, solo actualizar animación de muerte
        if self.state == "death":
            self.update_animation()
        else:
            if current_time - self.last_update > animation_speed:
                self.last_update = current_time
                if self.current_animation:
                    self.current_sprite = (self.current_sprite + 1) % len(self.current_animation)

        # Obtener la animación actual según el estado y dirección
        try:
            anim = self.animations[self.state][self.direction]
            if anim:  # Si hay animación para esta dirección
                self.current_animation = anim
            else:  # Si no hay animación para esta dirección, usar la animación hacia abajo
                self.current_animation = self.animations[self.state]["down"]
        except (KeyError, IndexError):
            # Fallback a idle hacia abajo si hay error
            self.current_animation = self.animations["idle"]["down"] if self.animations["idle"]["down"] else []

        if self.current_animation:  # Verificar que haya sprites en la animación
            current_sprite_index = self.current_sprite % len(self.current_animation)
            current_image = self.current_animation[current_sprite_index]
            
            # ACTUALIZAR EL RECT BASADO EN EL SPRITE ACTUAL
            # El rect debe tener el tamaño exacto de la imagen que se está dibujando
            self.rect.width = current_image.get_width()
            self.rect.height = current_image.get_height()
            # Mantener el X y Y actuales pero asegurar que sea el rect del sprite
            
            # Dibujar el sprite
            screen.blit(current_image, 
                       (self.rect.x + camera_offset_x, 
                        self.rect.y + camera_offset_y))

        # Si está muerto, no dibujar hitbox ni barra de vida
        if self.state == "death":
            return

        # Dibujar rectángulo del área de ataque (debug) — solo si está habilitado explícitamente
        try:
            if getattr(self, 'show_attack_debug', False):
                attack_rect = self.get_attack_rect()
                # dibujar como contorno rojo
                pygame.draw.rect(screen, (255, 0, 0), attack_rect.move(camera_offset_x, camera_offset_y), 2)
        except Exception:
            pass
        
        # Dibujar barra de vida encima del vampiro
        health_bar_width = int(self.rect.width * 0.8)  # 80% del ancho del vampiro
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        
        health_x = self.rect.x + camera_offset_x + (self.rect.width - health_bar_width) // 2
        health_y = self.rect.y + camera_offset_y - 10
        
        # Dibujar barra de vida
        pygame.draw.rect(screen, (64, 64, 64),
                        (health_x, health_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (255, 0, 0),
                        (health_x, health_y, health_bar_width * health_ratio, health_bar_height))
        
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
    def __init__(self, player, combat_system=None):
        self.player = player
        self.health = 100
        self.max_health = 100
        self.attack_power = 25
        self.attack_range = 30
        self.last_attack = 0
        self.attack_cooldown = 400  # Reducido a 400ms para ataques más rápidos
        self.is_attacking = False
        self.invulnerable = False
        self.invulnerable_time = 1200  # Aumentado a 1.2 segundos de invulnerabilidad
        self.last_hit = 0
        self.combo_window = 1000  # Ventana de 1 segundo para combos
        self.combo_hits = 0
        self.last_successful_hit = 0
        self.combat_system = combat_system  # Referencia al sistema de combate para efectos
        
        # Sistema de parry/defensa mejorado
        self.is_defending = False
        self.defense_cooldown = 600
        self.last_defense = 0
        self.parry_window = 200  # ms
        self.parry_active = False
        self.parry_end_time = 0
        
        # Parámetros de la barra de vida (expuestos para que otras partes del juego puedan posicionar elementos relativos)
        self.bar_width = 150
        self.bar_height = 10
        self.bar_x = 30
        self.bar_y = 30
        
        # Efectos de daño visual
        self.damage_flash = 0
        self.damage_flash_duration = 200
        
        # Estadísticas de combate
        self.total_damage_dealt = 0
        self.critical_hits = 0
        self.hits_received = 0
        
    def can_attack(self, current_time):
        return current_time - self.last_attack >= self.attack_cooldown
    
    def can_parry(self, current_time):
        """Verificar si puede defender/parry"""
        return current_time - self.last_defense >= self.defense_cooldown
    
    def start_parry(self, current_time):
        """Iniciar ventana de parry"""
        if self.can_parry(current_time):
            self.parry_active = True
            self.parry_end_time = current_time + self.parry_window
            self.last_defense = current_time
            return True
        return False
    
    def is_parrying(self, current_time):
        """Comprobar si está en ventana de parry"""
        return self.parry_active and current_time < self.parry_end_time
        
    def attack(self, current_time, enemies):
        if not self.can_attack(current_time):
            return False
            
        self.is_attacking = True
        self.last_attack = current_time
        hit_count = 0
        
        # Crear área de ataque principal (toca el contorno del enemigo)
        attack_rect = self.get_attack_rect()
        
        # Comprobar colisiones con enemigos
        for enemy in enemies[:]:  # Usar slice para evitar modificación mientras iteramos
            if enemy.is_dead:
                continue
                
            hit = False
            
            # Colisión SOLO con el rectángulo real del enemigo
            # Sin distancia, sin áreas expandidas - debe tocar el contorno
            if attack_rect.colliderect(enemy.rect):
                hit = True
            
            # Si hubo hit, aplicar daño
            if hit:
                # Calcular si es golpe crítico (20% de probabilidad)
                is_critical = current_time % 5 < 1  # Simplificado para demo
                damage = self.attack_power * (1.5 if is_critical else 1.0)
                
                # Aplicar knockback al enemigo
                # Normalizar vector de knockback
                dx = enemy.rect.centerx - self.player.rect.centerx
                dy = enemy.rect.centery - self.player.rect.centery
                dist_norm = (dx*dx + dy*dy) ** 0.5
                
                if dist_norm > 0:
                    knockback_x = (dx / dist_norm) * 8
                    knockback_y = (dy / dist_norm) * 8
                else:
                    knockback_x = 8
                    knockback_y = 0
                
                enemy.apply_knockback_force(knockback_x, knockback_y, duration=250)
                
                # Aplicar daño
                if enemy.take_damage(int(damage)):
                    enemies.remove(enemy)
                    hit_count += 1
                else:
                    hit_count += 1
                
                # Agregar efecto visual
                if self.combat_system:
                    effect_type = "crit" if is_critical else "impact"
                    self.combat_system.add_hit_effect(enemy.rect.centerx, enemy.rect.centery, effect_type)
                
                # Actualizar estadísticas
                self.total_damage_dealt += int(damage)
                if is_critical:
                    self.critical_hits += 1
                
                # Debug: mostrar golpe
                print(f"[HIT] Ataque conectado a {enemy.__class__.__name__} - Daño: {int(damage)}")
        
        # Agregar combo
        if hit_count > 0:
            self.combo_hits += hit_count
            self.last_successful_hit = current_time
            print(f"[COMBO] {self.combo_hits} golpes conectados")
        
        return hit_count > 0
                    
    def get_attack_rect(self):
        """Crear un rectángulo de ataque que toque el contorno del enemigo.
        Usa el mismo tamaño del rect del jugador para coherencia con detección del enemigo."""
        # Usar el tamaño exacto del rect del jugador actual
        attack_width = self.player.rect.width * 1.0  # Mismo ancho del jugador
        attack_height = self.player.rect.height * 1.0  # Mismo alto del jugador
        
        player_center = self.player.rect.center
        
        # Crear rectángulo según la dirección - debe tocar exactamente el borde del jugador
        if self.player.direccion == "derecha":
            return pygame.Rect(self.player.rect.right, 
                             self.player.rect.top,
                             attack_width, 
                             attack_height)
        elif self.player.direccion == "izquierda":
            return pygame.Rect(self.player.rect.left - attack_width,
                             self.player.rect.top,
                             attack_width,
                             attack_height)
        elif self.player.direccion == "arriba":
            return pygame.Rect(self.player.rect.left,
                             self.player.rect.top - attack_height,
                             attack_width,
                             attack_height)
        else:  # abajo
            return pygame.Rect(self.player.rect.left,
                             self.player.rect.bottom,
                             attack_width,
                             attack_height)
        
    def take_damage(self, amount, current_time):
        """Recibir daño con sistema mejorado de defensa y parry"""
        if self.invulnerable:
            return False
        
        # Si está paryando, reducir daño significativamente
        if self.is_parrying(current_time):
            amount = int(amount * 0.25)  # Solo 25% del daño
            self.parry_active = False  # Terminar parry después de usarlo
        
        self.health -= amount
        self.invulnerable = True
        self.last_hit = current_time
        self.damage_flash = self.damage_flash_duration
        self.hits_received += 1
        
        return self.health <= 0
        
    def update(self, current_time):
        # Actualizar estado de invulnerabilidad
        if self.invulnerable and current_time - self.last_hit >= self.invulnerable_time:
            self.invulnerable = False
        
        # Actualizar flash de daño
        if self.damage_flash > 0:
            self.damage_flash -= 16  # Aproximadamente 60 FPS
        
        # Limpiar combos si han pasado demasiado tiempo
        if (current_time - self.last_successful_hit) > self.combo_window:
            self.combo_hits = 0
            
    def draw_health(self, screen, show_stats=False):
        """Dibujar barra de vida y estadísticas opcionales"""
        bar_width = self.bar_width
        bar_height = self.bar_height
        x = self.bar_x
        y = self.bar_y

        # Fondo de la barra de vida (gris)
        pygame.draw.rect(screen, (64, 64, 64),
                        (x, y, bar_width, bar_height))
        
        # Barra de vida actual (verde), con parpadeo si está invulnerable
        health_width = int((self.health / self.max_health) * bar_width)
        if health_width > 0:
            # Flash de daño
            flash_alpha = int((self.damage_flash / self.damage_flash_duration) * 100)
            color_intensity = int(max(0, min(255, 255 - flash_alpha)))
            pygame.draw.rect(screen, (0, color_intensity, 0),
                            (x, y, health_width, bar_height))
        
        # Borde
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        # Mostrar estadísticas si está habilitado
        if show_stats:
            font = pygame.font.SysFont(None, 24)
            stats_text = f"HP: {int(self.health)}/{int(self.max_health)} | Combo: {self.combo_hits}"
            stat_surface = font.render(stats_text, True, (255, 255, 255))
            screen.blit(stat_surface, (x, y - 25))