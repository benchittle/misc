import time, math
import pygame as pg
import config

def spritecollide_sub(sprite, sub, dokill):
    '''
    for quad_rect, tiles in sub.quadrants.items():
        if sprite.rect.colliderect(quad_rect):
            for tile in pg.sprite.spritecollide(sprite, tiles, False):
                walls.add(*tile.room.walls)'''
    '''
    quadrants = sprite.rect.collidelistall(sub.quadrant_rects)
    tiles = [tile for quad in quadrants for tile in sub.quadrant_tiles[quad]]
    walls = [wall for tile in tiles for wall in tile.room.walls]
'''
    walls = [wall for tile in pg.sprite.spritecollide(sprite, sub.tiles, False) for wall in tile.room.walls]
    collisions = pg.sprite.spritecollide(sprite, walls, dokill)
    return collisions


#pg.init() # Necessary?

class Player(pg.sprite.Sprite):
    size = 16
    hitbox_size = math.sqrt(2 * size ** 2)
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        #self.game.all_sprites.add(self, layer=config.SPRITE_LAYER)

        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2()

        self.collisions = True

        self.image_base = pg.Surface((self.size, self.size), pg.SRCALPHA)
        self.image_base.fill(config.GREEN)
        self.rect = pg.Rect(0, 0, self.hitbox_size, self.hitbox_size)
        self.rect.center = self.pos - self.game.screen_pos
        self.rotation = 0

        self.inventory = [None] * 9
        self.inventory[0] = HandBlaster.from_owner(self)
        self._equipped_item = 0
        self.equipped_item = 0


    @property
    def equipped_item(self):
        return self.inventory[self._equipped_item]


    @equipped_item.setter
    def equipped_item(self, index):
        if self.equipped_item is not None:
            self.equipped_item.is_active = False
        self._equipped_item = index
        if self.equipped_item is not None:
            self.equipped_item.is_active = True


    def pickup_item(self, item):
        try:
            self.inventory[self.inventory.index(None)] = item
            item.owner = self
            item.is_item = False

        except IndexError:
            print("Inventory full: item not picked up.")


    def update(self):
        mouse = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()

        num_keys = keys[pg.K_1:pg.K_9 + 1]
        if any(num_keys):
            self.equipped_item = num_keys.index(1)

        if mouse[0]:
            self.primary_action()
        #if keys[pg.K_e]:

        if keys[pg.K_a]:
            self.vel.x -= config.PLAYER_ACCEL
        if keys[pg.K_d]:
            self.vel.x += config.PLAYER_ACCEL
        if keys[pg.K_s]:
            self.vel.y += config.PLAYER_ACCEL
        if keys[pg.K_w]:
            self.vel.y -= config.PLAYER_ACCEL

        self.update_position()


    def update_position(self):
        self.rotation = (pg.Vector2(pg.mouse.get_pos()) - self.rect.center).angle_to((1, 0))
        self.image = pg.transform.rotate(self.image_base, self.rotation)

        if self.vel.magnitude() > config.PLAYER_MAX_SPEED:
            self.vel.scale_to_length(config.PLAYER_MAX_SPEED)
        if self.vel.magnitude() > 0:
            self.vel -= self.vel * config.PLAYER_FRICTION
        if abs(self.vel.x) < config.PLAYER_MIN_VEL:
            self.vel.x = 0
        if abs(self.vel.y) < config.PLAYER_MIN_VEL:
            self.vel.y = 0

        center = self.rect.center
        self.rect.size = (self.hitbox_size, self.hitbox_size)
        self.rect.center = center

        self.rect.x += self.vel.x
        if self.collisions:
            #t1 = time.clock()
            #c =
            #print(time.clock() - t1)
            for wall in spritecollide_sub(self, self.game.sub, False):
                if self.vel.x > 0:
                    self.rect.right = wall.rect.left
                elif self.vel.x < 0:
                    self.rect.left = wall.rect.right
                self.vel.x = 0

        self.rect.y += self.vel.y
        if self.collisions:
            for wall in spritecollide_sub(self, self.game.sub, False):
                if self.vel.y > 0:
                    self.rect.bottom = wall.rect.top
                elif self.vel.y < 0:
                    self.rect.top = wall.rect.bottom
                self.vel.y = 0

        self.pos.update(self.game.screen_pos + self.rect.center)
        self.game.screen_pos.update(self.pos - config.SCREEN_MID)
        self.rect = self.image.get_rect(center=self.pos - self.game.screen_pos)


    ### unnecessary?
    def primary_action(self):
        if self.equipped_item is not None:
            self.equipped_item.action()


