import math
import pygame as pg
from settings import *


#pg.init() # Necessary?

class Player(pg.sprite.Sprite):
    def __init__(self, game, data):
        super().__init__(game.all_sprites)
        self.game = game

        '''## USE SET ATTR OR SOMETHING TO AUTOMATE THIS PROCESS
        for attr, field in data.items():
            setattr(self, attr, field)'''

        self.pos = pg.Vector2(data["pos"])
        self.vel = pg.Vector2(data["vel"])

        self.last_shot_time = pg.time.get_ticks()

        self.width = 30 ##
        self.height = 30 ##
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def update(self):
        mouse = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()

        if mouse[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot_time > 100:
                self.shoot()
                self.last_shot_time = now
        if keys[pg.K_a]:
            self.vel.x -= PLAYER_ACCEL
        if keys[pg.K_d]:
            self.vel.x += PLAYER_ACCEL
        if keys[pg.K_s]:
            self.vel.y += PLAYER_ACCEL
        if keys[pg.K_w]:
            self.vel.y -= PLAYER_ACCEL

        self.update_position()


    def update_position(self):
        if self.vel.magnitude() > PLAYER_MAX_SPEED:
            self.vel.scale_to_length(PLAYER_MAX_SPEED)
        if self.vel.magnitude() > 0:
            self.vel -= self.vel * PLAYER_FRICTION
        if abs(self.vel.x) < PLAYER_MIN_VEL:
            self.vel.x = 0
        if abs(self.vel.y) < PLAYER_MIN_VEL:
            self.vel.y = 0

        self.rect.x += self.vel.x
        for wall in pg.sprite.spritecollide(self, self.game.walls, False):
            if self.vel.x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right
            self.vel.x = 0

        self.rect.y += self.vel.y
        for wall in pg.sprite.spritecollide(self, self.game.walls, False):
            if self.vel.y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom
            self.vel.y = 0

        self.pos.update(self.game.dp_pos + self.rect.center)
        self.game.dp_pos.update(self.pos - (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.rect.center = self.pos - self.game.dp_pos


    def shoot(self):
        mpos = pg.Vector2(pg.mouse.get_pos())
        if mpos != self.pos:
            Projectile(self.game, self.pos * 1, mpos - self.rect.center)




class Projectile(pg.sprite.Sprite):
    def __init__(self, game, pos, vector):
        super().__init__(game.all_sprites, game.projectiles)
        self.game = game

        self.speed = 16
        self.power = 5
        self.range = 5000
        self._number_of_checks = 2

        self.pos = pos
        self.vel = vector
        self.vel.scale_to_length(self.speed)

        self.width = 10
        self.length = 10
        self.image = pg.Surface((self.width, self.length))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.game.dp_pos


    def update(self):
        for i in range(self._number_of_checks):
            self.pos += self.vel / self._number_of_checks
            self.rect.center = self.pos - self.game.dp_pos

            if pg.sprite.spritecollide(self, self.game.walls, False):
                self.kill()

        if self.pos.distance_to(self.game.player.pos) > self.range:
            self.kill()






def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()
