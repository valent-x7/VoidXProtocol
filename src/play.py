import pygame
from sprites.player import Player
from sprites.meteor import Meteor
from sprites.powerup import PowerUp
from sprites.fragment import Fragment
from ui.button import ButtonUI
from ui.healthbar import HealthBar
from ui.utils import draw_text, load_fragment_goal
from ui.counter import TimeCounter
from ui.resourcecounter import ResourceCounter
from settings import *

class Play:
    def __init__(self, screen: pygame.Surface, stars_group):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.wd = getcwd()
        self.player_group = pygame.sprite.Group()
        self.meteors_group = pygame.sprite.Group()
        self.fragment_group = pygame.sprite.Group()
        self.lasers_group = pygame.sprite.Group()
        self.powerups_group = pygame.sprite.Group()
        self.stars_group = stars_group

        self.fragment_goal = load_fragment_goal(join(self.wd, "game_config.json"))

        self.setup_sprites()
        self.setup_map()
        self.setup_fonts()
        self.setup_ui()

        self.showing_quit_popup = False
        self.paused = False

    def run(self, delta_time, events):
        for e in events:
            if self.showing_quit_popup:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return "MENU"
                    elif e.key == pygame.K_BACKSPACE:
                        self.showing_quit_popup = False
                
                if self.exit_btn.is_clicked(e):
                    return "MENU"
                
                elif self.go_back_btn.is_clicked(e):
                    self.showing_quit_popup = False
            else:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.showing_quit_popup = True
                    elif e.key == pygame.K_p:
                        self.paused = not self.paused

                elif e.type == self.METEOR_EVENT and not self.paused and not self.showing_quit_popup:
                    pos = (randint(20, int(self.screen_width)), randint(-85, -60))
                    Meteor(self.meteors_group, self.lasers_group, self.meteor_frames, self.explosion_sound, pos, self.screen_height)
            
                elif e.type == self.FRAGMENT_EVENT and not self.paused and not self.showing_quit_popup:
                    pos = (randint(20, int(self.screen_width)), randint(-85, -60))
                    image = choice(self.fragment_images)
                    Fragment(self.fragment_group, image, pos, self.screen_height, self.fragment_pickup)

                elif e.type == self.POWERUP_EVENT and not self.paused and not self.showing_quit_popup:
                    pos = (randint(20, int(self.screen_width)), randint(-85, -60))
                    type = choice(self.PowerUp_Choices)
                    image = self.PowerUp_Dict[type]

                    PowerUp(self.powerups_group, image, pos, type, self.screen_height)

        self.screen.blit(self.background, [0, 0])

        # ? --- Update Groups
        if not self.paused and not self.showing_quit_popup:
            self.stars_group.update()
            self.meteors_group.update(delta_time)
            self.fragment_group.update(delta_time)
            self.lasers_group.update(delta_time)
            self.HealthBar.update(self.player.health)
            self.TimeCounter.update(delta_time)
            self.FragmentCounter.update(self.player.fragments)
            self.powerups_group.update(delta_time)
            self.player_group.update(delta_time)

        # ? --- Draw Groups
        self.stars_group.draw(self.screen)
        self.powerups_group.draw(self.screen)
        self.fragment_group.draw(self.screen)
        self.meteors_group.draw(self.screen)
        self.lasers_group.draw(self.screen)
        self.HealthBar.draw(self.screen)
        self.TimeCounter.draw(self.screen)
        self.FragmentCounter.draw(self.screen)
        self.player_group.draw(self.screen)

        if self.paused:
            draw_text(self.screen, self.title_font, "Game Paused", "white", self.screen_width // 2, self.screen_height // 2)

        if self.player.health <= 0:
            return "GAMEOVER"
        elif self.player.fragments >= self.fragment_goal:
            return "WIN"
        
        if self.showing_quit_popup: # -> Exit
            self.screen.blit(self.scrim, [0, 0])
            pygame.draw.rect(self.screen, "#2A183B", self.popup_rect)
            pygame.draw.rect(self.screen, "#9D4EFF", self.popup_rect, 2)

            draw_text(self.screen, self.popup_title_font, "SIGNAL LOST", "white", self.screen_width // 2, self.screen_height // 2 - 95)
            draw_text(self.screen, self.popup_description_font, "Core Fragments will remain uncollected. Confirm exit?", "#D0B8E8", self.screen_width // 2, self.screen_height // 2)
            self.exit_btn.draw()
            self.go_back_btn.draw()

        return "PLAY"
    
    def setup_sprites(self):
        # ? --- Player ---
        ship_frames = [pygame.image.load(join(self.wd, "assets", "images", "ship", f"{i}.png")) for i in range(1, 5)]
        self.ship_frames = [pygame.transform.scale(frame, (128, 128)).convert_alpha() for frame in ship_frames]
        self.metal_hit_sound = pygame.Sound(join(self.wd, "assets", "audio", "ship_hit.mp3"))
        self.metal_hit_sound.set_volume(0.2)

        # ? --- Meteor ---
        meteor_frames = [pygame.image.load(join(self.wd, "assets", "images", "meteor", f"{i}.png")) for i in range(1, 5)]
        self.meteor_frames = [pygame.transform.scale(frame, (96, 96)).convert_alpha() for frame in meteor_frames]
        self.explosion_sound = pygame.Sound(join(self.wd, "assets", "audio", "explosion.mp3"))
        self.explosion_sound.set_volume(0.2)

        # ? --- Laser ---
        laser_frames = [pygame.image.load(join(self.wd, "assets", "images", "laser", f"{i}.png")) for i in range(1, 5)]
        self.laser_frames = [pygame.transform.scale(frame, (96, 96)).convert_alpha() for frame in laser_frames]
        self.laser_sound = pygame.Sound(join(self.wd, "assets", "audio", "laser.mp3"))
        self.laser_sound.set_volume(0.2)

        # ? --- Core Fragments
        fragment_images = [pygame.image.load(join(self.wd, "assets", "images", "fragments", f"{i}.png")) for i in range(1, 5)]
        self.fragment_images = [pygame.transform.scale(frame, (96, 96)).convert_alpha() for frame in fragment_images]
        self.fragment_pickup = pygame.Sound(join(self.wd, "assets", "audio", "fragment_pickup.mp3"))
        self.fragment_pickup.set_volume(0.2)

        # ? --- UI and PowerUps
        heart = pygame.image.load(join(self.wd, "assets", "images", "elements", "heart.png"))
        self.heart = pygame.transform.scale(heart, (96, 96)).convert_alpha()

        bolt = pygame.image.load(join(self.wd, "assets", "images", "elements", "bolt.png"))
        self.bolt = pygame.transform.scale(bolt, (96, 96)).convert_alpha()

        fragments = pygame.image.load(join(self.wd, "assets", "images", "elements", "fragments.png"))
        self.fragments = pygame.transform.scale(fragments, (96, 96)).convert_alpha()

        self.PowerUp_Choices = ["HEALTH", "SPEED"]
        self.PowerUp_Dict = {
            "HEALTH": self.heart,
            "SPEED": self.bolt
        }
        self.powerup_sound = pygame.Sound(join(self.wd, "assets", "audio", "powerup.mp3"))
        self.powerup_sound.set_volume(0.2)

    def setup_map(self):
        self.player = Player(self.player_group, self.fragment_group, self.powerups_group, self.powerup_sound, self.meteors_group, self.lasers_group,
                            self.laser_frames, self.laser_sound, self.ship_frames, (self.screen_width // 2,
                            self.screen_height - 80), self.metal_hit_sound)

        # ? --- Meteor Event
        self.METEOR_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.METEOR_EVENT, 600)

        # ? --- Fragment Event
        self.FRAGMENT_EVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.FRAGMENT_EVENT, 6000) # -> 6 segundos

        # ? --- PowerUp Event
        self.POWERUP_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(self.POWERUP_EVENT, 12000) # -> 12 segundos
    
    def setup_ui(self):
        background_img = pygame.image.load(join(self.wd, "assets", "images", "menu", "space.png"))
        self.background = pygame.transform.scale(background_img, (self.screen_width, self.screen_height)).convert()
        self.button_clicked_sound = pygame.Sound(join(self.wd, "assets", "audio", "button_clicked.mp3"))
        self.button_clicked_sound.set_volume(0.2)

        self.HealthBar = HealthBar(self.heart, (42, 20), 3)
        self.TimeCounter = TimeCounter(self.screen_width / 2 - 80, 25, 240, 80, self.time_counter_font)
        self.FragmentCounter = ResourceCounter(self.resource_counter_font, "Core Fragments", "white", (60, 180), self.fragments, self.fragment_goal)

        # ? --- Quit PopUp ---
        self.scrim = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.scrim.fill((0, 0, 0, 150))
        self.popup_rect = pygame.FRect(0, 0, self.screen_width - 325, self.screen_height // 3)
        self.popup_rect.center = (self.screen_width // 2, self.screen_height // 2)

        self.exit_btn = ButtonUI(self.screen, (self.screen_width // 2 - 155, self.screen_height // 2 + 95), "#A62056", "#FF3080",
                                self.popup_button_font, "Exit", 200, 45, self.button_clicked_sound)
        self.go_back_btn = ButtonUI(self.screen, (self.screen_width // 2 + 155, self.screen_height // 2 + 95), "#5A3896", "#8A60D0",
                                self.popup_button_font, "Go Back", 200, 45, self.button_clicked_sound)

    def setup_fonts(self):
        vt323_path = join(self.wd, "assets", "fonts", "VT323", "VT323-Regular.ttf")

        self.title_font = pygame.font.Font(vt323_path, 124)
        self.time_counter_font = pygame.font.Font(vt323_path, 84)
        self.resource_counter_font = pygame.font.Font(vt323_path, 32)

        # ? --- Quit PopUp Fonts ---
        self.popup_title_font = pygame.font.Font(vt323_path, 84)
        self.popup_description_font = pygame.font.Font(vt323_path, 62)
        self.popup_button_font = pygame.font.Font(vt323_path, 42)