import pygame
from ui.button import ButtonUI
from ui.utils import draw_text
from settings import join, getcwd

class Win:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()
        self.wd = getcwd()

        bg = pygame.image.load(join(self.wd, "assets", "images", "screens", "space.png"))
        self.bg = pygame.transform.scale(bg, (self.screen_w, self.screen_h)).convert()
        self.setup_fonts()

    def run(self, events: list[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "MENU"
                
        self.screen.blit(self.bg, [0, 0])

        draw_text(self.screen, self.title_font, "You win!", "white", self.screen_w / 2, self.screen_h / 3)

        return "WIN"
    
    def setup_fonts(self):
        vt323_path = join(self.wd, "assets", "fonts", "VT323", "VT323-Regular.ttf")
        self.title_font = pygame.font.Font(vt323_path, 124)