# Mejoras del Sistema de Combate

## 📊 Resumen de Cambios

Se han implementado mejoras significativas al sistema de combate para hacerlo más desafiante, visual y estratégico.

## 🎮 Mejoras Principales

### 1. **Sistema de Knockback Mejorado**
- Los enemigos ahora retroceden cuando son golpeados
- Knockback con fricción realista que disminuye gradualmente
- Duración configurable (300ms por defecto)
- Enemigos no pueden moverse durante knockback
- Resistencia a knockback (0.85 de fricción)

**Uso:**
```python
enemy.apply_knockback_force(force_x, force_y, duration=250)
```

### 2. **IA del Enemigo Mejorada**
- 3 comportamientos de combate:
  - **Chase**: Persecución directa al jugador
  - **Dash**: Embestida rápida cuando está arriba de 50% de salud (1.8x velocidad)
  - **Circle**: Movimiento evasivo lateral

- Sistema de decisiones inteligentes cada 2 segundos
- Ajuste de velocidad según comportamiento
- Mejor orientación hacia el objetivo

### 3. **Sistema de Parry/Defensa del Jugador**
- Nueva mecánica: presionar una tecla para defenderse
- Ventana de parry: 200ms para reaccionar defensivamente
- Cooldown: 600ms entre defensas
- Al paryar un ataque: reduce el daño a 25%
- Consumo único: se consume al usarlo exitosamente

**Uso:**
```python
combat_player.start_parry(current_time)  # Iniciar defensa
if combat_player.is_parrying(current_time):  # Comprobar si está defendiendo
    pass
```

### 4. **Sistema de Combos Mejorado**
- Contador de golpes conectados
- Multiplicador de daño por combo (hasta 1.5x)
- Ventana de combo: 1 segundo sin golpear resetea
- Estadísticas de combate:
  - Total de daño causado
  - Cantidad de golpes críticos
  - Golpes recibidos

### 5. **Golpes Críticos**
- 20% de probabilidad por ataque
- 1.5x de daño multiplicador
- Efecto visual diferenciado (estrellas amarillas)
- Contador de críticos en estadísticas

### 6. **Efectos Visuales de Combate**
- Sistema de efectos expandible:
  - **Impact**: Círculo de impacto que se expande
  - **Crit**: Estrellas destellantes de golpe crítico
  - **Heal**: Partículas verdes ascendentes
  
- Cada efecto tiene duración (200ms por defecto)
- Alpha progresiva para desvanecimiento suave
- Colores diferenciados por tipo

**Uso:**
```python
combat_system.add_hit_effect(x, y, effect_type="impact")
```

### 7. **Flash de Daño del Jugador**
- El sprite del jugador parpadea al recibir daño
- Duración: 200ms de flash visual
- Indica claramente cuándo fue golpeado
- Sincronizado con período de invulnerabilidad

### 8. **Barra de Vida Mejorada**
- Ahora incluye borde blanco
- Flash rojo durante invulnerabilidad
- Opción para mostrar estadísticas en tiempo real:
  - HP actual/máximo
  - Contador de combo actual
- Método mejorado: `draw_health(screen, show_stats=True)`

### 9. **Detección de Colisiones Optimizada**
- Múltiples rectángulos de ataque para mejor cobertura
- Colisión directa Y por punto central
- Mejor alineación con direcciones del jugador
- Slice de lista para evitar errores durante iteración

### 10. **Estadísticas de Combate**
- `total_damage_dealt`: Daño total inflado
- `critical_hits`: Cantidad de golpes críticos
- `hits_received`: Golpes recibidos por el jugador
- Útil para sistema de puntuación/desafíos

## 🛠️ API de Uso

### Inicializar Sistema de Combate
```python
combat_system = CombatSystem()
combat_player = CombatPlayer(player, combat_system)

# Agregar enemigos
enemy = Enemy(x, y, health=100)
combat_system.add_enemy(enemy)
```

### En el Loop de Juego
```python
current_time = pygame.time.get_ticks()

# Actualizar
combat_system.update_effects(current_time)
combat_player.update(current_time)

# Entrada del jugador
if attack_pressed:
    combat_player.attack(current_time, combat_system.enemies)
    
if defend_pressed:
    combat_player.start_parry(current_time)

# Movimiento de enemigos
for enemy in combat_system.enemies:
    enemy.move_towards_player(player.rect)
    if enemy.can_attack(current_time, player.rect):
        # Aplicar daño al jugador
        player_died = combat_player.take_damage(enemy.attack_power, current_time)

# Dibujo
combat_system.draw_effects(screen, camera_x, camera_y)
for enemy in combat_system.enemies:
    enemy.draw(screen, camera_x, camera_y)
combat_player.draw_health(screen, show_stats=True)
```

## 📈 Parámetros Ajustables

```python
# Enemy
enemy.speed = 2.5  # Velocidad base
enemy.attack_range = 40  # Rango de ataque
enemy.attack_power = 10  # Daño de ataque
enemy.attack_cooldown = 1000  # ms entre ataques
enemy.knockback_resistance = 0.85  # Fricción

# CombatPlayer
combat_player.attack_power = 25  # Daño de ataque
combat_player.attack_cooldown = 400  # ms entre ataques
combat_player.attack_range = 30  # Rango de ataque
combat_player.invulnerable_time = 1200  # ms de invulnerabilidad
combat_player.defense_cooldown = 600  # ms entre defensas
combat_player.parry_window = 200  # ms de ventana de parry
combat_player.combo_window = 1000  # ms para mantener combo
```

## 🎯 Ejemplos de Integración

### Aplicar Knockback
```python
knockback_x = (enemy.rect.centerx - player.rect.centerx) * 0.1
knockback_y = (enemy.rect.centery - player.rect.centery) * 0.1
enemy.apply_knockback_force(knockback_x, knockback_y, duration=250)
```

### Crear Efecto Visual
```python
combat_system.add_hit_effect(enemy.rect.centerx, enemy.rect.centery, "crit")
```

### Estadísticas en Tiempo Real
```python
print(f"Daño: {combat_player.total_damage_dealt}")
print(f"Críticos: {combat_player.critical_hits}")
print(f"Combo: {combat_player.combo_hits}")
```

## 🔧 Próximas Mejoras Sugeridas

- [ ] Sistema de habilidades especiales
- [ ] Enemigos con patrones de ataque avanzados
- [ ] Efectos de sonido y feedback de audio
- [ ] Sistema de drop de items
- [ ] Diálogos dinámicos durante combate
- [ ] Efecto de cámara shake en impactos
- [ ] Enemigos elite con comportamientos únicos
- [ ] Sistema de upgrades de armas
- [ ] Ranks de dificultad dinámicos

## 📝 Notas

- El sistema es completamente modular y puede expanderse fácilmente
- Los efectos visuales usan coordenadas de cámara para integración con sistemas de cámara
- Las estadísticas pueden usarse para sistemas de logros y desafíos
- Knockback es totalmente configurable para balance
