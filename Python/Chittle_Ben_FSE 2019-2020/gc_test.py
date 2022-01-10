import gc
import pygame as pg
pg.init()


SCREENW = 1260
SCREENH = 720

screen = pg.display.set_mode((SCREENW, SCREENH))
pg.display.set_caption("Testing all Systems...")
clock = pg.time.Clock()


class Block(pg.sprite.Sprite):
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.rect = pg.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, 40, 40))

    def update(self):
        pass

    def draw(self):
        self.rect = pg.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, 40, 40))


tst = []
t = None
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.KEYDOWN and event.key == pg.K_p:
            for i in range(10000):
                tst.append(Block(screen, 500, 300))

        if event.type == pg.KEYDOWN and event.key == pg.K_l:
            tst = []
            gc.collect()



    screen.fill((0, 0, 0))



    pg.display.update()
    clock.tick(100)

pg.quit()
print("Done!")