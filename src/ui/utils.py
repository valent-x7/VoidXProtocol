import pygame
import json

def draw_text(screen: pygame.Surface, font: pygame.Font, text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_frect(center = (x, y))
    screen.blit(text_surface, text_rect)

def load_fragment_goal(path):
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
        return config["Fragment-Goal"]
    
def set_fragment_goal(path, new_value):
    new_value = max(1, new_value)

    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    config["Fragment-Goal"] = new_value

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)