import pygame
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador
from juego.menu_pausa import pause_menu
from juego.combat_system import CombatSystem, Enemy, CombatPlayer
from assets.mapas.mapa5_data import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    puerta_4_entrada,
    puerta_4_salida,
    colisiones_escaladas
)

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

def ejecutar_mapa5():
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 23
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)

    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2

    puerta4pos = puerta_4_entrada.topleft
    pos_x = puerta4pos[0]
    pos_y = puerta4pos[1] - alto_jugador * 10
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)
    combat_player = CombatPlayer(jugador)
    combat_system = CombatSystem()
    
    # Crear algunos enemigos iniciales
    for _ in range(3):
        x = random.randint(100, ANCHO_PANTALLA - 100)
        y = random.randint(100, ALTO_PANTALLA - 100)
        enemy = Enemy(x, y)
        combat_system.add_enemy(enemy)

    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_pared = os.path.join(BASE_DIR, "assets", "mapas", "pared_mapa_4.png")
    if os.path.exists(ruta_pared):
        imagen_pared = pygame.image.load(ruta_pared).convert_alpha()
        imagen_escalada = pygame.transform.scale(imagen_pared, (ANCHO_PANTALLA, ALTO_PANTALLA))
    else:
        imagen_escalada = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    try:
                        state = {
                            'mapa': 'mapa5',
                            'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y)
                        }
                    except Exception:
                        state = None
                    pause_menu(pantalla, mapa_actual=5, state=state)

        jugador.manejar_teclas()

        pantalla.fill((0, 0, 0))  # Limpiar pantalla

        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))  # Fondo del mapa

        #Dibujar colisiones (opcional para depuración)
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)

        #Dibujar puertas (opcional para depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_4_entrada, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_4_salida, 2)

        # Manejo del combate
        current_time = pygame.time.get_ticks()
        
        # Actualizar y dibujar enemigos
        for enemy in combat_system.enemies[:]:  # Usar una copia de la lista para evitar problemas al eliminar
            enemy.move_towards_player(jugador.rect)
            enemy.draw(pantalla, offset_x, offset_y)
            
            # Ataque del enemigo
            if enemy.can_attack(current_time):
                if pygame.Rect(enemy.rect).colliderect(jugador.rect):
                    if combat_player.take_damage(enemy.attack_power, current_time):
                        print("Game Over")
                        running = False
                    enemy.last_attack = current_time
        
        # Manejo del ataque del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and combat_player.can_attack(current_time):
            jugador.estado = "attack"
            combat_player.attack(current_time, combat_system.enemies)
            
        # Actualizar jugador y sistema de combate
        combat_player.update(current_time)
        jugador.dibujar(pantalla, offset_x, offset_y)
        combat_player.draw_health(pantalla)

        if imagen_escalada:
            pantalla.blit(imagen_escalada, (0, 0))  # Después la imagen → queda arriba del jugador

        # Debug: dibujar área de ataque cuando el jugador está atacando
        if jugador.estado == "attack":
            attack_rect = combat_player.get_attack_rect()
            pygame.draw.rect(pantalla, (255, 255, 0), attack_rect.move(offset_x, offset_y), 2)

        pygame.display.flip()
        clock.tick(60)

        # Transiciones de mapa
        if jugador.rect.colliderect(puerta_4_salida):
            print("Transición al siguiente mapa")
            running = False  # Aquí puedes llamar al siguiente mapa si lo tienes
        # Ya no se permite volver al mapa anterior ni cerrar la ejecución si se toca la entrada

    pygame.quit()
    sys.exit()