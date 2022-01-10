import pygame as pg
import settings


class Tile:
    def __init__(self, kind, placement=None, adjacent_tile=None):
        if kind == "reg":
            size = (settings.REG_TILE_SIZE,) * 2
        elif kind == "big":
            size = (settings.BIG_TILE_SIZE,) * 2
        elif kind == "hall":
            size = (settings.HALL_TILE_SIZE,) * 2

        self.rect = pg.Rect((0, 0), size)

        if adjacent_tile is not None:
            if placement == "e":
                self.rect.midleft = adjacent_tile.rect.midright
            elif placement == "w":
                self.rect.midright = adjacent_tile.rect.midright
            elif placement == "s":
                self.rect.midtop = adjacent_tile.rect.midbottom
            elif placement == "n":
                self.rect.midbottom = adjacent_tile.rect.midtop
        else:
            self.rect.center = (0, 0)














'''
TEST_LEVEL = {
    "player" : {
        "pos" : (0.2 * settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT / 2),
        "vel" : (0, 0)
    },
    "walls" : tile1.room.walls + tile2.room.walls + tile3.room.walls#room1.walls + room2.walls + room3.walls + room4.walls

}
'''



def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()
