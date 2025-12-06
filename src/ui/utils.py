import pygame

def draw_text(screen: pygame.Surface, font: pygame.Font, text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_frect(center = (x, y))
    screen.blit(text_surface, text_rect)