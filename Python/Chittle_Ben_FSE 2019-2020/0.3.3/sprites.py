"""
Date: April 9, 2020
Version: 0.3.3
Added:

Removed:

Changed:
    >'HandBlaster.is_item' -> 'HandBlaster.is_on_ground'
    >'HandBlaster.is_active' -> 'HandBlaster.is_hidden'
    >Player.pickup_item - now checks the ground_items Group and chooses the
        first item detected that is within a certain range
"""

import math
import pygame as pg
import config


class ShipSprite(pg.sprite.Sprite):
    """Sprite subclass designed to exist within a Ship."""
    def __init__(self, ship):
        super().__init__()
        self.ship = ship
        self._tiles = None


    @property
    def tiles(self):
        return self._tiles

    @tiles.setter
    def tiles(self, tiles):
        # If the sprite has moved onto a new tile.
        if self.tiles != tiles:
            self._tiles = tiles
            # Update the list of Tiles the sprite could be colliding with.
            self._tiles_to_check = self.get_nearby_tiles()
            # Update the list of walls the sprite could be colliding with.
            self._walls_to_check = self.get_walls()

        # If 'tiles' is an empty list (the sprite escaped the ship).
        elif not tiles:
            # Try to find the sprite's position on the ship.
            new_tiles = self.ship.locate_sprite(self)
            # If successful, apply the change to the sprite's tile tracker.
            if new_tiles:
                self.tiles = new_tiles


    def get_nearby_tiles(self):
        """Returns a list of the sprite's current tile and its neighbours."""
        # Assume the sprite is in at least one Tile and knows which Tile(s) it's
        # in.
        try:
            # Choose the first tile as the current tile even if the sprite is
            # between two tiles; the other tile the sprite is in will be one of
            # its neighbours.
            current_tile = self.tiles[0]
            return [current_tile] + [tile for tile in current_tile.neighbours().values() if tile is not None]

        # Return an empty list if the sprite isnt't in any Tile(s) or doesn't
        # know what Tile(s) it's in.
        except IndexError:
            return []


    def get_walls(self):
        """Returns a list of the 'Block' sprites that wall the sprite's current Tile(s)."""
        return [wall for tile in self.tiles for wall in tile.room.walls]



