import pygame
import os

class Button:
    def __init__(self, image_path, pos, scale=1.0, text=None, font=None,
                 text_color=(255, 255, 255)):
        """
        Botón con imagen o fallback + animación de selección por teclado.
        """
        self.text = text
        self.text_color = text_color
        self.font = font
        self.pos = pos

        # Imagen base o fallback
        if image_path and os.path.exists(image_path):
            img = pygame.image.load(image_path).convert_alpha()
        else:
            img = pygame.Surface((200, 70), pygame.SRCALPHA)
            img.fill((30, 30, 30, 220))

        # Guardamos la imagen original
        self.original_image = img
        self.base_scale = scale
        self.hover_scale = scale * 1.2  # cuanto se agranda al seleccionarse

        # Escala actual (empieza en base)
        self.current_scale = self.base_scale
        self.scale_speed = 0.2  # suavidad de la transición

        self.current_image = self.get_scaled_image(self.current_scale)
        self.rect = self.current_image.get_rect(center=self.pos)

        # Estado de selección (se lo maneja desde el menú con flechas)
        self.selected = False

    def get_scaled_image(self, scale):
        """Devuelve la imagen escalada según el factor dado."""
        w, h = self.original_image.get_size()
        new_size = (int(w * scale), int(h * scale))
        return pygame.transform.smoothscale(self.original_image, new_size)

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)

        if self.text:
            if self.font is None:
                self.font = pygame.font.SysFont("Arial", 20, bold=True)
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def update(self):
        """Interpola suavemente la escala hacia el tamaño objetivo."""
        # Si el botón está seleccionado -> usar hover_scale
        if getattr(self, "selected", False):
            target_scale = self.hover_scale
        else:
            target_scale = self.base_scale

        # interpolación lineal hacia el target
        self.current_scale += (target_scale - self.current_scale) * self.scale_speed

        # actualizar imagen y rect
        self.current_image = self.get_scaled_image(self.current_scale)
        self.rect = self.current_image.get_rect(center=self.pos)    
