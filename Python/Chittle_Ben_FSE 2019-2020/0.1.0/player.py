import math
import pygame as pg


#pg.init() # Necessary?

class Player(pg.sprite.Sprite):
    instances = pg.sprite.Group()
    def __init__(self, sprites, x, y, motion):
        super().__init__(Player.instances)
        self.sprites = sprites

        self.friction = motion["friction"]
        self.accel = motion["accel"]
        self.max_speed = motion["max_speed"]
        self.slow_threshold = motion["slow_threshold"]
        self.velx = 0
        self.vely = 0
        self.last_shot_time = pg.time.get_ticks()

        self.width = 30 ##
        self.height = 30 ##
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        mouse = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()

        if mouse[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot_time > 100:
                self.shoot()
                self.last_shot_time = now
        if keys[pg.K_a]:
            self.velx -= self.accel
        if keys[pg.K_d]:
            self.velx += self.accel
        if keys[pg.K_s]:
            self.vely += self.accel
        if keys[pg.K_w]:
            self.vely -= self.accel

        self.update_position()


    def update_position(self):
        if self.speed > self.max_speed:
            ratio = 1 - (self.speed - self.max_speed) / self.max_speed
            self.velx *= ratio
            self.vely *= ratio
        if self.speed > 0:
            self.velx -= self.velx * self.friction
            self.vely -= self.vely * self.friction
        if self.speed < self.slow_threshold:
            self.velx = 0
            self.vely = 0

        self.rect.x += self.velx
        for wall in pg.sprite.spritecollide(self, self.sprites["walls"], False):
            if self.velx > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right
            self.velx = 0

        self.rect.y += self.vely
        for wall in pg.sprite.spritecollide(self, self.sprites["walls"], False):
            if self.vely > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

            self.vely = 0


    @property
    def speed(self):
        return math.hypot(self.velx, self.vely)

    def shoot(self):
        mx, my = pg.mouse.get_pos()
        dx = mx - self.rect.x
        dy = my - self.rect.y
        if not (dx == dy == 0):
            hypot = math.hypot(dx, dy)

            Projectile(
                sprites=self.sprites,
                x=self.rect.x,
                y=self.rect.y,
                xvel=20 * dx / hypot,
                yvel=20 * dy / hypot
                )




class Projectile(pg.sprite.Sprite):
    instances = pg.sprite.Group()

    def __init__(self, sprites, x, y, xvel, yvel):
        super().__init__(Projectile.instances)
        self.sprites = sprites

        self.power = 5

        self.velx = xvel
        self.vely = yvel
        self.x = x
        self.y = y

        self.width = 10
        self.length = 10
        self.image = pg.Surface((self.width, self.length))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        #self.oldx = self.x
        #self.oldy = self.y

        for i in range(2):
            self.x += self.velx * 0.5
            self.y += self.vely * 0.5
            self.rect.x = self.x
            self.rect.y = self.y

            if pg.sprite.spritecollide(self, self.sprites["walls"], False):
                self.kill()





def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()




'''
        m = (self.vely) / (self.velx)
        b = self.y - m * self.x

        for wall in self.sprites["walls"]:
            walldx = wall.rect.bottom - wall.rect.top
            walldy = wall.rect.right - wall.rect.left
            if walldx == 0:
                self.xi = wall.rect.x
                self.yi = m * self.xi + b
            elif walldy == 0:
                self.yi = wall.rect.y
                self.xi = (self.yi - b) / m
            else:
                wallm = walldy / walldx
                wallb = wall.rect.y - wallm * wall.rect.x
                self.xi = (b - wallb) / (wallm - m)
                self.yi = m * self.xi + b
'''

'''
        lowx, highx = (self.oldx, self.x) if self.oldx < self.x else (self.x, self.oldx)
        lowy, highy = (self.oldy, self.y) if self.oldy < self.y else (self.y, self.oldy)

        if lowx <= self.xi <= highx:
            if lowy <= self.yi <= highy:
                self.kill()
'''
