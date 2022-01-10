import pygame as pg
import environment

class Level:
    def __init__(self, sprites, level_dict):#, targets):
        self.sprites = sprites
        self.level_dict = level_dict

    def setup(self):
        for x, y, w, h, c in self.level_dict["walls"]:
            environment.Wall(self.sprites, x, y, w, h, c)
        for x, y, w, h, c in self.level_dict["moving walls"]:
            environment.MovingWall(self.sprites, x, y, w, h, c)
        for x, y, w, h, c in self.level_dict["targets"]:
            environment.Target(self.sprites, x, y, w, h, c)