class Player(ShipSprite):
    size = 16
    hitbox_size = math.sqrt(2 * size ** 2)
    noclip = False
    def __init__(self, game, ship, pos):
        super().__init__(ship)
        self.game = game

        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2()

        self.image_base = pg.Surface((self.size, self.size), pg.SRCALPHA)
        self.image_base.fill(config.GREEN)
        self.rect = self.image_base.get_rect(center=self.pos - self.game.screen_pos)
        self.rotation = 0

        self.tiles = self.ship.locate_sprite(self)

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
            self.equipped_item.is_hidden = True
        self._equipped_item = index
        if self.equipped_item is not None:
            self.equipped_item.is_hidden = False


    def pickup_item(self):
        items = []
        for item in self.game.ground_items:
            if self.pos.distance_to(item.pos) < 100:
                items.append(item)
        if items:
            try:
                print("potential items: {}".format(items))
                self.inventory[self.inventory.index(None)] = items[0]
                item.owner = self
                item.is_on_ground = False

            except IndexError:
                print("Inventory full: item not picked up.")
        else:
            print("No items nearby.")


    def update(self):
        # Get mouse and keyboard input.
        mouse = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()

        num_keys = keys[pg.K_1:pg.K_9 + 1]
        if any(num_keys):
            self.equipped_item = num_keys.index(1)

        if mouse[0]:
            self.primary_action()
        # Change the player's speed in the given direction.
        if keys[pg.K_a]: # Left
            self.vel.x -= config.PLAYER_ACCEL
        if keys[pg.K_d]: # Right
            self.vel.x += config.PLAYER_ACCEL
        if keys[pg.K_s]: # Down
            self.vel.y += config.PLAYER_ACCEL
        if keys[pg.K_w]: # Up
            self.vel.y -= config.PLAYER_ACCEL

        self.update_position()


    def update_position(self):
        # Get the required angle to face the mouse (measured from x axis).
        self.rotation = (pg.Vector2(pg.mouse.get_pos()) - self.rect.center).angle_to((1, 0))
        # Rotate the sprite's image to face the mouse.
        self.image = pg.transform.rotate(self.image_base, self.rotation)

        # Keep player's speed below limit.
        if self.vel.magnitude() > config.PLAYER_MAX_SPEED:
            self.vel.scale_to_length(config.PLAYER_MAX_SPEED)
        # Apply friction if the player is moving.
        if self.vel.magnitude() > 0:
            self.vel -= self.vel * config.PLAYER_FRICTION
        # If any of the player's velocity components are negligible, set to 0.
        if abs(self.vel.x) < config.PLAYER_MIN_VEL:
            self.vel.x = 0
        if abs(self.vel.y) < config.PLAYER_MIN_VEL:
            self.vel.y = 0

        # Corrects bounding rect's sizes
        center = self.rect.center
        self.rect.size = (self.hitbox_size, self.hitbox_size)
        self.rect.center = center

        # Deal with movement in the x direction.
        self.rect.x += self.vel.x
        if not self.noclip:
            # Get the Tile(s) that the sprite is currently in.
            self.tiles = pg.sprite.spritecollide(self, self._tiles_to_check, False)
            # Check for a collision with each wall in the Tile(s) the sprite is
            # in.
            for wall in pg.sprite.spritecollide(self, self._walls_to_check, False):
                # If the player is moving right, handle the collision by placing
                # the player to the left of the wall it collided with.
                if self.vel.x > 0:
                    self.rect.right = wall.rect.left
                # If the player is moving left, handle the collision by placing
                # the player to the right of the wall it collided with.
                elif self.vel.x < 0:
                    self.rect.left = wall.rect.right
                self.vel.x = 0

        # Deal with movement in the y direction.
        self.rect.y += self.vel.y
        if not self.noclip:
        # Get the Tile(s) that the sprite is currently in.
            self.tiles = pg.sprite.spritecollide(self, self._tiles_to_check, False)
            # Check for a collision with each wall in the Tile(s) the sprite is
            # in.
            for wall in pg.sprite.spritecollide(self, self._walls_to_check, False):
                # If the player is moving down, handle the collision by placing
                # the player above the wall it collided with.
                if self.vel.y > 0:
                    self.rect.bottom = wall.rect.top
                # If the player is moving up, handle the collision by placing
                # the player below the wall it collided with.
                elif self.vel.y < 0:
                    self.rect.top = wall.rect.bottom
                self.vel.y = 0

        # Update the player's position relative to the map.
        self.pos.update(self.game.screen_pos + self.rect.center)
        # Update the camera's position relative to the map.
        self.game.screen_pos.update(self.pos - config.SCREEN_MID)
        # Update the player's position relative to the screen.
        self.rect = self.image.get_rect(center=self.pos - self.game.screen_pos)


    ### unnecessary?
    def primary_action(self):
        if self.equipped_item is not None:
            self.equipped_item.action()


