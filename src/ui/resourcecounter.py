import pygame


class ResourceCounter:
    def __init__(self, TextFont: pygame.Font, Text, TextColor, Position, Image, TotalAmout):
        self.image = Image
        self.image_rect = self.image.get_frect(center = Position)

        self.font = TextFont
        self.text_surface = self.font.render(Text, True, TextColor)
        self.text_rect = self.text_surface.get_frect(topleft = (self.image_rect.right + 10, self.image_rect.top + 10))

        self.total_amount = TotalAmout
        self.amount = 0 # -> Inicial Amount
        self.amount_text_surface = self.font.render(f"{self.amount} / {self.total_amount}", True, "white")
        self.amount_rect = self.amount_text_surface.get_frect(topleft = ((self.image_rect.right + 10, self.image_rect.centery)))

    def update(self, amount):
        if amount != self.amount:
            self.amount = amount
            self.amount_text_surface = self.font.render(f"{self.amount} / {self.total_amount}", True, "white")

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.image_rect)
        screen.blit(self.text_surface, self.text_rect)
        screen.blit(self.amount_text_surface, self.amount_rect)