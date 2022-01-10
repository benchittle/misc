"""
Date: May 2, 2020
Version: 0.4.1
Added:
    >SentryBlaster

Removed:

Changed:

"""

import random
import pygame as pg
import config, sprites



class Item(pg.sprite.Sprite):
    """Template for creating item classes."""
    def __init__(self, lvldata):
        super().__init__(lvldata.ground_items)
        self._is_on_ground = True
        self._is_hidden = False
        self.layer = config.ITEM_LAYER


    @property
    def is_on_ground(self):
        return self._is_on_ground


    @is_on_ground.setter
    def is_on_ground(self, value):
        self._is_on_ground = value
        # Reconfigure the item if it was dropped.
        if self.is_on_ground:
            self.lvldata.ground_items.add(self)
            self.layer = config.ITEM_LAYER
            self.is_hidden = False
        # Reconfigure the item if it was picked up.
        else:
            self.lvldata.ground_items.remove(self)
            self.layer = config.SPRITE_LAYER

    @property
    def is_hidden(self):
        return self._is_hidden


    @is_hidden.setter
    def is_hidden(self, value):
        self._is_hidden = value
        # Reconfigure the item if it should hide.
        if self.is_hidden:
            self.lvldata.all_sprites.remove(self)
        # Reconfigure the item if it should show.
        else:
            self.lvldata.all_sprites.add(self, layer=self.layer)



class HandBlaster(Item):
    size = (15, 5)
    cooldown = 10

    def __init__(self, lvldata, pos, shot, rotation=0, colour=config.RED):
        super().__init__(lvldata)
        self.lvldata = lvldata
        self.lvldata.all_sprites.add(self, layer=config.ITEM_LAYER)

        self.pos = pg.Vector2(pos)
        self.rotation = rotation

        self.colour = colour ##
        self.image_base = pg.Surface(self.size, pg.SRCALPHA)
        self.image_base.fill(self.colour)
        self.image = pg.transform.rotate(self.image_base, self.rotation)
        self.rect = self.image.get_rect(center = self.pos - self.lvldata.screen_pos)

        self.last_shot_time = pg.time.get_ticks()
        self.shot = shot


    @classmethod
    def from_owner(cls, owner, shot):
        instance = cls(owner.lvldata, owner.pos, shot, owner.rotation)
        instance.is_on_ground = False
        return instance


    def update(self):
        if not self.is_hidden:
            self.rect = self.image.get_rect(center=self.pos - self.lvldata.screen_pos)


    def action(self, trajectory):
        self.last_shot_time = pg.time.get_ticks()
        self.shot(self.lvldata, self.pos, trajectory, self.colour)



class SentryBlaster(Item):
    size = (config.SENTRY_SIZE, config.SENTRY_SIZE // 4)
    cooldown = 100
    inaccuracy = 10

    def __init__(self, lvldata, pos, rotation=0, colour=config.ORANGE):
        super().__init__(lvldata)
        self.lvldata = lvldata
        self.lvldata.all_sprites.add(self, layer=config.SPRITE_LAYER_FRONT)

        self.pos = pos
        self.rotation = rotation

        self.colour = colour ##
        self.image_base = pg.Surface(self.size, pg.SRCALPHA)
        self.image_base.fill(self.colour)
        self.image = pg.transform.rotate(self.image_base, self.rotation)
        self.rect = self.image.get_rect(center=self.pos - self.lvldata.screen_pos)

        self.last_shot_time = 0


    def update(self):
        if not self.is_hidden:
            self.rect = self.image.get_rect(center=self.pos - self.lvldata.screen_pos)


    def action(self):
        self.last_shot_time = pg.time.get_ticks()
        trajectory = ((self.lvldata.player.pos - self.pos).normalize().elementwise()
                      + random.randint(-self.inaccuracy, self.inaccuracy) / 100)
        RegularShot(self.lvldata, self.pos, trajectory, self.colour)




class BouncyShot(sprites.ShipSprite):
    size = 4
    speed = 12
    power = 5
    max_range = 5000
    max_bounces = 10
    number_of_checks = 1

    def __init__(self, lvldata, pos, trajectory, colour=config.RED):
        super().__init__()
        self.lvldata = lvldata
        self.lvldata.all_sprites.add(self, layer=config.PROJECTILE_LAYER)
        self.add(self.lvldata.projectiles)

        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(trajectory)
        self.vel.scale_to_length(self.speed)

        self.image = pg.Surface((self.size, self.size))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.lvldata.screen_pos
        self.tiles = self.lvldata.ship.locate_sprite(self)

        self.bounces = 0


    def update(self):
        self.update_position()
        if self.pos.distance_to(self.lvldata.player.pos) > self.max_range:
            self.kill()


    def update_position(self):
        if self.bounces < self.max_bounces:
            for i in range(self.number_of_checks):
                dx = self.vel.x / self.number_of_checks
                self.pos.x += dx
                self.rect.centerx = self.pos.x - self.lvldata.screen_pos.x
                self.tiles = pg.sprite.spritecollide(self, self._tiles_to_check, False)
                if pg.sprite.spritecollideany(self, self._walls_to_check, False): ##
                    self.pos.x -= dx
                    self.vel.x *= -1
                    self.rect.centerx = self.pos.x - self.lvldata.screen_pos.x
                    self.bounces += 1

                dy = self.vel.y / self.number_of_checks
                self.pos.y += dy
                self.rect.centery = self.pos.y - self.lvldata.screen_pos.y
                self.tiles = pg.sprite.spritecollide(self, self._tiles_to_check, False) ##
                if pg.sprite.spritecollideany(self, self._walls_to_check, False): ##
                    self.pos.y -= dy
                    self.vel.y *= -1
                    self.rect.centery = self.pos.y - self.lvldata.screen_pos.y
                    self.bounces += 1
        else:
            self.kill()



class RegularShot(sprites.ShipSprite):
    size = 6
    speed = 20
    power = 5
    max_range = 5000
    number_of_checks = 1

    def __init__(self, lvldata, pos, trajectory, colour=config.ORANGE):
        super().__init__()
        self.lvldata = lvldata

        self.lvldata.all_sprites.add(self, layer=config.PROJECTILE_LAYER)
        self.add(self.lvldata.projectiles)

        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(trajectory)
        self.vel.scale_to_length(self.speed)

        self.image = pg.Surface((self.size, self.size))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.lvldata.screen_pos
        self.tiles = self.lvldata.ship.locate_sprite(self)


    def update(self):
        self.update_position()
        if self.pos.distance_to(self.lvldata.player.pos) > self.max_range:
            self.kill()


    def update_position(self):
        for i in range(self.number_of_checks):
            self.pos += self.vel / self.number_of_checks
            self.rect.center = self.pos - self.lvldata.screen_pos
            self.tiles = pg.sprite.spritecollide(self, self._tiles_to_check, False)
            if pg.sprite.spritecollideany(self, self._walls_to_check, False):
                self.kill()






class PlasmaRailCannon:
    pass


def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()