class HandBlaster(pg.sprite.Sprite):
    size = (15, 5)
    cooldown = 10

    def __init__(self, game, ship, pos, rotation):
        super().__init__()
        self.game = game
        self.ship = ship

        self.owner = None
        self.pos = pg.Vector2(pos)
        self.rotation = rotation

        self.image_base = pg.Surface(self.size, pg.SRCALPHA)
        self.image_base.fill(config.RED)
        self.image = pg.transform.rotate(self.image_base, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.game.screen_pos

        self.last_shot_time = pg.time.get_ticks()
        self.is_hidden = False
        self.is_on_ground = True


    @classmethod
    def from_owner(cls, owner):
        instance = cls(owner.game, owner.ship, owner.pos, owner.rotation)
        instance.owner = owner
        instance.is_on_ground = False
        return instance


    @property
    def is_on_ground(self):
        return self._is_on_ground


    @is_on_ground.setter
    def is_on_ground(self, value):
        self._is_on_ground = value
        if self.is_on_ground:
            self.game.ground_items.add(self)
            self.owner = None
            self.pos_offset = 0
        else:
            self.game.ground_items.remove(self)
            self.pos_offset = (self.owner.size / 2, self.owner.size / 2)


    @property
    def is_hidden(self):
        return self._is_hidden


    @is_hidden.setter
    def is_hidden(self, value):
        self._is_hidden = value
        if self.is_hidden:
            self.game.all_sprites.remove(self)
        else:
            self.game.all_sprites.add(self, layer=config.SPRITE_LAYER)
            self.update()  ##


    def update(self):
        if not self.is_hidden:
            if self.owner is not None:
                self.move_to_owner()
            else:
                self.rect.center = self.pos - self.game.screen_pos


    def move_to_owner(self):
        # Sets the default position of the object (i.e. facing east) to be
        # at the owner's position with some offset so that it is placed at
        # the owner's side.
        self.pos = self.owner.pos + self.pos_offset

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
                self.last_shot_time = pg.time.get_ticks()
                BlasterShot(self, mouse_pos - self.rect.center)



class BlasterShot(ShipSprite):
    size = 6
    speed = 16
    power = 5
    max_range = 5000
    max_bounces = 1000
    _number_of_checks = 2
    noclip = False

    def __init__(self, blaster, trajectory):
        super().__init__(blaster.ship)
        self.game = blaster.game
        self.blaster = blaster
        self.game.all_sprites.add(self, layer=config.PROJECTILE_LAYER)
        self.add(self.game.projectiles)

        self.pos = self.blaster.pos
        self.vel = pg.Vector2(trajectory)
        self.vel.scale_to_length(self.speed)

        self.image = pg.Surface((self.size, self.size))
        self.image.fill(config.GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - self.game.screen_pos
        self.tiles = self.ship.locate_sprite(self)

        self.bounces = 0


    def update(self):
        self.update_position()

        if self.pos.distance_to(self.game.player.pos) > self.max_range:
            self.kill()


    def update_position(self):
        for i in range(self._number_of_checks):
            self.pos += self.vel / self._number_of_checks
            self.rect.center = self.pos - self.game.screen_pos
            self.tiles = pg.sprite.spritecollide(self, self._tiles_to_check, False)
            if pg.sprite.spritecollideany(self, self._walls_to_check, False):
                self.kill()


    def update_position_bouncy(self):
        if self.bounces < self.max_bounces:
            for i in range(self._number_of_checks):
                dx = self.vel.x / self._number_of_checks
                self.pos.x += dx
                self.rect.centerx = self.pos.x - self.game.screen_pos.x
                if not self.noclip:
                    self.tiles = pg.sprite.spritecollide(self, self._tiles_to_check, False)
                    if pg.sprite.spritecollideany(self, self._walls_to_check, False): ##
                        self.pos.x -= dx
                        self.vel.x *= -1
                        self.rect.centerx = self.pos.x - self.game.screen_pos.x
                        self.bounces += 1

                dy = self.vel.y / self._number_of_checks
                self.pos.y += dy
                self.rect.centery = self.pos.y - self.game.screen_pos.y
                if not self.noclip:
                    self.tiles = pg.sprite.spritecollide(self, self._tiles_to_check, False) ##
                    if pg.sprite.spritecollideany(self, self._walls_to_check, False): ##
                        self.pos.y -= dy
                        self.vel.y *= -1
                        self.rect.centery = self.pos.y - self.game.screen_pos.y
                        self.bounces += 1
        else:
            self.kill()



class PlasmaRailCannon:
    pass


def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()
