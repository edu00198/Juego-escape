import pygame
import sys
from configuracion import ALTO_PANTALLA, ANCHO_PANTALLA

if __name__ == '__main__':
    try:
        pygame.init()
    except Exception as e:
        print(f"Error inicializando pygame: {e}")
        raise

    try:
        # Algunos módulos de mapas llaman a convert_alpha() al importarlos,
        # lo que requiere que exista un modo de video. Crear una ventana
        # temporal antes de importar evita el error "No video mode has been set".
        try:
            pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        except Exception:
            # Si por alguna razón no se puede crear la ventana, seguir e intentar importar
            pass

        from juego.mapa_3_2 import ejecutar_mapa4
        ejecutar_mapa4(pantalla)
    except Exception as e:
        print(f"Error ejecutando mapa_5: {e}")
        import traceback
        traceback.print_exc()
        sys.exit()