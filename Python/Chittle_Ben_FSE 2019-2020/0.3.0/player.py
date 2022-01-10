import math
import pygame as pg
import config


#pg.init() # Necessary?

class Player(pg.sprite.Sprite):
    size = 16
    hitbox_size = math.sqrt(2 * size ** 2)
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.game.all_sprites.add(self)

        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2()

        self.collisions = True

        self.image_base = pg.Surface((self.size, self.size), pg.SRCALPHA)
        self.image_base.fill(config.GREEN)
        self.rect = pg.Rect(0, 0, self.hitbox_size, self.hitbox_size)
        self.rect.center = self.pos - self.game.screen_pos
        self.angle = 0

        self.equipped_item = HandBlaster(self)


    def update(self):
        mouse = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()

        if mouse[0]:
            self.primary_action()
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
        self.angle = (pg.Vector2(pg.mouse.get_pos()) - self.rect.center).angle_to((1, 0))
        self.image = pg.transform.rotate(self.image_base, self.angle)

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
            for wall in pg.sprite.spritecollide(self, self.game.walls, False):
                if self.vel.x > 0:
                    self.rect.right = wall.rect.left
                elif self.vel.x < 0:
                    self.rect.left = wall.rect.right
                self.vel.x = 0

        self.rect.y += self.vel.y
        if self.collisions:
            for wall in pg.sprite.spritecollide(self, self.game.walls, False):
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
        self.equipped_item.action()


class HandBlaster(pg.sprite.Sprite):
    size = (15, 5)

    def __init__(self, owner):
        super().__init__()
        self.game = owner.game
        self.owner = owner
        self.game.all_sprites.add(self, layer=config.SPRITE_LAYER)

        self.pos = self.owner.pos

        self.image_base = pg.Surface(self.size, pg.SRCALPHA)
        self.image_base.fill(config.RED)
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.game.screen_pos
        self.pos_offset = ((self.owner.size + self.size[1]) / 2, self.owner.size / 2)
        self.visible = True


    def update(self):
        if self.visible:
            # Sets the default position of the object (i.e. facing east) to be
            # at the owner's position with some offset so that it is placed at
            # the owner's side.
            self.pos = self.owner.pos + self.pos_offset

            # A vector describing the displacement from the radius, which the
            # object will be rotated about, to the object.
            radial_vector = self.pos - (self.game.screen_pos + self.owner.rect.center)

            # A vector describing the change in position as the radial vector is
            # rotated about the radius.
            self.change_vector = radial_vector.rotate(-(self.owner.angle + 90)) - radial_vector

            # Applying the change in position.
            self.pos += self.change_vector

            # Applying the rotation to the image.
            self.image = pg.transform.rotate(self.image_base, self.owner.angle)

            # Sets the rect's position to the new position.
            self.rect = self.image.get_rect(center=self.pos - self.game.screen_pos)


    def action(self):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        if mouse_pos != self.owner.pos:
            BlasterShot(self, mouse_pos - self.owner.rect.center)



class PlasmaRailCannon:
    pass



class BlasterShot(pg.sprite.Sprite):
    _number_of_checks = 3
    speed = 20
    power = 5
    max_range = 5000
    size = 4

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
        self.image.fill(config.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.game.screen_pos


    def update(self):
        for i in range(self._number_of_checks):
            self.pos += self.vel / self._number_of_checks
            self.rect.center = self.pos - self.game.screen_pos

            if pg.sprite.spritecollide(self, self.game.walls, False):
                self.kill()

        if self.pos.distance_to(self.game.player.pos) > self.max_range:
            self.kill()




def main():
    print("RUN THE OTHER ONE DAMMIT")

if __name__ == "__main__":
    main()
