"""
Date: April 27, 2020
Version: 0.4.0
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
ORANGE = (255, 127, 0)
WHITE = (255, 255, 255)
GRAY = (190, 190, 190)
BLACK = (0, 0, 0)



# Application settings
TITLE = "TROJAN"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_MID = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
FPS = 60

#UI settings
HOTBAR_SIZE = (SCREEN_WIDTH / 12, SCREEN_HEIGHT / 2)
HOTBAR_OFFSET = 4


# Player inventory
INV_SIZE = 9


# Player movement
PLAYER_FRICTION = 0.2
PLAYER_MIN_VEL = 0.3
PLAYER_ACCEL = 1.2
PLAYER_MAX_SPEED = 6


# Enemy attributes
SENTRY_SIZE = 25


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
ITEM_LAYER = 2
PROJECTILE_LAYER = 3 # sprite layer?
SPRITE_LAYER = 4
SPRITE_LAYER_FRONT = 5





