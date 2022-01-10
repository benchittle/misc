import level


TITLE = "Testing 123"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60


PLAYER_FRICTION = 0.2
PLAYER_MIN_VEL = 0.3
PLAYER_ACCEL = 1.5
PLAYER_MAX_SPEED = 7

ROOM_SIZE = 1000
WALL_WIDTH = 20

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)




LEVEL_PLAYGROUND = {
    "player" : {
        "pos" : (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        "vel" : (0, 0)
        },
    "walls" : [
        (0, 0, SCREEN_WIDTH, 5, RED), # Top border
        (0, 0, 5, SCREEN_HEIGHT, RED), # Left border
        (SCREEN_WIDTH - 5, 0, 5, SCREEN_HEIGHT, RED), # Right border
        (0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5, RED), # Bottom border
        (800, 0, 50, 600, RED), # Big red wall 1
        (1000, 480, 50, 600, RED) # Big red wall 2
        ],
    "moving walls" : [
        (1400, 0, 50, 50, BLUE)
        ],
    "targets" : [
        (100, 600, 50, 50, BLUE),
        (1, 1, 1, 1, BLUE)
        ]
}

test1 = (
    "   |  |   "
    "   |  |   "
    "---    ---"
    "          "
    "          "
    "---    ---"
    "   |  |   "
    "   |  |   "
    "   |  |   "
    "   |  |   "
    )


test2 = (
    " -------- "
    "|        |"
    "|        |"
    "|        |"
    "|        |"
    "|        |"
    "|        |"
    "|        |"
    "|        |"
    " -------- "
    )

r = level.Room(0, 0, None)
w = [(getattr(r, i).pos.x, getattr(r, i).pos.y, getattr(r, i).vec.x, getattr(r, i).pos.x)
                for i in ["top", "bottom", "left", "right"]]

print(w)

TEST_LEVEL = {
    "player" : {
        "pos" : (0.2 * SCREEN_WIDTH, SCREEN_HEIGHT / 2),
        "vel" : (0, 0)
    },
    "walls" : [(getattr(r, i).pos.x, getattr(r, i).pos.y, getattr(r, i).vec.x, getattr(r, i).pos.x)
                for i in ["top", "bottom", "left", "right"]]#level.parse_level_string(test2)

}


