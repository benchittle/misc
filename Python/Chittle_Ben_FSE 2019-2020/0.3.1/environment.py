import random
import pygame as pg
import config


class Block(pg.sprite.Sprite):
    def __init__(self, game, pos, dimensions, *groups, anchor="topleft"):
        super().__init__()
        self.game = game
        self.game.all_sprites.add(self, layer=config.SPRITE_LAYER)
        self.add(*groups)

        self.pos = pg.Vector2(pos)
        self.colour = config.WALL_COLOUR
        self.anchor = anchor

        self.image = pg.Surface(dimensions)
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.pos - self.game.screen_pos)


    def update(self):
       setattr(self.rect, self.anchor, self.pos - self.game.screen_pos)


    def copy(self, keep_anchors=True):
        anchor = self.anchor if keep_anchors else "topleft"
        return Block(self.game, self.pos, (self.rect.w, self.rect.h), *self.groups(), anchor=anchor)


    def split(self, gap, axis, kill=True):
        if axis == "x": #vertical
            size = (self.rect.w, (self.rect.h - gap) // 2)
            wall1 = Block(self.game, self.rect.topleft + self.game.screen_pos, size, *self.groups())
            wall2 = wall1.copy()
            wall2.pos.y = self.rect.bottom + self.game.screen_pos.y - wall1.rect.h
        elif axis == "y":
            size = ((self.rect.w - gap) // 2, self.rect.h)
            wall1 = Block(self.game, self.rect.topleft + self.game.screen_pos, size, *self.groups())
            wall2 = wall1.copy()
            wall2.pos.x = self.rect.right + self.game.screen_pos.x - wall1.rect.w
        if kill:
            self.kill()

        return wall1, wall2



class VWall(Block):
    def __init__(self, game, pos, *groups, anchor="topleft"):
        super().__init__(game, pos, (config.WALL_WIDTH, config.TILE_SIZE), *groups, anchor=anchor)


class HWall(Block):
    def __init__(self, game, pos, *groups, anchor="topleft"):
        super().__init__(game, pos, (config.TILE_SIZE, config.WALL_WIDTH), *groups, anchor=anchor)


class VDoorSmall(Block):
    def __init__(self, game, pos, *groups, anchor="topleft"):
        super().__init__(game, pos, (config.WALL_WIDTH, config.DOOR_SIZE + 2 * config.WALL_WIDTH), *groups, anchor=anchor)


class HDoorSmall(Block):
    def __init__(self, game, pos, *groups, anchor="topleft"):
        super().__init__(game, pos, (config.DOOR_SIZE + 2 * config.WALL_WIDTH, config.WALL_WIDTH), *groups, anchor=anchor)


class VWallDoor:
    def __init__(self, game, pos, *groups, anchor="topleft"):
        temp_wall = Block(game, pos, (config.WALL_WIDTH, config.TILE_SIZE), anchor=anchor)
        for piece in temp_wall.split(config.DOOR_SIZE, "x"):
            for group in groups:
                group.add(piece)


class HWallDoor:
    def __init__(self, game, pos, *groups, anchor="topleft",):
        temp_wall = Block(game, pos, (config.TILE_SIZE, config.WALL_WIDTH), anchor=anchor)
        for piece in temp_wall.split(config.DOOR_SIZE, "y"):
            for group in groups:
                group.add(piece)


class VCorr:
    def __init__(self, game, pos, *groups, anchor="topleft"):
        bound_size = (config.DOOR_SIZE + 2 * config.WALL_WIDTH, (config.TILE_SIZE - config.DOOR_SIZE) // 2)
        temp_wall = Block(game, pos, bound_size, anchor=anchor)#, groups=(self.game.walls))

        for piece in temp_wall.split(config.DOOR_SIZE, "y"):
            for group in groups:
                group.add(piece)


class HCorr:
    def __init__(self, game, pos, *groups, anchor="topleft"):
        bound_size = ((config.TILE_SIZE - config.DOOR_SIZE) // 2, config.DOOR_SIZE + 2 * config.WALL_WIDTH)
        temp_wall = Block(game, pos, bound_size, anchor=anchor)

        for piece in temp_wall.split(config.DOOR_SIZE, "x"):
            for group in groups:
                group.add(piece)


class VCorrDoor:
    def __init__(self, game, pos, *groups, anchor="topleft"):
        HDoorSmall(game, pos, *groups, anchor=anchor)### GROUPS


class HCorrDoor:
    def __init__(self, game, pos, *groups, anchor="topleft"):
        VDoorSmall(game, pos, *groups, anchor=anchor) ### GROUPS



def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()