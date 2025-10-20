import pygame
from assets.mapas.fondo import key, cofre_a, cofre_c, nota

# Flag persistente para indicar si el código ya fue ingresado correctamente
# Esto es leído por `mapa_1` para mantener el estado entre mapas.
codigo_ya_ingresado = False

# Cargar sprites del cofre en una lista
sprites = [
    pygame.image.load(f"assets/animaciones/chest_animation/animacion cofre ({i}).png") for i in range(1, 6)
]

# Colores
DORADO = (255, 215, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
MARRON = (139, 69, 19)
ROJO = (200, 0, 0)
VERDE = (0, 200, 0)

class Llave:
    def __init__(self, x, y):
        self.encontrada = False
        try:
            self.imagen = pygame.image.load(key).convert_alpha()
            self.imagen = pygame.transform.scale(self.imagen, (35, 35))
        except Exception as e:
            print(f"No se pudo cargar la imagen de la llave desde '{key}': {e}")
            self.imagen = None

        if self.imagen:
            self.rect = self.imagen.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = pygame.Rect(x, y, 25, 25)

    def recoger(self):
        self.encontrada = True

    def dibujar(self, pantalla):
        if not self.encontrada:
            if self.imagen:
                pantalla.blit(self.imagen, self.rect)
            else:
                pygame.draw.rect(pantalla, DORADO, self.rect)
                pygame.draw.rect(pantalla, NEGRO, self.rect, 2)
                pygame.draw.circle(pantalla, DORADO, (self.rect.x + 8, self.rect.y + 12), 6)
                pygame.draw.circle(pantalla, NEGRO, (self.rect.x + 8, self.rect.y + 12), 6, 2)


class Cofre:
    def __init__(self, x, y):
        self.abierto = False
        try:
            self.imagen_cerrado = pygame.image.load(cofre_c).convert_alpha()
            self.imagen_cerrado = pygame.transform.scale(self.imagen_cerrado, (80, 75))
            self.imagen_abierto = pygame.image.load(cofre_a).convert_alpha()
            self.imagen_abierto = pygame.transform.scale(self.imagen_abierto, (90, 85))
        except Exception as e:
            print(f"No se pudieron cargar las imágenes del cofre: {e}")
            self.imagen_cerrado = None
            self.imagen_abierto = None

        if self.imagen_cerrado:
            self.rect = self.imagen_cerrado.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = pygame.Rect(x, y, 80, 75)

    def abrir(self):
        self.abierto = True

    def dibujar(self, pantalla):
        if self.imagen_cerrado and self.imagen_abierto:
            if self.abierto:
                pantalla.blit(self.imagen_abierto, self.rect)
            else:
                pantalla.blit(self.imagen_cerrado, self.rect)
        else:
            if self.abierto:
                pygame.draw.rect(pantalla, (160, 82, 45), self.rect)
                pygame.draw.rect(pantalla, NEGRO, self.rect, 2)
                pygame.draw.rect(pantalla, MARRON, (self.rect.x, self.rect.y - 8, self.rect.width, 8))
                pygame.draw.rect(pantalla, NEGRO, (self.rect.x, self.rect.y - 8, self.rect.width, 8), 2)
            else:
                pygame.draw.rect(pantalla, MARRON, self.rect)
                pygame.draw.rect(pantalla, NEGRO, self.rect, 2)
                pygame.draw.circle(pantalla, DORADO, (self.rect.centerx, self.rect.centery), 5)
                pygame.draw.circle(pantalla, NEGRO, (self.rect.centerx, self.rect.centery), 5, 2)


class CartaCodigo:
    def __init__(self, codigo_secreto, texto):
        self.encontrada = False
        self.codigo_secreto = codigo_secreto
        self.texto = texto
        self.visible = False
        try:
            self.imagen_carta = pygame.image.load(nota).convert_alpha()
            self.imagen_carta = pygame.transform.scale(self.imagen_carta, (450, 350))
        except Exception as e:
            print(f"No se pudo usar la imagen de la carta: {e}")
            self.imagen_carta = None

        pantalla = pygame.display.get_surface()
        self.rect = self.imagen_carta.get_rect(center=(pantalla.get_width() // 2,
                                                       pantalla.get_height() // 2))
        self.fuente_titulo = pygame.font.Font(None, 40)
        self.fuente_codigo = pygame.font.Font(None, 48)
        self.fuente_texto = pygame.font.Font(None, 24)
        self.fuente_instruccion = pygame.font.Font(None, 22)

    def mostrar(self):
        self.visible = True

    def ocultar(self):
        self.visible = False

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            # Allow closing the card with SPACE or ESCAPE
            if self.visible and evento.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                self.ocultar()
                return True
        return False

    def dibujar(self, pantalla, texto):
        if not self.visible:
            return

        ancho_pantalla, alto_pantalla = pantalla.get_size()
        overlay = pygame.Surface((ancho_pantalla, alto_pantalla))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0, 0))

        if self.imagen_carta:
            pantalla.blit(self.imagen_carta, self.rect.topleft)

        y_offset = 110
        texto = self.fuente_texto.render(self.texto, True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(self.rect.centerx, self.rect.y + y_offset))
        pantalla.blit(texto, texto_rect)
        y_offset += 28

        y_offset += 20
        codigo_fondo = pygame.Rect(self.rect.centerx - 80, self.rect.y + y_offset - 10, 160, 50)
        pygame.draw.rect(pantalla, (212, 175, 55), codigo_fondo)
        pygame.draw.rect(pantalla, (0, 0, 0), codigo_fondo, 3)

        codigo_texto = self.fuente_codigo.render(self.codigo_secreto, True, (0, 0, 0))
        codigo_rect = codigo_texto.get_rect(center=codigo_fondo.center)
        pantalla.blit(codigo_texto, codigo_rect)

        y_offset += 80
        mensaje_final = [
            "Memoriza este código y acércate a la puerta.",
            "Presiona ENTER cerca de la puerta para ingresar el código."
        ]
        for linea in mensaje_final:
            texto = self.fuente_instruccion.render(linea, True, (0, 0, 0))
            texto_rect = texto.get_rect(center=(self.rect.centerx, self.rect.y + y_offset))
            pantalla.blit(texto, texto_rect)
            y_offset += 25

        cerrar_texto = self.fuente_texto.render("Presiona ESPACIO para salir", True, (255, 0, 0))
        cerrar_rect = cerrar_texto.get_rect(center=(self.rect.centerx, self.rect.bottom - 30))
        pantalla.blit(cerrar_texto, cerrar_rect)


class PanelCodigo:
    def __init__(self, codigo_correcto, ancho_pantalla=800, alto_pantalla=600):
        self.codigo_correcto = codigo_correcto
        self.codigo_ingresado = ""
        self.visible = False
        self.codigo_correcto_ingresado = False
        self.mensaje_error = ""
        self.tiempo_mensaje = 0

        self.rect = pygame.Rect((ancho_pantalla - 400) // 2, (alto_pantalla - 300) // 2, 400, 300)
        self.fuente_titulo = pygame.font.Font(None, 36)
        self.fuente_codigo = pygame.font.Font(None, 48)
        self.fuente_texto = pygame.font.Font(None, 28)
        self.fuente_instruccion = pygame.font.Font(None, 24)

    def mostrar(self):
        self.visible = True
        self.codigo_ingresado = ""
        self.mensaje_error = ""
        self.codigo_correcto_ingresado = False

    def ocultar(self):
        self.visible = False

    def manejar_evento(self, evento):
        if not self.visible:
            return False

        if evento.type == pygame.KEYDOWN:
            # Allow closing the panel with SPACE or ESC
            if evento.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                self.ocultar()
                return True
            elif evento.key == pygame.K_BACKSPACE:
                self.codigo_ingresado = self.codigo_ingresado[:-1]
                self.mensaje_error = ""
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.codigo_ingresado == self.codigo_correcto:
                    self.codigo_correcto_ingresado = True
                    self.mensaje_error = "¡CÓDIGO CORRECTO!"
                    self.tiempo_mensaje = pygame.time.get_ticks()
                    return "codigo_correcto"
                else:
                    self.mensaje_error = "Código incorrecto. Intenta de nuevo."
                    self.codigo_ingresado = ""
                    self.tiempo_mensaje = pygame.time.get_ticks()
            elif len(self.codigo_ingresado) < 4 and evento.unicode.isdigit():
                self.codigo_ingresado += evento.unicode
                self.mensaje_error = ""

        return False

    def actualizar(self):
        if self.tiempo_mensaje > 0 and pygame.time.get_ticks() - self.tiempo_mensaje > 2000:
            if not self.codigo_correcto_ingresado:
                self.mensaje_error = ""
            self.tiempo_mensaje = 0

    def dibujar(self, pantalla):
        if self.visible:
            ancho_pantalla, alto_pantalla = pantalla.get_size()

            overlay = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
            for i in range(200):
                alpha = max(0, 128 - i)
                pygame.draw.circle(overlay, (0, 0, 0, alpha), (ancho_pantalla//2, alto_pantalla//2), i*3)
            pantalla.blit(overlay, (0, 0))

            rect_bg = pygame.Rect(self.rect)
            border_radius = 20
            pygame.draw.rect(pantalla, (240, 240, 240), rect_bg, border_radius=border_radius)
            pygame.draw.rect(pantalla, (50, 50, 50), rect_bg, 4, border_radius=border_radius)

            titulo_sombra = self.fuente_titulo.render("INGRESA EL CÓDIGO", True, (100, 100, 100))
            titulo = self.fuente_titulo.render("INGRESA EL CÓDIGO", True, (0, 0, 0))
            titulo_rect = titulo.get_rect(center=(self.rect.centerx, self.rect.y + 40))
            pantalla.blit(titulo_sombra, titulo_rect.move(2, 2))
            pantalla.blit(titulo, titulo_rect)

            codigo_rect = pygame.Rect(self.rect.centerx - 80, self.rect.centery - 25, 160, 50)
            pygame.draw.rect(pantalla, (255, 255, 255), codigo_rect, border_radius=10)
            pygame.draw.rect(pantalla, (0, 0, 0), codigo_rect, 3, border_radius=10)

            codigo_display = " ".join(self.codigo_ingresado + "_" * (4 - len(self.codigo_ingresado)))
            codigo_texto = self.fuente_codigo.render(codigo_display, True, (0, 0, 0))
            codigo_texto_rect = codigo_texto.get_rect(center=codigo_rect.center)
            pantalla.blit(codigo_texto, codigo_texto_rect)

            if self.mensaje_error:
                color = (0, 200, 0) if self.codigo_correcto_ingresado else (200, 0, 0)
                error_bg_rect = pygame.Rect(self.rect.centerx - 150, self.rect.centery + 40, 300, 40)
                pygame.draw.rect(pantalla, (255, 255, 255), error_bg_rect, border_radius=10)
                pygame.draw.rect(pantalla, color, error_bg_rect, 2, border_radius=10)
                error_texto = self.fuente_texto.render(self.mensaje_error, True, color)
                error_rect = error_texto.get_rect(center=error_bg_rect.center)
                pantalla.blit(error_texto, error_rect)

            if not self.codigo_correcto_ingresado:
                instrucciones = [
                    "Ingresa el código de 4 dígitos",
                    "ENTER: Confirmar | ESC: Cancelar"
                ]
                y_offset = self.rect.centery + 100
                for instruccion in instrucciones:
                    inst_texto = self.fuente_texto.render(instruccion, True, (0, 0, 0))
                    inst_rect = inst_texto.get_rect(center=(self.rect.centerx, y_offset))
                    pantalla.blit(inst_texto, inst_rect)
                    y_offset += 35


class SistemaLlavesCofres:
    def __init__(self, codigo_secreto):
        self.llaves = []
        self.cofres = []
        self.cartas = []
        self.panel_codigo = None
        self.llaves_encontradas = 0
        self.codigo_secreto = codigo_secreto
        self.codigo_correcto = False

    def agregar_llave(self, x, y, sprite_path=None):
        llave = Llave(x, y)
        self.llaves.append(llave)
        return llave

    def agregar_cofre(self, x, y, sprite_cerrado_path=None, sprite_abierto_path=None, sprite_carta_path=None):
        cofre = Cofre(x, y)
        self.cofres.append(cofre)

    def agregar_carta(self, texto):
        carta = CartaCodigo(self.codigo_secreto, texto)
        self.cartas.append(carta)
        return carta

    def dibujar(self, pantalla):
        for llave in self.llaves:
            llave.dibujar(pantalla)
        for cofre in self.cofres:
            cofre.dibujar(pantalla)
        for carta in self.cartas:
            carta.dibujar(pantalla, carta.texto)
        if self.panel_codigo:
            self.panel_codigo.dibujar(pantalla)

    def crear_panel_codigo(self, ancho_pantalla=800, alto_pantalla=600):
        self.panel_codigo = PanelCodigo(self.codigo_secreto, ancho_pantalla, alto_pantalla)

    def cerrar_panel_codigo(self):
        """Oculta y resetea el panel de código (para cuando se vuelve a mapa1)."""
        if self.panel_codigo:
            self.panel_codigo.visible = False
            self.panel_codigo.codigo_ingresado = ""
            self.panel_codigo.mensaje_error = ""
            self.panel_codigo.codigo_correcto_ingresado = False

    def verificar_colisiones(self, jugador_rect):
        for llave in self.llaves:
            if not llave.encontrada and jugador_rect.colliderect(llave.rect):
                llave.recoger()
                self.llaves_encontradas += 1
                return "llave"
        if self.llaves_encontradas > 0:
            for i, cofre in enumerate(self.cofres):
                if not cofre.abierto and jugador_rect.colliderect(cofre.rect):
                    cofre.abrir()
                    # Reproducir animación de apertura de cofre si existen 'screen' y 'sprites'.
                    try:
                        screen = pygame.display.get_surface()
                        import importlib, sys
                        # Preferir la lista local 'sprites' si existe en este módulo
                        sprites_to_play = globals().get('sprites', None)
                        # Si no hay sprites locales, intentar obtenerlos desde juego.mapa_1
                        if not sprites_to_play:
                            try:
                                if 'juego.mapa_1' in sys.modules:
                                    mod = sys.modules['juego.mapa_1']
                                else:
                                    mod = importlib.import_module('juego.mapa_1')
                                sprites_to_play = getattr(mod, 'sprites', None)
                            except Exception:
                                sprites_to_play = None

                        if sprites_to_play and screen:
                            # Preparar snapshot del fondo bajo la animación para restaurarlo
                            print("---------------------------codigo_secreto: [", self.codigo_secreto, "]---------------------------------------")
                            try:
                                # Usar primer frame sin escalar para calcular el rect de animación
                                sample = sprites_to_play[0]
                                anim_rect = sample.get_rect(center=cofre.rect.center)
                                # Asegurar que anim_rect esté dentro de la pantalla
                                anim_rect.clamp_ip(screen.get_rect())
                                background_snapshot = screen.subsurface(anim_rect).copy()
                            except Exception:
                                anim_rect = None
                                background_snapshot = None

                            for frame in sprites_to_play:
                                # Mantener la cola de eventos para que la ventana no se congele
                                pygame.event.pump()
                                try:
                                    # Escalar el frame al doble de tamaño (scale2x preserva calidad)
                                    try:
                                        frame_s = pygame.transform.scale(frame, (frame.get_width() * 3, frame.get_height() * 3))


                                    except Exception:
                                        # Fallback: escalar manualmente si scale2x falla
                                        frame_s = pygame.transform.scale(frame, (frame.get_width()*5, frame.get_height()*2))

                                    # Calcular rect centrado en el cofre
                                    frame_rect = frame_s.get_rect(center=(cofre.rect.centerx, cofre.rect.centery + 8))


                                    # Restaurar fondo en la zona de la animación para evitar manchas
                                    if background_snapshot and anim_rect:
                                        screen.blit(background_snapshot, anim_rect.topleft)

                                    # Dibujar frame sobre el fondo
                                    screen.blit(frame_s, frame_rect.topleft)

                                    # Actualizar sólo el área afectada
                                    try:
                                        pygame.display.update(frame_rect)
                                    except Exception:
                                        pygame.display.flip()

                                    # Esperar más tiempo (doble lento): 300 ms
                                    pygame.time.delay(300)
                                except Exception:
                                    # Si algo falla con este frame, continuar con el siguiente
                                    continue
                        else:
                            # No hay sprites disponibles: debug
                            #print("No se encontraron sprites para la animación del cofre.")
                            pass
                    except Exception as e:
                        print(f"Animación del cofre falló: {e}")
                    if i < len(self.cartas):
                        self.cartas[i].mostrar()
                    self.llaves_encontradas -= 1
                    return "cofre"
        return None

    def mostrar_panel_codigo(self, x=None, y=None):
        if self.panel_codigo:
            self.panel_codigo.mostrar()
            if x is not None and y is not None:
                self.panel_codigo.rect.center = (x, y)

    def manejar_eventos(self, evento):
        # If ESC was pressed, close any visible UI (cards or panel)
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            any_closed = False
            for carta in self.cartas:
                if carta.visible:
                    carta.ocultar()
                    any_closed = True
            if self.panel_codigo and self.panel_codigo.visible:
                self.panel_codigo.ocultar()
                any_closed = True
            if any_closed:
                return True

        for carta in self.cartas:
            if carta.manejar_evento(evento):
                return True
        if self.panel_codigo:
            resultado = self.panel_codigo.manejar_evento(evento)
            if resultado == "codigo_correcto":
                self.codigo_correcto = True
                global codigo_ya_ingresado
                codigo_ya_ingresado = True
                return "codigo_correcto"
        return False

    def actualizar(self):
        if self.panel_codigo:
            self.panel_codigo.actualizar()

    def hay_interfaz_visible(self):
        interfaz_visible = any(carta.visible for carta in self.cartas)
        if self.panel_codigo:
            interfaz_visible = interfaz_visible or self.panel_codigo.visible
        return interfaz_visible
