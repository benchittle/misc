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



red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
w = 50

playground = {
    "walls" : [
        (0, 0, SCREEN_WIDTH, 5, red), # Top border
        (0, 0, 5, SCREEN_HEIGHT, red), # Left border
        (SCREEN_WIDTH - 5, 0, 5, SCREEN_HEIGHT, red), # Right border
        (0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5, red), # Bottom border
        (800, 0, 50, 600, red), # Big red wall 1
        (1000, 480, 50, 600, red) # Big red wall 2
        ],
    "moving walls" : [
        (1400, 0, 50, 50, blue)
        ],
    "targets" : [
        (100, 600, 50, 50, blue),
        (1, 1, 1, 1, blue)
        ]
}

test_level = {

     #     #
     #1    #5
     #     #    6
######2    ##########
        #
        #
######3     ##########
     #4    #    7
     #     #8
     #     #
    "walls" : [
        (500, 0, w, 500, white), #1
        (0, 500, 500, w, white), #2
        (0, 800, 500, w, white), #3
        (500, 850, w, 450, white), #4
        (1000, 0, w, 500, white), #5
        (1050, 500, 950, w, white), #6
        (1050, 800, 950, w, white), #7
        (1000, 850, w, 450, white), #8
        (500, 650, 50, 50, white) #Mid
        ],
    "moving walls" : [],
    "targets" : []
    }