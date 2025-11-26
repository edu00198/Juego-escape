import pygame
import sys
import os
pygame.init()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .menu_pausa import pause_menu
from juego.cuatro_en_raya import inicio_juego
from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA, ESCALA_JUGADOR
from juego.jugador import Jugador
from juego.mapa_3_2 import ejecutar_mapa4
from assets.mapas.mapa3_4_en_raya_data import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    puerta_4 as puerta,
    colisiones_escaladas
)

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

def ejecutar_mapa4_en_raya():
    acertijo_en_raya = False
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 23
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)

    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2

    puerta4pos = puerta.topleft
    pos_x = puerta4pos[0]
    pos_y = puerta4pos[1] - alto_jugador * 10
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=ESCALA_JUGADOR, colisiones=colisiones_escaladas)

    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    # Imagen decorativa (tablero)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_tablero = os.path.join(BASE_DIR, "assets", "mapas", "tablero.png")
    imagen_tablero = pygame.image.load(ruta_tablero).convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen_tablero, (427, 240))
    pos_tablero = ((ANCHO_PANTALLA - imagen_escalada.get_width()) // 2, 150)

    cuatro_en_raya_ya_jugador = False

    # --- NPC ANIMADO (cargado uno por uno) ---
    ruta_npc_dir = os.path.join(BASE_DIR, "assets", "sprites_vampiro1", "Vampires1_Idle", "idle_abajo")

    npc_idle1 = pygame.image.load(os.path.join(ruta_npc_dir, "vampiro1_idle_abajo (1).png")).convert_alpha()
    npc_idle2 = pygame.image.load(os.path.join(ruta_npc_dir, "vampiro1_idle_abajo (2).png")).convert_alpha()
    npc_idle3 = pygame.image.load(os.path.join(ruta_npc_dir, "vampiro1_idle_abajo (3).png")).convert_alpha()
    npc_idle4 = pygame.image.load(os.path.join(ruta_npc_dir, "vampiro1_idle_abajo (4).png")).convert_alpha()

    # Escalar cada frame 3 veces el tamaño original
    escala_npc = 3
    npc_idle1 = pygame.transform.scale(npc_idle1, (npc_idle1.get_width()*escala_npc, npc_idle1.get_height()*escala_npc))
    npc_idle2 = pygame.transform.scale(npc_idle2, (npc_idle2.get_width()*escala_npc, npc_idle2.get_height()*escala_npc))
    npc_idle3 = pygame.transform.scale(npc_idle3, (npc_idle3.get_width()*escala_npc, npc_idle3.get_height()*escala_npc))
    npc_idle4 = pygame.transform.scale(npc_idle4, (npc_idle4.get_width()*escala_npc, npc_idle4.get_height()*escala_npc))

    # Posición arriba a la derecha
    pos_x_npc = ANCHO_PANTALLA - npc_idle1.get_width() - 250
    pos_y_npc = 300
    npc_rect = pygame.Rect(pos_x_npc, pos_y_npc, npc_idle1.get_width(), npc_idle1.get_height())

    npc_frames = [npc_idle1, npc_idle2, npc_idle3, npc_idle4]
    npc_index = 0
    npc_anim_timer = 0
    npc_anim_speed = 0.15

    fuente = pygame.font.Font(None, 40)
    mostrar_dialogo = False
    dialogo_texto = "¿Te animas a un 4 en línea?"

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    try:
                        state = {
                            'mapa': 'mapa3',
                            'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y)
                        }
                    except Exception:
                        state = None
                    pause_menu(pantalla, mapa_actual=4, state=state)
            if cuatro_en_raya_ya_jugador == False:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if jugador.rect.colliderect(npc_rect):
                        if not mostrar_dialogo:
                            mostrar_dialogo = True
                        else:
                            # Jugar y actualizar acertijo_en_raya según el resultado
                            acertijo_en_raya = inicio_juego()
                            if acertijo_en_raya:
                                dialogo_texto = "¡Felicidades! Has ganado. Puedes continuar."
                                cuatro_en_raya_ya_jugador = True
                            else:
                                dialogo_texto = "Has perdido. ¿Quieres intentarlo de nuevo?"
                                cuatro_en_raya_ya_jugador = False

        # Animación NPC
        npc_anim_timer += npc_anim_speed
        if npc_anim_timer >= 1:
            npc_anim_timer = 0
            npc_index = (npc_index + 1) % len(npc_frames)
        npc_frame_actual = npc_frames[npc_index]

        jugador.manejar_teclas()

        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
        #pygame.draw.rect(pantalla, (0, 0, 255), puerta, 2)

        jugador.dibujar(pantalla, offset_x, offset_y)
        pantalla.blit(imagen_escalada, pos_tablero)
        pantalla.blit(npc_frame_actual, (pos_x_npc, pos_y_npc))
        # Diálogo
        if mostrar_dialogo:
            cuadro_dialogo = pygame.Surface((ANCHO_PANTALLA, 100))
            cuadro_dialogo.fill((0, 0, 0))
            cuadro_dialogo.set_alpha(180)
            pantalla.blit(cuadro_dialogo, (0, ALTO_PANTALLA - 100))
            texto = fuente.render(dialogo_texto, True, (255, 255, 255))
            pantalla.blit(texto, (50, ALTO_PANTALLA - 70))

        pygame.display.flip()

        if jugador.rect.colliderect(puerta) and acertijo_en_raya:
            print("Regresa a mapa 3")
            running = False
            # Llamar a ejecutar_mapa3_2 pasando la superficie (evita TypeError)
            try:
                ejecutar_mapa4(pantalla)
                running = True # cuando se regrese del mapa4            
            except Exception as e:
                print(f"Error al ejecutar mapa 3_2: {e}")
    return
