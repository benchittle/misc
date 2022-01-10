import math
import pygame as pg
import PlayerClassTest

pg.init()
pg.font.init()

class Wall(pg.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, rotation):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.rect = pg.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def draw(self):
        return pg.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height))


screen = pg.display.set_mode((1920, 1080))
pg.display.set_caption("Testing all Systems...")
clock = pg.time.Clock()

tempFont = pg.font.SysFont("Comic Sans MS", 20)

player = PlayerClassTest.Player(screen, 50, 50)

width = 500
height = 750

x1 = 500
y1 = 0

x2 = 565
y2 = 5

wall1 = Wall(screen, x1, y1, width, height, 90)
wallGroup = pg.sprite.Group()
wallGroup.add(wall1)




run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False

        #print(event)

    screen.fill((0, 0, 0))

    textSurface = tempFont.render("Speed: {}".format(player.speed), False, (255, 255, 255))
    screen.blit(textSurface, (0, 0))

    wall1.draw()
    player.update(wallGroup)
    player.draw()

    #player.collide(wallGroup)

    #r2 = pg.draw.rect(screen, (255, 0, 0), (x2, y2, width, height))





    pg.display.update()
    clock.tick(100)

pg.quit()
print("Done!")