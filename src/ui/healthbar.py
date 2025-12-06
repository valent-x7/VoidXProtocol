import pygame

class HealthBar:
    def __init__(self, image, initial_pos, max_health):
        self.x, self.y = initial_pos
        self.heart_image = image
        self.max_health = max_health
        self.current_health = self.max_health

        self.spacing = 5

    def update(self, value):
        self.current_health = value
        self.current_health = max(0, self.current_health)

    def draw(self, screen):
        for i in range(self.current_health):
            pos_x = self.x + (self.heart_image.get_width() + self.spacing) * i
            pos_y = self.y
            screen.blit(self.heart_image, (pos_x, pos_y))
