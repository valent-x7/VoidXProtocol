import pygame
from settings import randint

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, groups, image, pos, type, max_h):
        super().__init__(groups)

        self.type = type
        self.max_h = max_h
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-40, -40)

        self.angle = 0
        self.speed = randint(185, 225)
        self.rotation_speed = 90

    def update(self, delta_time):
        self.move(delta_time)
        self.rotate_image(delta_time)
        self.check_position()

    def move(self, delta_time):
        self.rect.centery += self.speed * delta_time
        self.hitbox_rect.center = self.rect.center

    def check_position(self):
        if self.rect.top > self.max_h + 20: self.kill()

    def rotate_image(self, delta_time):
        self.angle += self.rotation_speed * delta_time
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_frect(center = self.rect.center)
        self.hitbox_rect.center = self.rect.center