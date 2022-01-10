import math, gc
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
        self.rect = pg.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

class Target(pg.sprite.Sprite):
    instances = pg.sprite.Group()

    def __init__(self, screen, x, y, screenh):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.vel = 3
        self.WIDTH = 10
        self.HEIGHT = 50
        self.SCREENH = screenh
        Target.instances.add(self)
        self.rect = pg.draw.rect(self.screen, (0, 0, 255), (self.x, self.y, self.WIDTH, self.HEIGHT))

    def update(self):
        if self.y > self.SCREENH - 10:
            self.vel = -5
        elif self.y < 10:
            self.vel = 5

        self.y += self.vel




    def draw(self):
        self.rect = pg.draw.rect(self.screen, (0, 0, 255), (self.x, self.y, self.WIDTH, self.HEIGHT))




SCREENW = 1260
SCREENH = 720

screen = pg.display.set_mode((SCREENW, SCREENH))
pg.display.set_caption("Testing all Systems...")
clock = pg.time.Clock()

tempFont = pg.font.SysFont("Comic Sans MS", 20)

width = 0.1 * SCREENW
height = 0.8 * SCREENH

x1 = 0.2 * SCREENW
y1 = 0

x2 = 0.6 * SCREENW
y2 = 50




wall1 = Wall(screen, x1, y1, width, height, 90)
leftBound = Wall(screen, 0, 0, 1, SCREENH, 90)
rightBound = Wall(screen, SCREENW, 0, 1, SCREENH, 90)
upBound = Wall(screen, 0, 0, SCREENW, 1, 0)
lowBound = Wall(screen, 0, SCREENH, SCREENW, 1, 0)
wallGroup = pg.sprite.Group()
wallGroup.add([wall1, leftBound, rightBound, upBound, lowBound])

player = PlayerClassTest.Player(screen, 5, 5, wallGroup, Target.instances)



run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if event.type == pg.KEYDOWN and event.key == pg.K_p:
            for i in range(7500):
                Target(screen, 0.75 * SCREENW, 10, SCREENH)
        '''
        if event.type == pg.KEYDOWN and event.key == pg.K_l:
            for i in tst:
                del i
                '''
        if event.type == pg.KEYDOWN and event.key == pg.K_k:
            c = 0
            for obj in gc.get_objects():
                c += 1
            print(c)



        #print(event)

    screen.fill((0, 0, 0))

    velText = tempFont.render("Velocity: {:.3f}[~{}]".format(player.speed, player.direction), False, (255, 255, 255))
    bulletCount = tempFont.render("Bullets: {} Sprites: {}".format(len(PlayerClassTest.Bullet.instances), len(Target.instances)), False, (255, 255, 255))
    screen.blit(velText, (0, 0))
    screen.blit(bulletCount, (0, 20))

    #wall1.draw()
    #pg.draw.circle(screen, (255, 0, 0), (400, 400), 50)
    for wall in wallGroup:
        wall.draw()
    player.update()
    player.draw()

    for trgt in Target.instances:
        trgt.update()
        trgt.draw()

    for shot in PlayerClassTest.Bullet.instances:
        shot.update()


    #pg.sprite.spritecollide(trgt1, pg.sprite.Group(PlayerClassTest.Bullet.instances), True)

    #print(len(PlayerClassTest.Bullet.instances))

    #player.collide(wallGroup)

    #r2 = pg.draw.rect(screen, (255, 0, 0), (x2, y2, width, height))





    pg.display.update()
    clock.tick(100)

pg.quit()
print("Done!")
