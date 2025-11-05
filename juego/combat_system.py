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
        self.scale = 3  # Mismo tamaño que en el cuatro en raya
        # El rectángulo se ajustará después de cargar los sprites
        self.rect = pygame.Rect(x, y, 32 * self.scale, 32 * self.scale)
        self.speed = 2.5  # Aumentada la velocidad para que el vampiro se mueva mejor
        self.attack_range = 40  # Alcance reducido para que no pegue desde tan lejos
        self.attack_power = 10
        # Inicializar last_attack para evitar que el enemigo ataque inmediatamente al aparecer
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000  # 1 segundo entre ataques

        # Cargar sprites del vampiro
        self.load_sprites()

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
        # Si está muerto, no hacer nada (ni mover, ni cambiar dirección, ni animación)
        if self.is_dead:
            self.state = "death"
            self.update_animation()
            return

        # Si está atacando, no moverse
        if self.state == "attack":
            return

        # Calcular la dirección hacia el jugador
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)

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
            dx, dy = dx / dist, dy / dist

            # Actualizar posición
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            self.is_moving = True

        else:
            self.is_moving = False

        # El vampiro siempre está en estado "idle" excepto cuando ataca o está muerto
        if not self.is_dead:
            self.state = "idle"

        # Depuración mínima para entender comportamiento (se puede quitar después)
        # Mostrar sólo cuando cambia estado de movimiento para no llenar la consola
        # (siempre que pygame esté inicializado)
        try:
            if hasattr(self, 'last_moving_state'):
                if self.last_moving_state != self.is_moving:
                    print(f"[Enemy] pos={self.rect.topleft} player={player_rect.center} dist={dist:.1f} is_moving={self.is_moving} state={self.state}")
            else:
                print(f"[Enemy] pos={self.rect.topleft} player={player_rect.center} dist={dist:.1f} is_moving={self.is_moving} state={self.state}")
            self.last_moving_state = self.is_moving
        except Exception:
            pass

        self.update_animation()
            
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
                    dx = player_rect.centerx - self.rect.centerx
                    dy = player_rect.centery - self.rect.centery
                    dist = math.hypot(dx, dy)
                    in_range = dist <= self.attack_range

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
        """Devuelve un rectángulo que representa el área alcanzable por el ataque
        según la dirección actual y el valor self.attack_range.
        """
        w = self.attack_width
        h = self.attack_height
        cx, cy = self.rect.centerx, self.rect.centery

        if self.direction == "right":
            rect = pygame.Rect(self.rect.right, self.rect.centery - h // 2, w, h)
        elif self.direction == "left":
            rect = pygame.Rect(self.rect.left - w, self.rect.centery - h // 2, w, h)
        elif self.direction == "up":
            rect = pygame.Rect(self.rect.centerx - h // 2, self.rect.top - w, h, w)
        else:  # down
            rect = pygame.Rect(self.rect.centerx - h // 2, self.rect.bottom, h, w)

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
            # Dibujar el sprite
            screen.blit(current_image, 
                       (self.rect.x + camera_offset_x, 
                        self.rect.y + camera_offset_y))

        # Si está muerto, no dibujar hitbox ni barra de vida
        if self.state == "death":
            return

        # Dibujar rectángulo del área de ataque (debug): el espacio donde el vampiro puede golpear
        try:
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
        """Crear un rectángulo de ataque en la dirección que mira el jugador"""
        attack_width = self.attack_range
        attack_height = int(self.player.rect.height * 0.7)

        # Posición base es el centro del jugador
        player_center = self.player.rect.center
        
        # Crear rectángulo según la dirección
        if self.player.direccion == "derecha":
            return pygame.Rect(self.player.rect.right, 
                             player_center[1] - attack_height//2,
                             attack_width, 
                             attack_height)
        elif self.player.direccion == "izquierda":
            return pygame.Rect(self.player.rect.left - attack_width,
                             player_center[1] - attack_height//2,
                             attack_width,
                             attack_height)
        elif self.player.direccion == "arriba":
            return pygame.Rect(player_center[0] - attack_height//2,
                             self.player.rect.top - attack_width,
                             attack_height,
                             attack_width)
        else:  # abajo
            return pygame.Rect(player_center[0] - attack_height//2,
                             self.player.rect.bottom,
                             attack_height,
                             attack_width)
        
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