import itertools, random
import pygame as pg
import settings


def pairwise(iterable):
    """
    Iterate pairwise through an iterable.

    pairwise([1,2,3,4]) -> (1,2),(2,3),(3,4)
    """
    val, nextVal = itertools.tee(iterable)
    next(nextVal, None)
    return zip(val, nextVal)


class SimpleRoom:
    size = 500

    def __init__(self, tile):
        V_WALL = pg.Rect(0, 0, settings.WALL_WIDTH, SimpleRoom.size)
        H_WALL = pg.Rect(0, 0, SimpleRoom.size, settings.WALL_WIDTH)

        top = H_WALL.copy()
        top.topleft = tile.rect.topleft

        left = V_WALL.copy()
        left.topleft = tile.rect.topleft

        right = V_WALL.copy()
        right.topright = tile.rect.topright

        bottom = H_WALL.copy()
        bottom.bottomleft = tile.rect.bottomleft

        self.walls = [top, left, right, bottom]


    def create_door(self, wall):
        rect = wall.copy()
        if rect.w > rect.h:
            rect.w = (rect.w - settings.DOOR_WIDTH) / 2
            return [rect.copy(), rect.copy().move(rect.w + settings.DOOR_WIDTH, 0)]

        elif rect.h > rect.w:
            rect.h = (rect.h - settings.DOOR_WIDTH) / 2
            return [rect.copy(), rect.copy().move(0, rect.h + settings.DOOR_WIDTH)]





class Tile:
    def __init__(self, room_class, placement=None, adjacent_tile=None):
        self.rect = pg.Rect((0, 0), (room_class.size, room_class.size))

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

        self.room = room_class(self)


class Map:
    def __init__(self, size):
        self.size = size
        self.map_string = self.generate_map_string()
        self.tiles = self.generate_map()


    def generate_map_string(self):
        coords = []
        string = ""
        prev = [0, 0]
        while len(coords) < self.size:
            new = prev[:]
            new[random.randint(0, 1)] += random.choice([1, -1])
            if new not in coords:
                coords.append(new)
                prev = new[:]

        for coord, next_coord in pairwise(coords):
            dx = next_coord[0] - coord[0]
            dy = next_coord[1] - coord[1]
            if dx == 1:
                string += "e"
            elif dx == -1:
                string += "w"
            elif dy == 1:
                string += "n"
            elif dy == -1:
                string += "s"

        return string


    def generate_map(self):
        tiles = [Tile(SimpleRoom)]
        prev = tiles[0]
        for direction in self.map_string:
            new_tile = Tile(SimpleRoom, direction, prev)
            tiles.append(new_tile)
            prev = new_tile
        return tiles


    def get_walls(self):
        walls = []
        for tile in self.tiles:
            walls += tile.room.walls

        return walls






map1 = Map(10)








TEST_LEVEL = {
    "player" : {
        "pos" : (0.2 * settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT / 2),
        "vel" : (0, 0)
    },
    "walls" : map1.get_walls()

}




def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()
