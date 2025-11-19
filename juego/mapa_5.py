import pygame
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador_lvl2 import JugadorLvl2
from juego.menu_pausa import pause_menu
from juego.combat_system import CombatSystem, Enemy, CombatPlayer
from juego.save_system import load_game, save_game
from assets.mapas.mapa5_data import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    TILE_SIZE,
    SCALE_FACTOR,
    puerta_4_entrada,
    puerta_4_salida,
    colisiones_escaladas
)
from assets.mapas.fondo import vida_jugador

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

def ejecutar_mapa5(respect_saved: bool = True):
    clock = pygame.time.Clock()
    running = True

    # Cargar la imagen de vida una sola vez al inicio
    imagen_vida = None
    try:
        # vida_jugador puede ser una ruta (str) o una Surface ya cargada
        if isinstance(vida_jugador, str):
            cargado = pygame.image.load(vida_jugador)
        elif isinstance(vida_jugador, pygame.Surface):
            cargado = vida_jugador
        else:
            raise TypeError(f"vida_jugador tiene un tipo inesperado: {type(vida_jugador)!r}")

        try:
            # Intentar usar convert_alpha si está disponible
            imagen_vida = cargado.convert_alpha()
        except AttributeError as ae:
            # Mensaje detallado y sugestivo si el objeto no soporta convert_alpha
            msg = (
                "GRAN ERROR cargando imagen de vida: el objeto cargado no tiene 'convert_alpha'. "
                f"Tipo del objeto: {type(cargado).__name__}. Detalle del error: {ae}.\n"
                "Asegúrate de que 'vida_jugador' sea la ruta a un fichero de imagen (str) o una "
                "instancia de pygame.Surface válida. Se usará un fallback visual.")
            print(msg)
            # Crear un fallback visual (superficie semitransparente roja)
            imagen_vida = pygame.Surface((250, 90), pygame.SRCALPHA)
            imagen_vida.fill((255, 0, 0, 180))

        # Escalar la imagen/fallback a la dimensión deseada
        imagen_vida = pygame.transform.scale(imagen_vida, (250, 90))  # Ajusta el tamaño según necesites

    except Exception as e:
        # Mensaje amplio de fallo y creación de fallback gris
        print("GRAN ERROR cargando imagen de vida:", e)
        imagen_vida = pygame.Surface((250, 90))
        imagen_vida.fill((128, 128, 128))

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

    # Cargar guardado solo si se permite respetar el save (en ejecuciones dentro del juego)
    if respect_saved:
        _saved = load_game(1) or {}
        mapa5_enemigo_muerto = _saved.get('mapa5_enemigo_muerto', False)
        # Debug: mostrar el estado guardado al iniciar el mapa
        print(f"[mapa_5] saved_state={_saved} mapa5_enemigo_muerto={mapa5_enemigo_muerto}")
    else:
        mapa5_enemigo_muerto = False
        print("[mapa_5] respect_saved=False -> Ignorando save, enemigo vivo para ejecución aislada")

    # Siempre usar JugadorLvl2 ya que si llegó al mapa 5 ya tiene la espada
    jugador = JugadorLvl2(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)
    
    # Crear sistema de combate pero no activarlo aún
    combat_player = CombatPlayer(jugador)
    # Mejorar significativamente el área de ataque del jugador en mapa 5
    # Esto hace que sea más fácil golpear al vampiro sin necesitar tanta precisión
    combat_player.attack_range = 100  # Aumentado el alcance base
    combat_player.attack_width = 120  # Ancho del área de ataque muy amplio
    combat_player.attack_height = 100  # Altura del área de ataque muy amplia
    combat_player.attack_power = 35  # Aumentar el daño para compensar la dificultad de acertar
    combat_system = CombatSystem()
    combate_activo = False
    enemy = None  # Inicializar enemy como None
    
    # Definir zona de combate más grande para facilitar el trigger
    zona_combate = pygame.Rect(
        offset_x + 10 * TILE_SIZE * SCALE_FACTOR,  # x: desde columna 10
        offset_y + 3 * TILE_SIZE * SCALE_FACTOR,   # y: desde fila 3
        10 * TILE_SIZE * SCALE_FACTOR,             # ancho: 10 tiles
        4 * TILE_SIZE * SCALE_FACTOR               # alto: 4 tiles
    )

    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_pared = os.path.join(BASE_DIR, "assets", "mapas", "pared_mapa_5.png")
    if os.path.exists(ruta_pared):
        imagen_pared = pygame.image.load(ruta_pared).convert_alpha()
        imagen_escalada = pygame.transform.scale(imagen_pared, (ANCHO_PANTALLA, ALTO_PANTALLA))
    else:
        imagen_escalada = None

    def animacion_puerta_abierta(pantalla):
        # Cargar sprites de la animación de la puerta
        sprites_animacion_puerta = [
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion/puerta_reja_abrien_escalada(1).png"),
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion/puerta_reja_abrien_escalada(2).png"),
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion/puerta_reja_abrien_escalada(3).png"),
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion/puerta_reja_abrien_escalada(4).png"),
        ]

        # Variables de animación
        sprite_index = 0
        animation_timer = pygame.time.get_ticks()
        animation_speed = 300  # milisegundos entre frames
        animacion_terminada = False

        # Bucle de animación
        while not animacion_terminada:
            current_time = pygame.time.get_ticks()

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        try:
                            state = {
                                'mapa': 'mapa3',
                                'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y)
                            }
                        except Exception:
                            state = None
                        pause_menu(pantalla, mapa_actual=3, state=state)
            
            # Dibujar fondo y jugador
            pantalla.fill((0, 0, 0))
            
            pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
            pantalla.blit(imagen_escalada, (0, 0))
            
            JugadorLvl2.dibujar(jugador, pantalla, offset_x, offset_y)    # Jugador lvl2
           
            
            
            # Dibujar sprite actual de la puerta
            if sprite_index < len(sprites_animacion_puerta):
                imagen_puerta = sprites_animacion_puerta[sprite_index]
                imagen_puerta_escalado= pygame.transform.scale(imagen_puerta, (ANCHO_PANTALLA, ALTO_PANTALLA))
                pantalla.blit(imagen_puerta_escalado, (0, 0))               # Posición de la puerta

            pygame.display.update()

            # Avanzar al siguiente frame si pasó el tiempo
            if current_time - animation_timer > animation_speed:
                sprite_index += 1
                animation_timer = current_time
                if sprite_index >= len(sprites_animacion_puerta):
                    animacion_terminada = True
            # Actualizar pantalla final
            pygame.display.flip()
            clock.tick(60)

    animacion_puerta_abierta(pantalla)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Tecla R para resetear la bandera de enemigo muerto (útil para testing)
                if event.key == pygame.K_r:
                    mapa5_enemigo_muerto = False
                    try:
                        s = load_game(1) or {}
                        s['mapa5_enemigo_muerto'] = False
                        save_game(s, 1)
                        print("[mapa_5] mapa5_enemigo_muerto reseteado por tecla R")
                    except Exception as ex:
                        print(f"[mapa_5] Error reseteando save: {ex}")
                
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
        '''
        #Dibujar colisiones (opcional para depuración)
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)'''

        
        #Dibujar puertas (opcional para depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_4_entrada, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_4_salida, 2)

        # Manejo del combate
        current_time = pygame.time.get_ticks()
        
        # Debug: Mostrar posición del jugador y zona de combate
        if jugador.rect.colliderect(zona_combate):
            print(f"Jugador en zona de combate. Pos: {jugador.rect.topleft}")
            
        # Actualizar y dibujar enemigos
        for enemy in combat_system.enemies[:]:  # Usar una copia de la lista para evitar problemas al eliminar
            enemy.move_towards_player(jugador.rect)
            enemy.draw(pantalla, offset_x, offset_y)
            
            # Ataque del enemigo (iniciar solo si en rango)
            if enemy.can_attack(current_time, jugador.rect):
                if pygame.Rect(enemy.rect).colliderect(jugador.rect):
                    if combat_player.take_damage(enemy.attack_power, current_time):
                        print("Game Over")
                        running = False
                    enemy.last_attack = current_time

        # Debug: Dibujar zona de combate para visualización
        #pygame.draw.rect(pantalla, (255, 0, 0), zona_combate, 2)
        
        # Manejo del ataque del jugador (integrado desde test_combat.py)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and combat_player.can_attack(current_time) and not jugador.atacando:
            # ACTUALIZAR RECT DE ENEMIGOS ANTES DE DETECTAR COLISIÓN
            for enemy_instance in combat_system.enemies[:]:
                if not enemy_instance.is_dead:
                    enemy_instance.update_rect()
            
            # activar animación de ataque en el jugador (igual comportamiento que en test_combat.py)
            jugador.estado = "attack"
            jugador.atacando = True
            jugador.frame_actual = 0
            jugador.contador_tiempo = 0  # Resetear contador de animación
            clave_animacion = f"{jugador.estado}_{jugador.direccion}"
            if clave_animacion in jugador.animaciones:
                jugador.animacion_actual = jugador.animaciones[clave_animacion]
            combat_player.attack(current_time, combat_system.enemies)
            
        # Activar combate si el jugador entra en la zona (sólo si el enemigo no fue eliminado antes)
        if not combate_activo and not mapa5_enemigo_muerto and jugador.rect.colliderect(zona_combate):
            combate_activo = True
            # Crear enemigo cuando se active el combate
            enemy = Enemy(
                zona_combate.centerx,  # Centrado en x en la zona
                zona_combate.centery - TILE_SIZE * SCALE_FACTOR  # Un poco arriba del centro
            )
            # Configurar el enemigo y agregarlo al sistema de combate
            try:
                # Aumentar el rango, ancho y alto de la hitbox del enemigo para cubrir todo su cuerpo
                enemy.set_attack_hitbox(attack_range=45, attack_width=50, attack_height=int(enemy.rect.height * 0.9))
                combat_system.add_enemy(enemy)
                # Mostrar mensaje de inicio de combate
                font = pygame.font.Font(None, 36)
                text = font.render("¡Combate iniciado!", True, (255, 0, 0))
                pantalla.blit(text, (ANCHO_PANTALLA//2 - text.get_width()//2, 50))
            except Exception as e:
                print(f"Error al inicializar el enemigo: {e}")
                combate_activo = False

        # Actualizar jugador y sistema de combate
        combat_player.update(current_time)
        jugador.dibujar(pantalla, offset_x, offset_y)
        
        # Dibujar la imagen de vida del jugador centrada justo encima de la barra de vida
        if imagen_vida:
            try:
                iw, ih = imagen_vida.get_size()
                bx = getattr(combat_player, 'bar_x', 10)
                by = getattr(combat_player, 'bar_y', 10)
                bw = getattr(combat_player, 'bar_width', iw)
                # Centrar horizontalmente sobre la barra.
                pos_x = bx + (bw - iw) // 2
                # Baja la imagen en Y respecto a la posición original para acercarla a la barra.
                # Ajusta este valor (imagen_vida_dy) para subir/bajar la imagen.
                imagen_vida_dy = 20
                pos_y = by - ih + imagen_vida_dy
                pantalla.blit(imagen_vida, (pos_x, pos_y))
            except Exception as e:
                # Fallback: dibujar en la esquina si algo falla
                pantalla.blit(imagen_vida, (10, 10))
        
        # Solo mostrar la barra de vida y enemigos si el combate está activo
        if combate_activo:
            combat_player.draw_health(pantalla)
            # Debug: dibujar área de ataque cuando el jugador está atacando
            if jugador.estado == "attack":
                attack_rect = combat_player.get_attack_rect()
                pygame.draw.rect(pantalla, (255, 255, 0), attack_rect.move(offset_x, offset_y), 2)
            
            # Debug: mostrar zona de combate
            #pygame.draw.rect(pantalla, (0, 0, 255), zona_combate, 2)

            # Verificar si hay enemigos en el sistema de combate
            if len(combat_system.enemies) == 0:
                # Si el enemigo existe y está muerto -> limpiar referencia, desactivar combate y persistir
                if enemy is not None and getattr(enemy, 'is_dead', False):
                    # remover cualquier rastro en la lista por si quedó
                    for e in combat_system.enemies[:]:
                        if getattr(e, 'is_dead', False):
                            combat_system.remove_enemy(e)
                    enemy = None
                    combate_activo = False
                    mapa5_enemigo_muerto = True
                    try:
                        state = load_game(1) or {}
                        state['mapa5_enemigo_muerto'] = True
                        save_game(state, 1)
                        print("[mapa_5] Guardado: enemigo de mapa5 marcado como muerto permanentemente")
                    except Exception as ex:
                        print(f"[mapa_5] Error guardando estado de mapa5: {ex}")
                # Si el enemigo existe y está vivo pero por alguna razón no está en la lista, agregarlo
                elif enemy is not None and not getattr(enemy, 'is_dead', False):
                    if enemy not in combat_system.enemies:
                        combat_system.add_enemy(enemy)
                        try:
                            # Usar los mismos valores aumentados para la hitbox del enemigo
                            enemy.set_attack_hitbox(attack_range=45, attack_width=50, attack_height=int(enemy.rect.height * 0.9))
                        except Exception:
                            pass

            # Actualizar y dibujar enemigos solo si el combate está activo
            for enemy_instance in combat_system.enemies[:]:
                enemy_instance.move_towards_player(jugador.rect)
                enemy_instance.draw(pantalla, offset_x, offset_y)
                
                # Ataque del enemigo
                if enemy_instance.can_attack(current_time, jugador.rect):
                    if pygame.Rect(enemy_instance.rect).colliderect(jugador.rect):
                        if combat_player.take_damage(enemy_instance.attack_power, current_time):
                            print("Game Over")
                            running = False
                        enemy_instance.last_attack = current_time

        #if imagen_escalada:
            #pantalla.blit(imagen_escalada, (0, 0))  # Después la imagen → queda arriba del jugador

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