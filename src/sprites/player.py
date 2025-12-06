import pygame
from sprites.laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, fragment_group, powerup_group, powerup_sound, meteor_group, laser_group, laser_frames, laser_sound, frames, pos, hit_sound):
        super().__init__(groups)

        # ? --- Laser Items ---
        self.laser_group = laser_group
        self.laser_frames = laser_frames
        self.laser_sound = laser_sound

        # ? --- Meteor Group Reference ---
        self.meteor_group = meteor_group

        # ? --- PowerUp Group Reference ---
        self.powerup_group = powerup_group
        self.powerup_sound = powerup_sound

        # ? --- Fragment Group Reference
        self.fragment_group = fragment_group

        self.frames = frames
        self.frame = 0

        self.image = self.frames[self.frame]
        self.rect = self.image.get_frect(center = (pos))
        self.hitbox_rect = self.rect.inflate(-40, -35)

        self.invincible = False
        self.invincible_time = 1000
        self.invincible_start = 0
        self.blink = False
        self.blink_speed = 100
        self.last_time_blink = 0

        self.powerup_cooldown = 10000 # -> 10 segundos
        self.is_powerup_effect = False
        self.powerup_effect_start = 0

        self.hit_sound = hit_sound
        self.vector_move = pygame.Vector2()
        self.shoot_cooldown = 500
        self.last_shoot_time = 0
        self.speed = 525
        self.speed_animation = 12
        self.health = 3
        self.fragments = 0

    def update(self, delta_time):
        self.handle_input()
        self.move(delta_time)
        self.animate(delta_time)
        self.check_meteor_collision()
        self.check_powerup_collision()
        self.check_fragment_collision()
        self.Update_PowerUp_Effect()
        self.update_invincibility()

    def animate(self, delta_time):
        self.frame += self.speed_animation * delta_time
        self.image = self.frames[int(self.frame) % len(self.frames)]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vector_move.update(0, 0)

        if keys[pygame.K_w]: self.vector_move.y = -1
        elif keys[pygame.K_s]: self.vector_move.y = 1
        elif keys[pygame.K_a]: self.vector_move.x = -1
        elif keys[pygame.K_d]: self.vector_move.x = 1

        if self.vector_move.length() > 0:
            self.vector_move = self.vector_move.normalize()

        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shoot_time >= self.shoot_cooldown:
                self.shoot(self.laser_group, self.laser_frames, self.laser_sound)
                self.last_shoot_time = now

    def move(self, delta_time):
        self.rect.center += self.vector_move * self.speed * delta_time
        self.rect.clamp_ip(pygame.display.get_surface().get_frect())

        self.hitbox_rect.center = self.rect.center # -> Update HitBox Rect

    def shoot(self, laser_group, laser_frames, laser_sound):
        Laser.launch(laser_group, laser_frames, laser_sound, self)

    def check_meteor_collision(self):
        if self.invincible:
            return

        for meteor in self.meteor_group:
            if self.hitbox_rect.colliderect(meteor.hitbox_rect):
                meteor.kill() # -> Destroy Meteor
                self.health -= 1
                self.hit_sound.play()

                self.invincible = True
                self.invincible_start = pygame.time.get_ticks()
                self.last_time_blink = pygame.time.get_ticks()
                self.blink = True

                break

    def check_fragment_collision(self):
        hits = pygame.sprite.spritecollide(self, self.fragment_group, True)

        if hits:
            for hit in hits:
                hit.sound.play()
                hit.kill()
                self.fragments += 1

    def update_invincibility(self):
        now = pygame.time.get_ticks()

        if now - self.invincible_start >= self.invincible_time:
            self.invincible = False
            self.blink = False
            self.image.set_alpha(255)
        else:
            if now - self.last_time_blink >= self.blink_speed:
                self.last_time_blink = now
                self.blink = not self.blink

                self.image.set_alpha(80 if self.blink else 255)

    def Update_PowerUp_Effect(self):
        now = pygame.time.get_ticks()

        if self.is_powerup_effect:
            if now - self.powerup_effect_start >= self.powerup_cooldown:
                self.shoot_cooldown = 500
                self.is_powerup_effect = False

        return

    def check_powerup_collision(self):
        hits = pygame.sprite.spritecollide(self, self.powerup_group, True)

        if hits:
            for power in hits:
                self.powerup_sound.play()
                self.apply_power(power)

    def apply_power(self, power_up):
        now = pygame.time.get_ticks()

        if power_up.type == "HEALTH":
            self.health = min(self.health + 1, 3)
        
        elif power_up.type == "SPEED":
            self.shoot_cooldown = 300
            self.is_powerup_effect = True
            self.powerup_effect_start = now