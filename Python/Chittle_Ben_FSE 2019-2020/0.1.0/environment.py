import pygame as pg
#pg.init()


class Wall(pg.sprite.Sprite):
    instances = pg.sprite.Group()

    def __init__(self, sprites, x, y, width, height, colour):
        super().__init__(Wall.instances)
        self.sprites = sprites

        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.image.fill(colour)
        #self.image = pg.transform.rotate(self.image, 30)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        pass


class MovingWall(Wall):
    def __init__(self, sprites, x, y, width, height, colour):
        super().__init__(sprites, x, y, width, height, colour)
        self.speed = -4

    def update(self):
        if self.rect.y < 0 or self.rect.y > 700:
            self.speed = -self.speed

        self.rect.y += self.speed

class Target(pg.sprite.Sprite):
    instances = pg.sprite.Group()

    def __init__(self, sprites, x, y, width, height, colour):
        super().__init__(Target.instances)
        self.sprites = sprites

        self.max_shield = 25
        self.shield = self.max_shield
        self.recharge_rate = 0.2
        self.recharge_delay = 3000
        self.last_hit_time = pg.time.get_ticks()
        self.health = 25

        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        now = pg.time.get_ticks()
        if self.shield < self.max_shield:
            if now - self.last_hit_time > self.recharge_delay:
                self.shield += self.recharge_rate

                if self.shield > self.max_shield:
                    self.shield = self.max_shield

        projectile_hits = pg.sprite.spritecollide(self, self.sprites["projectiles"], True)
        if projectile_hits:
            self.hit(projectile_hits[0])


    def hit(self, projectile):
        self.last_hit_time = pg.time.get_ticks()
        dmg = projectile.power
        if self.shield > 0:
            self.shield -= dmg

            if self.shield < 0:
                self.health += self.shield
                self.shield = 0
        else:
            self.health -= dmg

        if self.health <= 0:
            self.health = 0
            self.kill()






def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()