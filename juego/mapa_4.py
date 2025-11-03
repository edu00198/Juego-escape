import pygame
import sys
import os

# Inicializar Pygame y crear la ventana ANTES de importar módulos que cargan imágenes
pygame.init()
ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
from jugador_lvl2 import JugadorLvl2

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
    estandarte_de_armaduras,
    colisiones_escaladas
)

def ejecutar_mapa4(pantalla):
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
    jugador = Jugador(pos_x, pos_y, ancho_jugador, alto_jugador, escala=3, colisiones=colisiones_escaladas)

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
    
    
    ruta_estand_de_armadura_vacio = os.path.join(BASE_DIR, "assets", "mapas", "estand_de_armadura_vacio.png") 
    imagen_estand_de_armadura_vacio = pygame.image.load(ruta_estand_de_armadura_vacio).convert_alpha()
    imagen_estand_de_armadura_vacio_escalado = pygame.transform.scale(imagen_estand_de_armadura_vacio, (1280, 720))

    imagen_estand_de_armadura_actual = imagen_estand_de_armadura_lleno_escalado

    print("Tamaño original pared:", imagen_pared.get_size())
    print("Tamaño original estandarte:", imagen_estand_de_armadura_lleno.get_size())
    
    def animacion_puerta_abierta(pantalla):
        # Cargar sprites de la animación de la puerta
        sprites_animacion_puerta = [
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(1).png"),
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(2).png"),
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(3).png"),
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(4).png"),
            pygame.image.load("assets/animaciones/puerta_reja_abriendose_animacion_pared/door_reja_abriendose(5).png"),
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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    try:
                        state = {'mapa': 'mapa4'}
                    except Exception:
                        state = None
                    pause_menu(pantalla, mapa_actual=4, state=state)

            pantalla.fill((0, 0, 0))
            pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
            pantalla.blit(imagen_escalada, (0, 0))
            pantalla.blit(imagen_estand_de_armadura_actual, (0, 0))
            jugador.dibujar(pantalla, offset_x, offset_y)    # Jugador

            # Dibujar sprite actual de la puerta
            if sprite_index < len(sprites_animacion_puerta):
                imagen_puerta = sprites_animacion_puerta[sprite_index]
                pantalla.blit(imagen_puerta, (0, 0))               # Posición de la puerta

            pygame.display.update()

            # Avanzar al siguiente frame si pasó el tiempo
            if current_time - animation_timer > animation_speed:
                sprite_index += 1
                animation_timer = current_time
                if sprite_index >= len(sprites_animacion_puerta):
                    animacion_terminada = True

        # Redibujar escena final después de la animación
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_escalado, (OFFSET_X, OFFSET_Y))
        pantalla.blit(imagen_escalada, (0, 0))
        pantalla.blit(imagen_estand_de_armadura_actual, (0, 0))
        jugador.dibujar(pantalla, offset_x, offset_y)
        
        

        # Dibujar colisiones visibles (opcional)
        # for colision in colisiones_escaladas:
        #     pygame.draw.rect(pantalla, (255, 0, 0), colision, 2)

        # Dibujar zonas de interacción
        pygame.draw.rect(pantalla, (0, 0, 255), puerta_3_entrada, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_salida, 2)
        pygame.draw.rect(pantalla, (0, 255, 255), puerta_3_engranaje, 2)
        pygame.draw.rect(pantalla, (255, 0, 255), puerta_3_cuatro_en_raya, 2)

        # Actualizar pantalla final
        pygame.display.flip()
        clock.tick(60)

    #hace a animacion
    animacion_puerta_abierta(pantalla)
    # Acá comienza el juego normal
    running = True
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

        """
        #depuracion de alturas
        print("Posición Y del jugador:", jugador.sprite_pos.y)
        print("Altura del jugador:", jugador.rect.height)
        print("Suma:", jugador.sprite_pos.y + jugador.rect.height)"""

        # Dibujo condicional según posición del jugador
        if float(jugador.sprite_pos.y + jugador.rect.height) < 310.0:  
            jugador.dibujar(pantalla, offset_x, offset_y)
            pantalla.blit(imagen_escalada, (0, 0))
            pantalla.blit(imagen_estand_de_armadura_actual, (0, 0))

        else:
            pantalla.blit(imagen_escalada, (0, 0))
            pantalla.blit(imagen_estand_de_armadura_actual, (0, 0))
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
        pygame.draw.rect(pantalla, (255, 255, 0), estandarte_de_armaduras, 2)  

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
            continue
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and jugador.rect.colliderect(estandarte_de_armaduras):
                    print("¡Interacción con el estandarte activada! Subiendo a nivel 2...")

                    # Cambiar imagen del estandarte
                    imagen_estand_de_armadura_actual = imagen_estand_de_armadura_vacio_escalado

                    # Guardar posición actual
                    pos_x = jugador.sprite_pos.x
                    pos_y = jugador.sprite_pos.y

                    # Crear nuevo jugador de nivel 2 en la misma posición
                    jugador = JugadorLvl2(
                        x=pos_x,
                        y=pos_y,
                        ancho=jugador.rect.width,
                        alto=jugador.rect.height,
                        escala=jugador.escala,
                        colisiones=jugador.colisiones
            )

            
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    ejecutar_mapa4(pantalla)