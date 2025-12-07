import pygame
from ui.button import ButtonUI
from ui.utils import draw_text
from settings import join, getcwd

class GameOver:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.wd = getcwd()

        bg = pygame.image.load(join(self.wd, "assets", "images", "screens", "space.png"))
        self.bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height)).convert()
        self.setup_fonts()
        self.setup_UI()

    def run(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "MENU"
                            
            if self.retry_btn.is_clicked(e):
                return "PLAY"
            
            elif self.main_menu_btn.is_clicked(e):
                return "MENU"
        
        self.screen.blit(self.bg, [0, 0])
        
        draw_text(self.screen, self.title_font, "You lose!", "white", self.screen_width / 2, self.screen_height / 3)
        self.retry_btn.draw()
        self.main_menu_btn.draw()

        return "GAMEOVER"
    
    def setup_fonts(self):
        vt323_path = join(self.wd, "assets", "fonts", "VT323", "VT323-Regular.ttf")
        self.title_font = pygame.font.Font(vt323_path, 124)
        self.button_font = pygame.font.Font(vt323_path, 62)

    def setup_UI(self):
        self.button_clicked_sound = pygame.Sound(join(self.wd, "assets", "audio", "button_clicked.mp3"))
        self.button_clicked_sound.set_volume(0.2)

        self.retry_btn = ButtonUI(self.screen, (self.screen_width / 2, self.screen_height / 2), "#312c85", "#242161",
                                self.button_font, "Retry", 300, 90, self.button_clicked_sound)
        self.main_menu_btn = ButtonUI(self.screen, (self.screen_width / 2, self.screen_height / 2 + 110), "#312c85", "#242161",
                                self.button_font, "Main Menu", 300, 90, self.button_clicked_sound)