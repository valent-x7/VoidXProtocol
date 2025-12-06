import pygame
from settings import *
from sprites.star import Star
from menu import Menu
from play import Play
from gameover import GameOver
from win import Win
from music_manager import MusicManager

class Game:
    def __init__(self, state = "MENU"):
        self.wd = getcwd()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()
        pygame.display.set_caption("Void juego")
        self.clock = pygame.time.Clock()
        self.state = state
        self.stars_group = pygame.sprite.Group()
        self.create_stars()

        self.music_manager = MusicManager()
        self.menu = None
        self.play = None
        self.gameover = None
        self.win = None
        self.running = True

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            
            events = pygame.event.get()

            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            self.music_manager.play_state(self.state)

            if self.state == "MENU":
                if not self.menu:
                    self.menu = Menu(self.screen, self.stars_group)
                
                self.state = self.menu.run(events)
            
            elif self.state == "PLAY":
                if not self.play:
                    self.play = Play(self.screen, self.stars_group)
                
                next_state = self.play.run(self.dt, events)

                if next_state == "MENU":
                    self.play = None
                    self.state = "MENU"
                else:
                    self.state = next_state
            
            elif self.state == "GAMEOVER":
                if not self.gameover:
                    self.gameover = GameOver(self.screen)
                
                self.state = self.gameover.run(events)
                self.play = None

            elif self.state == "WIN":
                if not self.win:
                    self.win = Win(self.screen)
                
                self.state = self.win.run(events)
                self.play = None

            elif self.state == "RETRY":
                if self.play:
                    self.play = None

                self.state = "PLAY"

            elif self.state == "EXIT":
                self.running = False

            pygame.display.flip()

        pygame.quit()

    def create_stars(self):
        self.star_image = pygame.image.load(join(self.wd, "assets", "images", "menu", "star.png")).convert_alpha()
        for _ in range(35):
            Star(self.stars_group, self.star_image, self.screen_w, self.screen_h)