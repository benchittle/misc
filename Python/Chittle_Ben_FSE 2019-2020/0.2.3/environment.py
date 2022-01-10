import random
import pygame as pg
import config


class Wall(pg.sprite.Sprite):
    def __init__(self, game, pos, dimensions, anchor="topleft"):
        super().__init__(game.all_sprites, game.walls)
        self.game = game

        self.pos = pg.Vector2(pos)
        self.colour = [255] + [random.randint(0, 255) for i in range(2)]
        random.shuffle(self.colour)
        self.anchor = anchor

        self.image = pg.Surface(dimensions)#, pg.SRCALPHA)
        self.image.fill(self.colour)
        #self.image = pg.transform.rotate(self.image, 30)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.pos)


    def update(self):
       setattr(self.rect, self.anchor, self.pos - self.game.dp_pos)

    def copy(self):
        return Wall(self.game, tuple(self.pos), (self.rect.w, self.rect.h), self.anchor)

    def union(self, wall):
        self.update()
        wall.update()
        new_rect = self.rect.union(wall.rect)
        self.kill()
        wall.kill()
        return Wall(self.game, self.pos, new_rect.size, self.anchor)


    def split(self, gap): #use getattr?
        if self.rect.h > self.rect.w: #vertical
            self.rect.h = (self.rect.h - gap) / 2
            wall1 = self.copy()
            wall2 = wall1.copy()
            wall2.pos.y += self.rect.h + gap


        elif self.rect.w > self.rect.h:
            self.rect.w = (self.rect.w - gap) / 2
            wall1 = self.copy()
            wall2 = wall1.copy()
            wall2.pos.x += self.rect.w + gap# + 100

        self.kill()

        return wall1, wall2 #{"-" : wall1, "+" : wall2}



class VWall(Wall):
    def __init__(self, game, pos, length, anchor="topleft"):
        super().__init__(game, pos, (config.WALL_WIDTH, length), anchor)


class HWall(Wall):
    def __init__(self, game, pos, length, anchor="topleft"):
        super().__init__(game, pos, (length, config.WALL_WIDTH), anchor)








def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()