import pygame as pg
import math
#https://www.pygame.org/docs/ref/rect.html


class Player(pg.sprite.Sprite):
    def __init__(self, screen, x, y):
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
        self.rect = pg.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))

        self.ACCEL_SPEED = 0.05
        self.FRICTION = 0.01
        self.MAX_SPEED = 6
        self.SLOW_THRESHOLD = 0.1


    def update(self, wallGroup):
        keys = pg.key.get_pressed()

        '''
        oldVelx = self.velx
        oldVely = self.vely

        if keys[pg.K_a] and self.x > 0:
            self.velx -= self.SPEED
        if keys[pg.K_d] and self.x < 1900:
            self.velx += self.SPEED
        if keys[pg.K_s] and self.y < 1020:
            self.vely += self.SPEED
        if keys[pg.K_w] and self.y > 0:
            self.vely -= self.SPEED
        '''
        self.deltaVelx = 0
        self.deltaVely = 0

        if keys[pg.K_a]:
            self.deltaVelx = -self.ACCEL_SPEED
        if keys[pg.K_d]:
            self.deltaVelx = self.ACCEL_SPEED
        if keys[pg.K_s]:
            self.deltaVely = self.ACCEL_SPEED
        if keys[pg.K_w]:
            self.deltaVely = -self.ACCEL_SPEED
        if keys[pg.K_r]:
            self.x = 50
            self.y = 50
            self.velx = 0
            self.vely = 0

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

        #self.rect = pg.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))
        self.x += self.velx
        self.rect = pg.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))
        for wall in wallGroup:
            if pg.sprite.collide_rect(self, wall):
                self.x -= self.velx
                self.velx = 0
                break
        #self.rect = pg.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))
        self.y += self.vely
        self.rect = pg.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))
        for wall in wallGroup:
            if pg.sprite.collide_rect(self, wall):
                self.y -= self.vely
                self.vely = 0
                break
        #self.rect = pg.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))


        '''
            self.x -= self.velx
            if not pg.sprite.collide_rect(self, wall):
               # print("X")
                self.x += 2 * self.velx
                #self.velx = 0
            self.y -= self.vely
            if not pg.sprite.collide_rect(self, wall):
               # print("Y")
                self.y += 2 * self.vely
                #self.vely = 0

        #self.x += self.velx
        #self.y += self.vely
'''



        self.rect = pg.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.WIDTH, self.HEIGHT))

        '''
        if 500 <= self.x <= 550:
            if 0 <=self. y <= 1000:
                if 500 <= (self.x - movex) <= 550:
                    self.y -= moveY
                elif 0 <= (self.y - moveY) <= 1000:
                    self.x -= movex
        '''
    def draw(self):
        return self.rect

    def collide(self, spriteGroup): # SPECIFICALLY FOR WALL CLASS ONLY
        pass

        """
        for sprite in spriteGroup:
            if pg.sprite.collide_rect(self, sprite):
                if sprite.rotation == 90:
                    self.velx = -self.velx
                elif sprite.rotation == 0:
                    self.vely = -self.vely
                else:
                    print("collision issue bois")
        """


def main():
    test = Player(None, 50, 50)

if __name__ == "__main__":
    main()