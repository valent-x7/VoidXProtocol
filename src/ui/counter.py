import pygame
from ui.utils import draw_text

class TimeCounter:
    def __init__(self, x, y, width, height, font, color = "white"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.time = 0
        self.font = font

    def update(self, delta_time):
        self.time += delta_time

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2, 12)
        draw_text(screen, self.font, f"{int(self.time)}", "white", self.rect.centerx, self.rect.centery)