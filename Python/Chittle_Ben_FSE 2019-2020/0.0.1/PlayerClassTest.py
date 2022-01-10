import pygame as pg
import math
#https://www.pygame.org/docs/ref/rect.html

class Bullet(pg.sprite.Sprite):
    instances = pg.sprite.Group()

    def __init__(self, screen, x, y, wallGroup, trgtGroup, direction, vel_i):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.vel = 5 + vel_i
        self.direction = direction
        if self.direction == "N" or self.direction == "S":
            self.WIDTH = 5
            self.HEIGHT = 15
        else:
            self.WIDTH = 15
            self.HEIGHT = 5
        self.rect = pg.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))
        self.wallGroup = wallGroup
        self.trgtGroup = trgtGroup

        Bullet.instances.add([self])


    def update(self):
        if self.direction == "E":
            self.x += self.vel
        elif self.direction == "W":
            self.x -= self.vel
        elif self.direction == "N":
            self.y -= self.vel
        elif self.direction == "S":
            self.y += self.vel

        self.draw()
        pg.sprite.spritecollide(self, self.trgtGroup, True)

        if pg.sprite.spritecollide(self, self.wallGroup, False):
            Bullet.instances.remove(self)
            del self



    def draw(self):
        self.rect = pg.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))


class Player(pg.sprite.Sprite):
    def __init__(self, screen, x, y, wallGroup, trgtGroup):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
        self.deltaVelx = 0
        self.deltaVely = 0
        self.speed = 0
        self.WIDTH = 20
        self.HEIGHT = 60
        self.wallGroup = wallGroup
        self.trgtGroup = trgtGroup
        self.lastShotTime = 0
        self.rect = pg.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))
        self.direction = "E"

        self.ACCEL_SPEED = 0.2
        self.FRICTION = 0.05
        self.MAX_SPEED = 6
        self.SLOW_THRESHOLD = 0.1


    def update(self):
        keys = pg.key.get_pressed()

        self.deltaVelx = 0
        self.deltaVely = 0

        if keys[pg.K_a]:
            self.deltaVelx = -self.ACCEL_SPEED
            self.direction = "W"
        if keys[pg.K_d]:
            self.deltaVelx = self.ACCEL_SPEED
            self.direction = "E"
        if keys[pg.K_s]:
            self.deltaVely = self.ACCEL_SPEED
            self.direction = "S"
        if keys[pg.K_w]:
            self.deltaVely = -self.ACCEL_SPEED
            self.direction = "N"
        if keys[pg.K_r]:
            self.x = 50
            self.y = 50
            self.velx = 0
            self.vely = 0
        if keys[pg.K_f]:
            if pg.time.get_ticks() - self.lastShotTime > 100:
                self.lastShotTime = pg.time.get_ticks()
                self.shoot()

        self.speed = math.hypot(self.velx + self.deltaVelx, self.vely + self.deltaVely)
        if self.speed < self.MAX_SPEED:
            self.velx += self.deltaVelx
            self.vely += self.deltaVely

        if self.speed < self.SLOW_THRESHOLD and self.deltaVelx == self.deltaVely == 0:
            self.velx = self.vely = 0

        if abs(self.velx) > 0:
            self.velx -= self.FRICTION * self.velx
        if abs(self.vely) > 0:
            self.vely -= self.FRICTION * self.vely

        self.x += self.velx
        self.draw()
        for wall in self.wallGroup:
            if pg.sprite.collide_rect(self, wall):
                self.x -= self.velx
                self.velx = 0
                break
        self.y += self.vely
        self.draw()
        for wall in self.wallGroup:
            if pg.sprite.collide_rect(self, wall):
                self.y -= self.vely
                self.vely = 0
                break
        self.draw()


    def draw(self):
        self.rect = pg.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))

    def shoot(self):
        for i in range(1000):
            Bullet(self.screen, self.x + 0.5 * self.WIDTH, self.y + 0.5 * self.HEIGHT, self.wallGroup, self.trgtGroup, self.direction, self.speed)

    def collide(self, spriteGroup): # SPECIFICALLY FOR WALL CLASS ONLY
        pass


def main():
    test = Player(None, 50, 50)

if __name__ == "__main__":
    main()
