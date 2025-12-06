import pygame
from random import randint, choice

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, image, screen_w, screen_h):
        super().__init__(groups)

        self.image = image
        self.rect = self.image.get_frect()
        self.rect.x = randint(0, int(screen_w - self.rect.width))
        self.rect.y = randint(0, int(screen_h - self.rect.height))

        self.speed_x = choice([-3, -2, -1, 1, 2, 3])
        self.speed_y = choice([-3, -2, -1, 1, 2, 3])
        self.width_limit = screen_w
        self.height_limit = screen_h

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.right >= self.width_limit or self.rect.left <= 0:
            self.speed_x *= -1 # -> Invierte dirección X
            
        if self.rect.bottom >= self.height_limit or self.rect.top <= 0:
            self.speed_y *= -1 # -> Invierte dirección Y