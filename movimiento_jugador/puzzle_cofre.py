import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Llaves, Cofres y Cartas")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 100, 200)
VERDE = (0, 200, 0)
ROJO = (200, 0, 0)
DORADO = (255, 215, 0)
MARRON = (139, 69, 19)
GRIS = (128, 128, 128)
AMARILLO = (255, 255, 0)

# Fuentes
fuente_titulo = pygame.font.Font(None, 36)
fuente_texto = pygame.font.Font(None, 24)
fuente_carta = pygame.font.Font(None, 20)

class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocidad = 5
        self.tiene_llave = False
    
    def mover(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT] and self.rect.x < ANCHO - self.rect.width:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN] and self.rect.y < ALTO - self.rect.height:
            self.rect.y += self.velocidad
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, AZUL, self.rect)
        # Dibujar ojos
        pygame.draw.circle(pantalla, BLANCO, (self.rect.x + 8, self.rect.y + 8), 3)
        pygame.draw.circle(pantalla, BLANCO, (self.rect.x + 22, self.rect.y + 8), 3)
        pygame.draw.circle(pantalla, NEGRO, (self.rect.x + 8, self.rect.y + 8), 1)
        pygame.draw.circle(pantalla, NEGRO, (self.rect.x + 22, self.rect.y + 8), 1)

class Llave:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.encontrada = False
    
    def dibujar(self, pantalla):
        if not self.encontrada:
            # Dibujar llave dorada
            pygame.draw.rect(pantalla, DORADO, self.rect)
            pygame.draw.rect(pantalla, NEGRO, self.rect, 2)
            # Detalles de la llave
            pygame.draw.circle(pantalla, DORADO, (self.rect.x + 5, self.rect.y + 10), 8)
            pygame.draw.circle(pantalla, NEGRO, (self.rect.x + 5, self.rect.y + 10), 8, 2)

class Cofre:
    def __init__(self, x, y, mensaje):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.abierto = False
        self.mensaje = mensaje
    
    def abrir(self):
        self.abierto = True
    
    def dibujar(self, pantalla):
        if self.abierto:
            # Cofre abierto (marrón claro)
            pygame.draw.rect(pantalla, (160, 82, 45), self.rect)
            pygame.draw.rect(pantalla, NEGRO, self.rect, 2)
            # Tapa abierta
            pygame.draw.rect(pantalla, MARRON, (self.rect.x, self.rect.y - 10, self.rect.width, 10))
            pygame.draw.rect(pantalla, NEGRO, (self.rect.x, self.rect.y - 10, self.rect.width, 10), 2)
        else:
            # Cofre cerrado
            pygame.draw.rect(pantalla, MARRON, self.rect)
            pygame.draw.rect(pantalla, NEGRO, self.rect, 2)
            # Cerradura
            pygame.draw.circle(pantalla, DORADO, (self.rect.centerx, self.rect.centery), 5)
            pygame.draw.circle(pantalla, NEGRO, (self.rect.centerx, self.rect.centery), 5, 2)

class Carta:
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.visible = False
        self.rect = pygame.Rect(ANCHO//2 - 200, ALTO//2 - 150, 400, 300)
    
    def mostrar(self):
        self.visible = True
    
    def ocultar(self):
        self.visible = False
    
    def dibujar(self, pantalla):
        if self.visible:
            # Fondo semi-transparente
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(128)
            overlay.fill(NEGRO)
            pantalla.blit(overlay, (0, 0))
            
            # Carta
            pygame.draw.rect(pantalla, BLANCO, self.rect)
            pygame.draw.rect(pantalla, NEGRO, self.rect, 3)
            
            # Título
            titulo = fuente_titulo.render("¡Misión Encontrada!", True, NEGRO)
            titulo_rect = titulo.get_rect(center=(self.rect.centerx, self.rect.y + 40))
            pantalla.blit(titulo, titulo_rect)
            
            # Mensaje - dividir en líneas
            lineas = self.mensaje.split('\n')
            y_offset = 80
            for linea in lineas:
                if linea.strip():  # Solo dibujar líneas no vacías
                    texto = fuente_carta.render(linea, True, NEGRO)
                    texto_rect = texto.get_rect(center=(self.rect.centerx, self.rect.y + y_offset))
                    pantalla.blit(texto, texto_rect)
                y_offset += 25
            
            # Instrucción para cerrar
            cerrar_texto = fuente_texto.render("Presiona ESPACIO para continuar", True, ROJO)
            cerrar_rect = cerrar_texto.get_rect(center=(self.rect.centerx, self.rect.bottom - 30))
            pantalla.blit(cerrar_texto, cerrar_rect)

class Juego:
    def __init__(self):
        self.jugador = Jugador(50, 50)
        self.llave = Llave(300, 200)
        
        # Mensaje de la carta
        mensaje_mision = """Tu próxima misión es:

Encuentra las 3 gemas perdidas del reino.
Están escondidas en lugares peligrosos:
- La gema roja en el volcán ardiente
- La gema azul en las profundidades del océano  
- La gema verde en el bosque encantado

¡Ten cuidado con los guardianes!
El destino del reino está en tus manos."""
        
        self.cofre = Cofre(500, 300, mensaje_mision)
        self.carta = Carta(mensaje_mision)
        self.juego_terminado = False
    
    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and self.carta.visible:
                self.carta.ocultar()
    
    def actualizar(self):
        keys = pygame.key.get_pressed()
        self.jugador.mover(keys)
        
        # Verificar colisión con llave
        if not self.llave.encontrada and self.jugador.rect.colliderect(self.llave.rect):
            self.llave.encontrada = True
            self.jugador.tiene_llave = True
        
        # Verificar colisión con cofre
        if (self.jugador.tiene_llave and not self.cofre.abierto and 
            self.jugador.rect.colliderect(self.cofre.rect)):
            self.cofre.abrir()
            self.carta.mostrar()
    
    def dibujar(self, pantalla):
        pantalla.fill(BLANCO)
        
        # Dibujar elementos del juego
        self.jugador.dibujar(pantalla)
        self.llave.dibujar(pantalla)
        self.cofre.dibujar(pantalla)
        
        # Dibujar interfaz
        if self.jugador.tiene_llave:
            llave_texto = fuente_texto.render("¡Tienes una llave!", True, DORADO)
            pantalla.blit(llave_texto, (10, 10))
        
        if self.cofre.abierto:
            cofre_texto = fuente_texto.render("¡Cofre abierto! Misión recibida.", True, VERDE)
            pantalla.blit(cofre_texto, (10, 40))
        
        # Instrucciones
        if not self.jugador.tiene_llave:
            instruccion = fuente_texto.render("Usa las flechas para moverte. Encuentra la llave.", True, NEGRO)
            pantalla.blit(instruccion, (10, ALTO - 60))
        elif not self.cofre.abierto:
            instruccion = fuente_texto.render("¡Ve al cofre para abrirlo con tu llave!", True, NEGRO)
            pantalla.blit(instruccion, (10, ALTO - 60))
        else:
            instruccion = fuente_texto.render("¡Misión completada! El cofre ha sido abierto.", True, NEGRO)
            pantalla.blit(instruccion, (10, ALTO - 60))
        
        # Dibujar carta (siempre al final para que esté encima)
        self.carta.dibujar(pantalla)

# Función principal
def main():
    reloj = pygame.time.Clock()
    juego = Juego()
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            juego.manejar_eventos(evento)
        
        juego.actualizar()
        juego.dibujar(pantalla)
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()
    sys.exit()

