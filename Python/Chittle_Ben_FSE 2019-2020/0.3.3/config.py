"""
Date: April 9, 2020
Version: 0.3.3
"""


import math
import pygame as pg

# Common directions and conversions
CARDINALS = ("n", "e", "s", "w")
CONVERSIONS = {
    "n" : "top",
    "e" : "right",
    "s" : "bottom",
    "w" : "left",
    "top" : "n",
    "right" : "e",
    "bottom" : "s",
    "left" : "w"
    }
OPPOSITES = {
    "n" : "s",
    "e" : "w",
    "s" : "n",
    "w" : "e",
    "top" : "bottom",
    "right" : "left",
    "bottom" : "top",
    "left" : "right"
}

# Common RGB colour values
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



# Application settings
TITLE = "Testing 123"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_MID = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
FPS = 60

#UI settings
HOTBAR_SIZE = (SCREEN_WIDTH / 16, SCREEN_HEIGHT / 3)


# Player movement
PLAYER_FRICTION = 0.1
PLAYER_MIN_VEL = 0.3
PLAYER_ACCEL = 1.4
PLAYER_MAX_SPEED = 10


# Room sizing and colours
WALL_WIDTH = 20
TILE_SIZE = 200
TILE_GAP = 0
DOOR_SIZE = 80

ROOM_COLOUR = (100, 100, 100)
TILE_COLOUR = (63, 63, 63)
WALL_COLOUR = WHITE


# Sprite layering
TILE_LAYER = 0
ROOM_LAYER = 1
PROJECTILE_LAYER = 2 # sprite layer?
ITEM_LAYER = 3
SPRITE_LAYER = 4





