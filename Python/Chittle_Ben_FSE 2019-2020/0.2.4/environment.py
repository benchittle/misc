import random
import pygame as pg
import config


class Block(pg.sprite.Sprite):
    def __init__(self, game, pos, dimensions, anchor="topleft", groups=()):
        super().__init__(game.all_sprites, *groups)
        self.game = game

        self.pos = pg.Vector2(pos)
        self.colour = [255] + [random.randint(0, 255) for i in range(2)]
        random.shuffle(self.colour)
        self.anchor = anchor

        self.image = pg.Surface(dimensions)#, pg.SRCALPHA)
        self.image.fill(self.colour)
        #self.image = pg.transform.rotate(self.image, 30)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.pos - self.game.dp_pos)


    def update(self):
       setattr(self.rect, self.anchor, self.pos - self.game.dp_pos)


    def copy(self, keep_anchors=True):
        anchor = self.anchor if keep_anchors else "topleft"
        return Block(self.game, self.pos, (self.rect.w, self.rect.h), anchor, self.groups())


    def split(self, gap, axis): #use getattr?
        if axis == "x": #vertical
            size = (self.rect.w, (self.rect.h - gap) // 2)
            wall1 = Block(self.game, self.rect.topleft + self.game.dp_pos, size, groups=self.groups())
            wall2 = wall1.copy()
            wall2.pos.y = self.rect.bottom + self.game.dp_pos.y - wall1.rect.h

        elif axis == "y":
            size = ((self.rect.w - gap) // 2, self.rect.h)
            wall1 = Block(self.game, self.rect.topleft + self.game.dp_pos, size, groups=self.groups())
            wall2 = wall1.copy()
            wall2.pos.x = self.rect.right + self.game.dp_pos.x - wall1.rect.w

        return wall1, wall2


class Composite(pg.sprite.Group):
    def __init__(self, game, pos, anchor):
        super().__init__()
        self.game = game
        self.pos = pg.Vector2(pos)
        self.anchor = anchor



class VWall(Block):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, (config.WALL_WIDTH, config.TILE_SIZE), anchor, groups)


class HWall(Block):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, (config.TILE_SIZE, config.WALL_WIDTH), anchor, groups)


class VDoorSmall(Block):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, (config.WALL_WIDTH, config.DOOR_SIZE), anchor, groups)


class HDoorSmall(Block):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, (config.DOOR_SIZE, config.WALL_WIDTH), anchor, groups)


class VWallDoor(Composite):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, anchor)
        temp_wall = Block(self.game, self.pos, (config.WALL_WIDTH, config.TILE_SIZE), self.anchor)
        for piece in temp_wall.split(config.DOOR_SIZE, "x"):
            self.add(piece)
            for group in groups:
                group.add(piece)

        temp_wall.kill()


class HWallDoor(Composite):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, anchor)
        temp_wall = Block(self.game, self.pos, (config.TILE_SIZE, config.WALL_WIDTH), self.anchor)
        for piece in temp_wall.split(config.DOOR_SIZE, "y"):
            self.add(piece)
            for group in groups:
                group.add(piece)

        temp_wall.kill()


class VCorr(Composite):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, anchor)
        bound_size = (config.DOOR_SIZE + 2 * config.WALL_WIDTH, (config.TILE_SIZE - config.DOOR_SIZE) // 2)
        temp_wall = Block(self.game, self.pos, bound_size, self.anchor)#, groups=(self.game.walls))
        self.rect = temp_wall.rect

        for piece in temp_wall.split(config.DOOR_SIZE, "y"):
            self.add(piece)
            for group in groups:
                group.add(piece)

        temp_wall.kill()


class HCorr(Composite):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, anchor)
        bound_size = ((config.TILE_SIZE - config.DOOR_SIZE) // 2, config.DOOR_SIZE + 2 * config.WALL_WIDTH)
        temp_wall = Block(self.game, self.pos, bound_size, self.anchor)
        self.rect = temp_wall.rect

        for piece in temp_wall.split(config.DOOR_SIZE, "x"):
            self.add(piece)
            for group in groups:
                group.add(piece)

        temp_wall.kill()


class VCorrDoor(Composite):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, anchor)
        HDoorSmall(self.game, self.pos, anchor=self.anchor, groups=(self, self.game.walls))### GROUPS


class HCorrDoor(Composite):
    def __init__(self, game, pos, anchor="topleft", groups=()):
        super().__init__(game, pos, anchor)
        VDoorSmall(self.game, self.pos, anchor=self.anchor, groups=(self, self.game.walls)) ### GROUPS





def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()