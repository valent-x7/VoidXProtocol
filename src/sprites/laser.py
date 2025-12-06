import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, frames, sound, pos):
        super().__init__(groups)

        self.frames = frames
        self.frame = 0
        self.image = self.frames[self.frame]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-65, -25)

        self.animation_speed = 15
        self.speed = -625
        sound.play() # -> PyGame Sound

    def update(self, delta_time):
        self.animate(delta_time)
        self.move(delta_time)

    def animate(self, delta_time):
        self.frame += self.animation_speed * delta_time
        self.image = self.frames[int(self.frame) % len(self.frames)]

    def move(self, delta_time):
        self.rect.centery += self.speed * delta_time
        self.hitbox_rect.center = self.rect.center

        self.check_pos()
    
    def check_pos(self):
        if self.rect.bottom < -20: self.kill()

    @classmethod
    def launch(cls, meteors_group, frames, sound, player):
        pos = (player.rect.centerx, player.rect.top)
        return cls(meteors_group, frames, sound, pos)