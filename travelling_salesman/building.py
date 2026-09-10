import globals
import pygame
from pygame import draw
from pygame import Rect

building_size = 12
building_half_size = building_size / 2

class Building:
    def __init__(self, index, position):
        self.index = index
        self.pos = position
        self.rect = Rect(self.pos.x - building_half_size, self.pos.y - building_half_size, building_size, building_size)

    def draw(self):
        draw.rect(globals.screen, (255, 255, 255), self.rect)
        text_surface = globals.game_font.render(str(self.index), False, (255, 0, 0))
        globals.screen.blit(text_surface, self.pos)
