import pygame
from settings import randint

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, laser_group, frames, sound, pos, max_h):
        super().__init__(groups)
        self.laser_group = laser_group
        self.frames = frames
        self.frame = 0
        self.explosion_sound = sound
        self.max_h = max_h
        self.image = self.frames[self.frame]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-35, -40)

        self.animation_speed = randint(10, 14)
        self.speed = randint(375, 455)

    def update(self, delta_time):
        self.animate(delta_time)
        self.move(delta_time)

    def animate(self, delta_time):
        self.frame += self.animation_speed * delta_time
        self.image = self.frames[int(self.frame) % len(self.frames)]
        self.check_laser_collision(self.laser_group)

    def move(self, delta_time):
        self.rect.centery += self.speed * delta_time
        self.hitbox_rect.center = self.rect.center

        self.check_position()

    def check_position(self):
        if self.rect.top > self.max_h + 20: self.kill()

    def check_laser_collision(self, laser_group):
        for laser in laser_group:
            if self.hitbox_rect.colliderect(laser.hitbox_rect):
                laser.kill()
                self.explosion_sound.play()
                self.kill()
                break