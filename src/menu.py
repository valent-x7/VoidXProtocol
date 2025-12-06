import pygame
from settings import *
from ui.button import ButtonUI
from ui.utils import draw_text

class Menu:
    def __init__(self, screen: pygame.Surface, stars_group: pygame.sprite.Group):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.wd = getcwd()
        self.stars_group = stars_group
        self.setup_fonts()
        self.setup_ui()

    def run(self, events: list[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "EXIT"
                
            if self.play_btn.is_clicked(e):
                return "PLAY"
            elif self.exit_btn.is_clicked(e):
                return "EXIT"
                
        # ? --- Draw Background ---
        self.screen.blit(self.background, [0, 0])

        # ? --- Update and Draw Stars Group ---
        self.stars_group.update()
        self.stars_group.draw(self.screen)

        # ? --- Draw title and buttons ---
        draw_text(self.screen, self.title_font, "Void X Protocol", "white", self.screen_width // 2, self.screen_height // 3)
        self.play_btn.draw()
        self.settings_btn.draw()
        self.exit_btn.draw()

        return "MENU"
    
    def setup_fonts(self):
        vt323_path = join(self.wd, "assets", "fonts", "VT323", "VT323-Regular.ttf")

        self.title_font = pygame.font.Font(vt323_path, 124)
        self.button_font = pygame.font.Font(vt323_path, 62)

    def setup_ui(self):
        background_img = pygame.image.load(join(self.wd, "assets", "images", "menu", "space.png"))
        self.background = pygame.transform.scale(background_img, (self.screen_width, self.screen_height)).convert()

        self.button_clicked_sound = pygame.Sound(join(self.wd, "assets", "audio", "button_clicked.mp3"))
        self.button_clicked_sound.set_volume(0.2)

        # * --- Define Menu Buttons ---
        self.play_btn = ButtonUI(self.screen, (self.screen_width // 2, self.screen_height // 2), "#312c85", "#242161",
                                self.button_font, "Play", 300, 90, self.button_clicked_sound)
        self.settings_btn = ButtonUI(self.screen, (self.screen_width // 2, self.screen_height // 2 + 110), "#312c85", "#242161",
                                    self.button_font, "Settings", 300, 90, self.button_clicked_sound)
        self.exit_btn = ButtonUI(self.screen, (self.screen_width // 2, self.screen_height // 2 + 220), "#312c85", "#242161",
                                self.button_font, "Exit", 300, 90, self.button_clicked_sound)