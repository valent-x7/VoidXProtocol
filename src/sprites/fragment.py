import pygame
from settings import randint

class Fragment(pygame.sprite.Sprite):
    def __init__(self, groups, image, pos, max_h, sound):
        super().__init__(groups)

        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-50, -60)
        
        self.max_h = max_h
        self.speed = randint(315, 365)
        self.angle = 0
        self.rotate_speed = randint(90, 180)
        self.sound = sound

    def update(self, delta_time):
        self.move(delta_time)
        self.rotate_image(delta_time)

    def move(self, delta_time):
        self.rect.centery += self.speed * delta_time
        self.hitbox_rect.center = self.rect.center

        self.check_position()

    def rotate_image(self, delta_time):
        self.angle += self.rotate_speed * delta_time
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_frect(center = self.rect.center)
        self.hitbox_rect.center = self.rect.center

    def check_position(self):
        if self.rect.top > self.max_h + 20: self.kill()