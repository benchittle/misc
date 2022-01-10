import pygame as pg
import settings


class Tile:

    def __init__(self, adjacent_tile, room_class, placement=None):
        self.rect = pg.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE)

        if adjacent_tile is not None:
            if placement == "right":
                self.rect.midleft = adjacent_tile.rect.midright
                entrance = "left"
            elif placement == "left":
                self.rect.midright = adjacent_tile.rect.midright
                entrance = "right"
            elif placement == "bottom":
                self.rect.midtop = adjacent_tile.rect.midbottom
                entrance = "top"
            elif placement == "top":
                self.rect.midbottom = adjacent_tile.rect.midtop
                entrance = "bottom"

        elif adjacent_tile is None:
            self.rect.topleft = (0, 0)
            entrance = "right"

        self.room = room_class(self.rect.topleft, {entrance})


class Room:
    V_WALL = pg.Rect(0, 0, settings.WALL_WIDTH, settings.TILE_SIZE)
    H_WALL = pg.Rect(0, 0, settings.TILE_SIZE, settings.WALL_WIDTH)

    OUTER_WALLS = {
        "top" : H_WALL.copy(),
        "left" : V_WALL.copy(),
        "right" : V_WALL.copy().move(H_WALL.right - V_WALL.w, 0),
        "bottom" : H_WALL.copy().move(0, V_WALL.bottom - H_WALL.h)
        }

    def __init__(self, pos, doors):
        self.pos = pos if type(pos) == pg.Vector2 else pg.Vector2(pos)
        self.doors = doors if type(doors) == set else set(doors)


    @property
    def bound_rect(self):
        return self.walls[0].unionall(self.walls[1:])

    @property
    def walls(self):
        _walls = []
        for key, wall in Room.OUTER_WALLS.items():
            if key in self.doors:
                _walls += self.create_door(wall)
            else:
                _walls.append(wall.copy())

        for wall in _walls:
            wall.topleft += self.pos

        return _walls


    def create_door(self, wall):
        rect = wall.copy()
        if rect.w > rect.h:
            rect.w = (rect.w - settings.DOOR_WIDTH) / 2
            return [rect.copy(), rect.copy().move(rect.w + settings.DOOR_WIDTH, 0)]

        elif rect.h > rect.w:
            rect.h = (rect.h - settings.DOOR_WIDTH) / 2
            return [rect.copy(), rect.copy().move(0, rect.h + settings.DOOR_WIDTH)]






class Hall:
    V_WALL = pg.Rect(0, 0, settings.WALL_WIDTH, settings.TILE_SIZE)
    H_WALL = pg.Rect(0, 0, settings.TILE_SIZE, settings.WALL_WIDTH)

    OUTER_WALLS = {
        "main" : V_WALL.copy(),
        "far" : V_WALL.copy().move(settings.DOOR_WIDTH + settings.WALL_WIDTH, 0)
        }

    def __init__(self, x, y):
        pass



tile1 = Tile(None, Room)
tile2 = Tile(tile1, Room, "right")
tile3 = Tile(tile2, Room, "bottom")











LEVEL_PLAYGROUND = {
    "player" : {
        "pos" : (settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2),
        "vel" : (0, 0)
        },
    "walls" : [
        (0, 0, settings.SCREEN_WIDTH, 5, settings.RED), # Top border
        (0, 0, 5, settings.SCREEN_HEIGHT, settings.RED), # Left border
        (settings.SCREEN_WIDTH - 5, 0, 5, settings.SCREEN_HEIGHT, settings.RED), # Right border
        (0, settings.SCREEN_HEIGHT - 5, settings.SCREEN_WIDTH, 5, settings.RED), # Bottom border
        (800, 0, 50, 600, settings.RED), # Big red wall 1
        (1000, 480, 50, 600, settings.RED) # Big red wall 2
        ],
    "moving walls" : [
        (1400, 0, 50, 50, settings.BLUE)
        ],
    "targets" : [
        (100, 600, 50, 50, settings.BLUE),
        (1, 1, 1, 1, settings.BLUE)
        ]
}








def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()