class HandBlaster(pg.sprite.Sprite):
    size = (15, 5)
    cooldown = 100

    def __init__(self, game, pos, rotation):
        super().__init__()
        self.game = game

        self.owner = None
        self.pos = pg.Vector2(pos)
        self.rotation = rotation

        self.image_base = pg.Surface(self.size, pg.SRCALPHA)
        self.image_base.fill(config.RED)
        self.image = pg.transform.rotate(self.image_base, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.game.screen_pos
        #self._pos_offset = (self.owner.size / 2, self.owner.size / 2)

        self.last_shot_time = pg.time.get_ticks()
        self.is_active = True
        self.is_item = True


    @classmethod
    def from_owner(cls, owner):
        instance = cls(owner.game, owner.pos, owner.rotation)
        instance.owner = owner
        instance._pos_offset = (owner.size / 2, owner.size / 2)####
        instance.is_item = False
        return instance


    @property
    def is_item(self):
        return self._is_item

    @is_item.setter
    def is_item(self, value):
        self._is_item = value
        if self.is_item:
            self.game.items.add(self)
            self.owner = None
            self._pos_offset = 0
        else:
            self.game.items.remove(self)
            self._pos_offset = (self.owner.size / 2, self.owner.size / 2)


    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value
        if self.is_active:
            self.game.all_sprites.add(self, layer=config.SPRITE_LAYER)
            self.update()  ##
        else:
            self.game.all_sprites.remove(self)


    def update(self):
        if self.is_active:
            if self.owner is not None:
                self.move_to_owner()

            else:
                self.rect.center = self.pos - self.game.screen_pos


    def move_to_owner(self):
        # Sets the default position of the object (i.e. facing east) to be
        # at the owner's position with some offset so that it is placed at
        # the owner's side.
        self.pos = self.owner.pos + self._pos_offset

        # A vector describing the displacement from the radius, which the
        # object will be rotated about, to the object.
        radial_vector = self.pos - (self.game.screen_pos + self.owner.rect.center)

        # A vector describing the change in position as the radial vector is
        # rotated about the radius.
        self.change_vector = radial_vector.rotate(-(self.owner.rotation + 90)) - radial_vector

        # Applying the change in position.
        self.pos += self.change_vector

        # Applying the rotation to the image.
        self.image = pg.transform.rotate(self.image_base, self.owner.rotation)

        # Sets the rect's position to the new position.
        self.rect = self.image.get_rect(center=self.pos - self.game.screen_pos)


    def action(self):
        if pg.time.get_ticks() - self.last_shot_time > self.cooldown:
            mouse_pos = pg.Vector2(pg.mouse.get_pos())
            if mouse_pos.distance_to(self.owner.rect.center) > 20:
                BlasterShot(self, mouse_pos - self.rect.center)
                self.last_shot_time = pg.time.get_ticks()



class PlasmaRailCannon:
    pass



class BlasterShot(pg.sprite.Sprite):
    size = 6
    speed = 16
    power = 5
    max_range = 5000
    max_bounces = 500
    _number_of_checks = 2


    def __init__(self, blaster, trajectory):
        super().__init__()
        self.game = blaster.game
        self.blaster = blaster
        self.game.all_sprites.add(self, layer=config.PROJECTILE_LAYER)
        self.add(self.game.projectiles)

        #offset = self.blaster.change_vector * 1
        #offset.scale_to_length(self.blaster.change_vector.length() + 0)
        self.pos = self.blaster.pos
        self.vel = pg.Vector2(trajectory)
        self.vel.scale_to_length(self.speed)

        self.image = pg.Surface((self.size, self.size))
        self.image.fill(config.GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.game.screen_pos

        self.bounces = 0


    def update(self):
        self.update_position_bouncy()

        if self.pos.distance_to(self.game.player.pos) > self.max_range:
            self.kill()


    def update_position(self):
        for i in range(self._number_of_checks):
            self.pos += self.vel / self._number_of_checks
            self.rect.center = self.pos - self.game.screen_pos
            if spritecollide_sub(self, self.game.sub, False):
                self.kill()


    def update_position_bouncy(self):
        if self.bounces < self.max_bounces:
            for i in range(self._number_of_checks):
                self.pos.x += self.vel.x / self._number_of_checks
                self.rect.centerx = self.pos.x - self.game.screen_pos.x
                if spritecollide_sub(self, self.game.sub, False):
                    self.vel.x *= -1
                    self.pos.x += self.vel.x / self._number_of_checks
                    self.rect.centerx = self.pos.x - self.game.screen_pos.x
                    self.bounces += 1


                self.pos.y += self.vel.y / self._number_of_checks
                self.rect.centery = self.pos.y - self.game.screen_pos.y
                if spritecollide_sub(self, self.game.sub, False):
                    self.vel.y *= -1
                    self.pos.y += self.vel.y #/ self._number_of_checks
                    self.rect.centery = self.pos.y - self.game.screen_pos.y
                    self.bounces += 1
        else:
            self.kill()




def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()
