import math

TITLE = "Testing 123"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_MID = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
FPS = 60

PLAYER_FRICTION = 0.1
PLAYER_MIN_VEL = 0.3
PLAYER_ACCEL = 1.4
PLAYER_MAX_SPEED = 10

WALL_WIDTH = 10
TILE_SIZE = 200
TILE_GAP = 0
DOOR_SIZE = 80
SUB_LAYER = 0


TILE_LAYER = 1
ROOM_LAYER = 2
PROJECTILE_LAYER = 3
ITEM_LAYER = 4
SPRITE_LAYER = 5


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROOM_COLOUR = (100, 100, 100)
TILE_COLOUR = (63, 63, 63)
WALL_COLOUR = WHITE





CARDINALS = ("n", "e", "s", "w")
CORNERS = ("topleft", "topright", "bottomright", "bottomleft")

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