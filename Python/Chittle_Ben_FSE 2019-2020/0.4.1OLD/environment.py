"""
Date: April 27, 2020
Version: 0.4.0
Added:

Removed:

Changed:

"""



import random
import pygame as pg
import config


class Block(pg.sprite.Sprite):
    def __init__(self, lvldata, pos, dimensions, *groups, anchor="topleft"):
        super().__init__()
        self.lvldata = lvldata
        self.lvldata.all_sprites.add(self, layer=config.SPRITE_LAYER)
        self.add(*groups)

        self.pos = pg.Vector2(pos)
        self.colour = config.WALL_COLOUR
        self.anchor = anchor

        self.image = pg.Surface(dimensions)
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.pos - self.lvldata.screen_pos)


    def __repr__(self):
        return "{}".format(self.rect)


    def update(self):
       setattr(self.rect, self.anchor, self.pos - self.lvldata.screen_pos)


    def copy(self, keep_anchors=True):
        anchor = self.anchor if keep_anchors else "topleft"
        return Block(self.lvldata, self.pos, (self.rect.w, self.rect.h), *self.groups(), anchor=anchor)


    def split(self, gap, axis, kill=True):
        if axis == "x": #vertical
            size = (self.rect.w, (self.rect.h - gap) // 2)
            wall1 = Block(self.lvldata, self.rect.topleft + self.lvldata.screen_pos, size, *self.groups())
            wall2 = wall1.copy()
            wall2.pos.y = self.rect.bottom + self.lvldata.screen_pos.y - wall1.rect.h
        elif axis == "y":
            size = ((self.rect.w - gap) // 2, self.rect.h)
            wall1 = Block(self.lvldata, self.rect.topleft + self.lvldata.screen_pos, size, *self.groups())
            wall2 = wall1.copy()
            wall2.pos.x = self.rect.right + self.lvldata.screen_pos.x - wall1.rect.w
        if kill:
            self.kill()

        return wall1, wall2



def VWall(lvldata, pos, *groups, anchor="topleft"):
    Block(lvldata, pos, (config.WALL_WIDTH, config.TILE_SIZE), *groups, anchor=anchor)


def HWall(lvldata, pos, *groups, anchor="topleft"):
    Block(lvldata, pos, (config.TILE_SIZE, config.WALL_WIDTH), *groups, anchor=anchor)


def VDoorSmall(lvldata, pos, *groups, anchor="topleft"):
    Block(lvldata, pos, (config.WALL_WIDTH, config.DOOR_SIZE + 2 * config.WALL_WIDTH), *groups, anchor=anchor)


def HDoorSmall(lvldata, pos, *groups, anchor="topleft"):
    Block(lvldata, pos, (config.DOOR_SIZE + 2 * config.WALL_WIDTH, config.WALL_WIDTH), *groups, anchor=anchor)


def VWallDoor(lvldata, pos, *groups, anchor="topleft"):
    temp_wall = Block(lvldata, pos, (config.WALL_WIDTH, config.TILE_SIZE), anchor=anchor)
    for piece in temp_wall.split(config.DOOR_SIZE, "x"):
        for group in groups:
            group.add(piece)


def HWallDoor(lvldata, pos, *groups, anchor="topleft"):
    temp_wall = Block(lvldata, pos, (config.TILE_SIZE, config.WALL_WIDTH), anchor=anchor)
    for piece in temp_wall.split(config.DOOR_SIZE, "y"):
        for group in groups:
            group.add(piece)


def VCorr(lvldata, pos, *groups, anchor="topleft"):
    bound_size = (config.DOOR_SIZE + 2 * config.WALL_WIDTH, (config.TILE_SIZE - config.DOOR_SIZE) // 2)
    temp_wall = Block(lvldata, pos, bound_size, anchor=anchor)#, groups=(self.lvldata.walls))

    for piece in temp_wall.split(config.DOOR_SIZE, "y"):
        for group in groups:
            group.add(piece)


def HCorr(lvldata, pos, *groups, anchor="topleft"):
    bound_size = ((config.TILE_SIZE - config.DOOR_SIZE) // 2, config.DOOR_SIZE + 2 * config.WALL_WIDTH)
    temp_wall = Block(lvldata, pos, bound_size, anchor=anchor)

    for piece in temp_wall.split(config.DOOR_SIZE, "x"):
        for group in groups:
            group.add(piece)


def VCorrDoor(lvldata, pos, *groups, anchor="topleft"):
    HDoorSmall(lvldata, pos, *groups, anchor=anchor)### GROUPS


def HCorrDoor(lvldata, pos, *groups, anchor="topleft"):
    VDoorSmall(lvldata, pos, *groups, anchor=anchor) ### GROUPS



def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()