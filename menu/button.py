import pygame
import os

class Button:
    def __init__(self, image_path, pos, scale=1.0, text=None, font=None,
                 text_color=(255, 255, 255), hover_effect=True):
        """
        Botón con imagen o fallback + efecto hover animado opcional.
        """
        self.text = text
        self.text_color = text_color
        self.font = font
        self.pos = pos
        self.hover_effect = hover_effect   # <<--- agregado

        # Imagen base o fallback
        if image_path and os.path.exists(image_path):
            img = pygame.image.load(image_path).convert_alpha()
        else:
            img = pygame.Surface((200, 70), pygame.SRCALPHA)
            img.fill((30, 30, 30, 220))
            pygame.draw.rect(img, (200, 200, 200), img.get_rect(), 3)

        # Guardamos la imagen original
        self.original_image = img
        self.base_scale = scale
        self.hover_scale = scale * 1.2 if hover_effect else scale  # <<--- hover desactivado si es False

        # Escala actual (empieza en base)
        self.current_scale = self.base_scale
        self.scale_speed = 0.1  # cuanto más alto, más rápido cambia

        self.current_image = self.get_scaled_image(self.current_scale)
        self.rect = self.current_image.get_rect(center=self.pos)

    def get_scaled_image(self, scale):
        """Devuelve la imagen escalada según el factor dado."""
        w, h = self.original_image.get_size()
        new_size = (int(w * scale), int(h * scale))
        return pygame.transform.smoothscale(self.original_image, new_size)

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)

        if self.text:
            if self.font is None:
                self.font = pygame.font.SysFont("Arial", 28, bold=True)
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def update(self):
        """Interpola suavemente la escala hacia el tamaño objetivo."""
        target_scale = self.hover_scale if (self.hover_effect and self.is_hover()) else self.base_scale

        # interpolación lineal hacia el target
        self.current_scale += (target_scale - self.current_scale) * self.scale_speed

        # actualizar imagen y rect
        self.current_image = self.get_scaled_image(self.current_scale)
        self.rect = self.current_image.get_rect(center=self.pos)

    def is_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.rect.collidepoint(e.pos):
                    return True
        return False

