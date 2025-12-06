import pygame
from ui.utils import draw_text

class ButtonUI:
    def __init__(self, screen, position, color, hover_color, font, text, width, height, sound):
        self.screen = screen
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.sound = sound

        self.rect = pygame.FRect(0, 0, width, height)
        self.rect.center = position

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        # ? Dibujar rect
        pygame.draw.rect(self.screen, self.color, self.rect, 0, 12)

        # Si hay hover, dibuja el botón con el color del hover
        if self.rect.collidepoint(mouse_pos):
            # Botón hover encima
            pygame.draw.rect(self.screen, self.hover_color, self.rect, 0, 12)

        draw_text(self.screen, self.font, self.text, "white", self.rect.centerx, self.rect.centery)

    # Detectar clic
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.sound.play()
                return True
        return False