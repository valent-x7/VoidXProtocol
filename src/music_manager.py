import pygame
from settings import *

class MusicManager:
    def __init__(self):
        self.wd = getcwd()
        pygame.mixer.music.set_volume(0.4)
        self.current_track = None

        self.tracks = {
            # ? --- Track Path --- Loops
            "MENU": [join(self.wd, "assets", "songs", "menu_loop.mp3"), -1],
            "PLAY": [join(self.wd, "assets", "songs", "play_loop.wav"), -1],
            "GAMEOVER": [join(self.wd, "assets", "songs", "gameover.wav"), 0],
            "WIN": [join(self.wd, "assets", "songs", "win.mp3"), 0]
        }

    def play_state(self, state):
        if state not in self.tracks:
            return
        
        track_path = self.tracks[state][0]
        track_loops = self.tracks[state][1]

        if self.current_track == track_path:
            return
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play(track_loops)

        self.current_track = track_path

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None