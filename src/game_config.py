import pygame
from ui.button import ButtonUI
from ui.utils import draw_text, load_fragment_goal, set_fragment_goal
from settings import *

class GameConfig:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.wd = getcwd() # -> Working Directory
        self.setup_fonts()
        self.setup_UI()
        self.fragment_goal_path = join(self.wd, "game_config.json")

        self.fragment_goal = load_fragment_goal(self.fragment_goal_path)

    def run(self, events: list[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.fragment_goal = load_fragment_goal(self.fragment_goal_path)
                    return "MENU"
                
                if pygame.K_0 <= e.key <= pygame.K_9:
                    digit = e.unicode
                    new_value = str(self.fragment_goal) + digit
                    if len(new_value) <= 3:
                        self.fragment_goal = int(new_value)

                # ? --- Delete
                if e.key == pygame.K_BACKSPACE:
                    self.fragment_goal = int(str(self.fragment_goal)[:-1] or "0")
                
            if self.set_goal_btn.is_clicked(e):
                set_fragment_goal(self.fragment_goal_path, self.fragment_goal)
                self.fragment_goal = load_fragment_goal(self.fragment_goal_path)

            elif self.main_menu_btn.is_clicked(e):
                return "MENU"

        self.screen.blit(self.background, [0, 0])

        # ? --- Title and Subtitle 
        draw_text(self.screen, self.title_font, "Game Config", "white", self.screen_width // 2, self.screen_height // 4)
        draw_text(self.screen, self.button_font, "Fragment Goal:", "white", self.screen_width // 2, self.screen_height // 2 - 100)

        # ? --- Input
        pygame.draw.rect(self.screen, "white", self.input_rect, border_radius = 20)
        draw_text(self.screen, self.button_font, f"{self.fragment_goal}", "black", self.screen_width // 2, self.screen_height // 2)
        self.set_goal_btn.draw()
        self.main_menu_btn.draw()

        return "CONFIG"
    
    def setup_fonts(self):
        vt323_path = join(self.wd, "assets", "fonts", "VT323", "VT323-Regular.ttf")

        self.title_font = pygame.font.Font(vt323_path, 124)
        self.button_font = pygame.font.Font(vt323_path, 62)
    
    def setup_UI(self):
        background_img = pygame.image.load(join(self.wd, "assets", "images", "menu", "space.png"))
        self.background = pygame.transform.scale(background_img, (self.screen_width, self.screen_height)).convert()
        self.button_clicked_sound = pygame.Sound(join(self.wd, "assets", "audio", "button_clicked.mp3"))
        self.button_clicked_sound.set_volume(0.2)

        self.input_rect = pygame.FRect(0, 0, 375, 80)
        self.input_rect.center = (self.screen_width // 2, self.screen_height // 2)

        self.set_goal_btn = ButtonUI(self.screen, (self.screen_width // 2, self.screen_height // 2 + 150), "#312c85", "#242161",
                                     self.button_font, "Save", 300, 90, self.button_clicked_sound)
        
        self.main_menu_btn = ButtonUI(self.screen, (self.screen_width // 2, self.screen_height // 2 + 260), "#312c85", "#242161",
                                self.button_font, "Main Menu", 300, 90, self.button_clicked_sound)