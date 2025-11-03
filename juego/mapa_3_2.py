import pygame
import sys
import os
import threading
import importlib

# Inicializar Pygame y crear la ventana ANTES de importar módulos que cargan imágenes
pygame.init()
ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
ESCALA_JUGADOR = 2.5  # Factor de escala para el jugador


pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Ahora sí podés importar módulos que usan convert_alpha()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


    

# Pause menu import
from juego import jugador
from juego.jugador import Jugador
from juego.menu_pausa import pause_menu
#from juego.mapa_5 import ejecutar_mapa5
from assets.mapas.mapa4_data import (
    fondo_mapa,
    SCALED_WIDTH,
    SCALED_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    puerta_3_entrada,
    puerta_3_salida_al_mapa_4 as puerta_3_salida,
    puerta_3_engranaje,
    puerta_3_cuatro_en_raya,
    colisiones_escaladas
)

from juego.engranajes import minijuego_engranajes



def ejecutar_mapa4(pantalla, spawn_point=None):
    """
    spawn_point puede ser: 'entrada', 'engranajes', None
    """
    clock = pygame.time.Clock()
    running = True

    ancho_jugador = 23
    alto_jugador = 15

    escala_x = ANCHO_PANTALLA / fondo_mapa.get_width()
    escala_y = ALTO_PANTALLA / fondo_mapa.get_height()
    escala = min(escala_x, escala_y)

    offset_x = (ANCHO_PANTALLA - fondo_mapa.get_width() * escala) // 2
    offset_y = (ALTO_PANTALLA - fondo_mapa.get_height() * escala) // 2

    # Posición inicial del jugador frente a la puerta de entrada
    puerta2pos = puerta_3_entrada.topleft
    pos_x = puerta2pos[0] - ancho_jugador * -10
    pos_y = puerta2pos[1] - alto_jugador * -2
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala= ESCALA_JUGADOR, colisiones=colisiones_escaladas)

    # Fondo escalado
    fondo_escalado = pygame.transform.scale(fondo_mapa, (SCALED_WIDTH, SCALED_HEIGHT))

    # Imagen decorativa encima del jugador (opcional)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_pared = os.path.join(BASE_DIR, "assets", "mapas", "paredes_mapa_4.png")
    imagen_pared = pygame.image.load(ruta_pared).convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen_pared, (1280, 720))

     #estandarte lleno
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ruta_estand_de_armadura_lleno = os.path.join(BASE_DIR, "assets", "mapas", "estand_de_armadura_lleno.png")
    imagen_estand_de_armadura_lleno = pygame.image.load(ruta_estand_de_armadura_lleno).convert_alpha()
    imagen_estand_de_armadura_lleno_escalado = pygame.transform.scale(imagen_estand_de_armadura_lleno, (1280, 720))

    print("Tamaño original pared:", imagen_pared.get_size())
    print("Tamaño original estandarte:", imagen_estand_de_armadura_lleno.get_size())


    # Cargar sprites de animación de puerta
    sprites_animacion_puerta = [
        pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(1).png"),
        pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(2).png"),
        pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(3).png"),
        pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(4).png"),
        pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(5).png"),
        
    ]

        # Variables de animación
        # Reproducir animación de puerta con fondo y jugador visibles
    sprite_index = 0
    animation_timer = pygame.time.get_ticks()
    animation_speed = 300  # milisegundos entre frames
    animacion_terminada = False

    # Puntos de profundidad visual (ajustalos según el diseño de tus sprites)
    pie_y_pared = 450  # punto visual donde la pared toca el suelo
    pie_y_imagen_escalada = 600  # ajustá este valor si querés que imagen_escalada tenga profundidad

    while not animacion_terminada:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    try:
                        state = {
                            'mapa': 'mapa4',
                            # no jugador aún en este punto de la animación
                        }
                    except Exception:
                        state = None
                    pause_menu(pantalla, mapa_actual=4, state=state)

        if current_time - animation_timer > animation_speed:
            sprite_index += 1
            animation_timer = current_time
            if sprite_index >= len(sprites_animacion_puerta):
                animacion_terminada = True
                break

        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))

        # Usar el mismo sistema de profundidad visual
        objetos_animacion = [
            {'tipo': 'imagen', 'obj': imagen_estand_de_armadura_lleno_escalado, 'pos': (0, 0), 'pie_y': pie_y_pared},
            {'tipo': 'jugador', 'obj': jugador, 'pie_y': jugador.rect.bottom},
            {'tipo': 'imagen', 'obj': imagen_escalada, 'pos': (0, 0), 'pie_y': pie_y_imagen_escalada},
        ]

        objetos_animacion.sort(key=lambda item: item['pie_y'])

        if jugador.sprite_pos.y > 450:
            jugador.dibujar(pantalla, offset_x, offset_y)
            pantalla.blit(imagen_estand_de_armadura_lleno_escalado, (0, 0))
            pantalla.blit(imagen_escalada, (0, 0))

        else:
            pantalla.blit(imagen_estand_de_armadura_lleno_escalado, (0, 0))
            pantalla.blit(imagen_escalada, (0, 0))
            jugador.dibujar(pantalla, offset_x, offset_y)

        for item in objetos_animacion:
            if item['tipo'] == 'jugador':
                item['obj'].dibujar(pantalla, offset_x, offset_y)
            else:
                pantalla.blit(item['obj'], item['pos'])

        


                
        
        
        """
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)"""

        pygame.draw.rect(pantalla, (0, 0, 255), puerta_3_entrada, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_salida, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_engranaje, 2)
        pygame.draw.rect(pantalla, (255, 0, 255), puerta_3_cuatro_en_raya, 2)

       


        # 🔥 ESTA LÍNEA ES CLAVE PARA VER LA ANIMACIÓN
        pygame.display.flip()
        clock.tick(60)

    # Acá comienza el juego normal
    # Iniciar preload en background del mapa de engranajes para evitar lag al importar
    preload_started = False
    running = True
    def _start_preload():
        try:
            importlib.import_module('juego.mapa3engranajes')
            print('Preload: mapa3engranajes importado en background')
        except Exception as e:
            print(f'Preload falló: {e}')
    # Lanzar preload una vez justo antes del bucle principal
    if not preload_started:
        threading.Thread(target=_start_preload, daemon=True).start()
        preload_started = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    try:
                        state = {
                            'mapa': 'mapa4',
                            'pos_jugador': (jugador.sprite_pos.x, jugador.sprite_pos.y)
                        }
                    except Exception:
                        state = None
                    pause_menu(pantalla, mapa_actual=4, state=state)

        

        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))

        # Dibujo condicional según posición del jugador
        if jugador.sprite_pos.y + jugador.rect.height > 450:
            jugador.dibujar(pantalla, offset_x, offset_y)
            pantalla.blit(imagen_estand_de_armadura_lleno_escalado, (0, 0))
            pantalla.blit(imagen_escalada, (0, 0))

        else:
            pantalla.blit(imagen_estand_de_armadura_lleno_escalado, (0, 0))
            pantalla.blit(imagen_escalada, (0, 0))
            jugador.dibujar(pantalla, offset_x, offset_y)


        """
        # Dibujar colisiones
        for colision in colisiones_escaladas:
            pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)"""

        #Dibujar puertas (opcional para depuración)
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_3_entrada, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_salida, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_engranaje, 2)
        pygame.draw.rect(pantalla, (255, 0, 255), puerta_3_cuatro_en_raya, 2)

        jugador.manejar_teclas()

        pygame.display.flip()
        clock.tick(60)



        # Transición al siguiente mapa
        if jugador.rect.colliderect(puerta_3_salida):
            print("Transición al siguiente mapa")
            running = False
            return
            
        if jugador.rect.colliderect(puerta_3_entrada):
            print("regresa a mapa 2")
            #running = False  # Aquí puedes llamar al siguiente mapa si lo tienes
            #return 2
    
        if jugador.rect.colliderect(puerta_3_cuatro_en_raya):
            print("Transición al minijuego de 4 en raya")
            running = False
            return
            
        if jugador.rect.colliderect(puerta_3_engranaje):
            while True:
                resultado = minijuego_engranajes()
                # Restaurar resolución del juego después del minijuego
                pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
                if resultado == "completado":
                    print("✅ Mecanismo alineado, puedes continuar en mapa 3")
                    # Eliminar cualquier rect de colisión que se solape con el área del engranaje
                    antes = len(colisiones_escaladas)
                    colisiones_escaladas[:] = [r for r in colisiones_escaladas if not r.colliderect(puerta_3_engranaje)]
                    despues = len(colisiones_escaladas)
                    print(f"Colisiones removidas: {antes - despues}")
                    # Mover al jugador fuera de la zona del engranaje para evitar re-trigger inmediato
                    try:
                        # Intentar mover a la derecha del trigger
                        new_x = int(puerta_3_engranaje.right + 5)
                        max_x = ANCHO_PANTALLA - jugador.rect.width
                        if new_x <= max_x:
                            jugador.rect.x = new_x
                        else:
                            # Si no cabe a la derecha, intentar a la izquierda
                            new_x_left = int(puerta_3_engranaje.left - jugador.rect.width - 5)
                            if new_x_left >= 0:
                                jugador.rect.x = new_x_left
                            else:
                                # Si no cabe a los lados, intentar abajo
                                new_y = int(puerta_3_engranaje.bottom + 5)
                                max_y = ALTO_PANTALLA - jugador.rect.height
                                if new_y <= max_y:
                                    jugador.rect.y = new_y
                                else:
                                    # Fallback: arriba dentro de la pantalla
                                    jugador.rect.y = max(0, int(puerta_3_engranaje.top - jugador.rect.height - 5))

                        # Actualizar sprite_pos para que el dibujo no quede desincronizado
                        offset_x_j = 58
                        offset_y_j = 101
                        jugador.sprite_pos.x = jugador.rect.x - offset_x_j
                        jugador.sprite_pos.y = jugador.rect.y - offset_y_j
                    except Exception:
                        pass
                    break
                else:
                    # Mostrar un mensaje y repetir; el minijuego ya maneja reinicios
                    print("❌ Fallaste el minijuego, intenta de nuevo")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    ejecutar_mapa4(pantalla)