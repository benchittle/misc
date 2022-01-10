'''def parse_level_string(level_string):
    assert len(level_string) == 100

    rows = []
    cols = []

    for i in range(0, 100, 10):
        rows.append(level_string[i : i + 10])

    for i in range(10):
        cols.append("".join([s for s in level_string[i::10]]))

    r = iter(rows)
    wall_len = 0
    for i in range(10):
        if next(r) == "w":
            wall_len += 1
        else:

    print(rows)
    print(cols)

'''



ex = (
"          "
"wwwwwwwwww"
"w         "
"w         "
"w         "
"          "
"wwwwwwwwww"
"w         "
"w         "
"w         "
)

#parse_level_string(ex)





TITLE = "Testing 123"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60


PLAYER_FRICTION = 0.15
PLAYER_MIN_VEL = 0.3
PLAYER_ACCEL = 2
PLAYER_MAX_SPEED = 7

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

w = 50

TEST_LEVEL = {
    "player" : {
        "pos" : (0.2 * SCREEN_WIDTH, SCREEN_HEIGHT / 2),
        "vel" : (0, 0)
    },


}










'''
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
        (500, 0, w, 500, WHITE), #1
        (0, 500, 500, w, WHITE), #2
        (0, 800, 500, w, WHITE), #3
        (500, 850, w, 450, WHITE), #4
        (1000, 0, w, 500, WHITE), #5
        (1050, 500, 950, w, WHITE), #6
        (1050, 800, 950, w, WHITE), #7
        (1000, 850, w, 450, WHITE), #8
        (500, 650, 50, 50, WHITE) #Mid
        ],
    "moving walls" : [],
    "targets" : []
    }
'''