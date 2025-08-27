import pygame
import sys
import math

def draw_loading_spinner(surface, center, radius, frame, alpha=255):
    rotation_speed = 6
    num_dots = 8
    
    for i in range(num_dots):
        angle = math.radians((frame * rotation_speed + i * (360 / num_dots)) % 360)
        
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))
        
        dot_alpha = max(50, int(alpha * (1 - i * 0.1)))
        
        dot_size = 4 if i == 0 else max(2, 4 - i // 2)
        
        color_value = int(255 * (dot_alpha / 255))
        color = (color_value, color_value, color_value)
        
        pygame.draw.circle(surface, color, (x, y), dot_size)

def main_intro():
    pygame.init()

    # Inicializa el mixer de audio
    #pygame.mixer.init()

    try:
        # Cargar y reproducir el audio de la intro
        pygame.mixer.music.load("SONIDOS/buen-audio.mp3")  # Cambia el nombre si es necesario
        #pygame.mixer.music.set_volume(0.8)  # Opcional: ajustar volumen
        #pygame.mixer.music.play()
    except pygame.error as e:
        print(f"No se pudo reproducir el audio: {e}")

    try:
        from configuracion import ANCHO_PANTALLA, ALTO_PANTALLA
        WIDTH, HEIGHT = ANCHO_PANTALLA, ALTO_PANTALLA
    except ImportError:
        WIDTH, HEIGHT = 1280, 720
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Palermo Studios Intro")
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ACCENT_COLOR = (100, 149, 237)
    
    clock = pygame.time.Clock()
    
    try:
        big_font = pygame.font.Font(None, 150)
        small_font = pygame.font.Font(None, 70)
    except:
        big_font = pygame.font.SysFont("Arial", 150, bold=True)
        small_font = pygame.font.SysFont("Arial", 70)
    
    logo_original = pygame.image.load("intro_assets/arbol.png")
    
    max_logo_width = WIDTH // 0.8
    max_logo_height = HEIGHT // 0.8  
    
    original_width = logo_original.get_width()
    original_height = logo_original.get_height()
    
    scale_x = max_logo_width / original_width
    scale_y = max_logo_height / original_height
    scale = min(scale_x, scale_y) 
    
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    
    logo_image = pygame.transform.scale(logo_original, (new_width, new_height))
    
    studio_text = small_font.render("PALERMO STUDIOS", True, WHITE)
    
    logo_surface = logo_image.convert_alpha()
    studio_surface = studio_text.convert_alpha()
    
    logo_rect = logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))  
    studio_rect = studio_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    loading_center = (WIDTH // 2, HEIGHT // 2 + 80)
    loading_radius = 25
    
    FADE_IN_FRAMES = 30
    HOLD_FRAMES = 30
    FADE_OUT_FRAMES = 30
    STUDIO_FADE_IN_FRAMES = 30
    LOADING_FRAMES = 180
    
    logo_transition_end = FADE_IN_FRAMES + HOLD_FRAMES + FADE_OUT_FRAMES
    total_duration = logo_transition_end + STUDIO_FADE_IN_FRAMES + LOADING_FRAMES
    
    frame = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    running = False
        
        screen.fill(BLACK)
        
        if frame < logo_transition_end:
            if frame < FADE_IN_FRAMES:
                alpha = int((frame / FADE_IN_FRAMES) * 255)
            elif frame < FADE_IN_FRAMES + HOLD_FRAMES:
                alpha = 255
            else:
                fade_out_frame = frame - FADE_IN_FRAMES - HOLD_FRAMES
                alpha = max(0, int(255 * (1 - fade_out_frame / FADE_OUT_FRAMES)))
            
            logo_surface.set_alpha(alpha)
            screen.blit(logo_surface, logo_rect)
        
        elif frame < total_duration:
            studio_frame = frame - logo_transition_end
            if studio_frame < STUDIO_FADE_IN_FRAMES:
                alpha = int((studio_frame / STUDIO_FADE_IN_FRAMES) * 255)
            else:
                alpha = 255
            
            studio_surface.set_alpha(alpha)
            screen.blit(studio_surface, studio_rect)
            
            draw_loading_spinner(screen, loading_center, loading_radius, frame, alpha)
        
        pygame.display.flip()
        frame += 1
        clock.tick(60)
        
        if frame >= total_duration:
            running = False

    # Espera un momento antes de cerrar y detiene la música
    #pygame.time.wait(200)
    #pygame.mixer.music.stop()
    return

if __name__ == "__main__":
    main_intro()
