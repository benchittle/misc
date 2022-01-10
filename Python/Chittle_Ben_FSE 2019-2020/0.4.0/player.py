"""
Date: April 27, 2020
Version: 0.4.0
Added:

Removed:

Changed:

"""

import math
import pygame as pg
import config, items, sprites


class Player(sprites.ShipSprite):
    size = 16
    hitbox_size = math.sqrt(2 * size ** 2)
    noclip = False
    def __init__(self, lvldata, pos):
        super().__init__()
        self.lvldata = lvldata

        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2()

        self.image_base = pg.Surface((self.size, self.size), pg.SRCALPHA)
        self.image_base.fill(config.GREEN)
        self.rect = self.image_base.get_rect(center=self.pos - self.lvldata.screen_pos)
        self.rotation = 0

        self.tiles = self.lvldata.ship.locate_sprite(self)

        self.item_pos_offset = (self.size / 2, self.size / 2)
        self.inventory = [None] * 9
        self.inventory[0] = items.HandBlaster.from_owner(self) ##
        self._equipped_item = 0
        #self.equipped_item = 0


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
        mouse_pos = pg.mouse.get_pos()
        items = []
        for item in self.lvldata.ground_items:
            dist = pg.Vector2(item.rect.center).distance_to(mouse_pos)
            if dist < 15:
                items.append((dist, item))
        print("potential items: {}".format(items))
        if items:
            # Select the closest item.
            new_item = min(items, key=lambda tup: tup[0])[1]
            new_item.pos = pg.Vector2(self.pos)
            is_empty = not any(self.inventory)
            index = self.add_to_inventory(new_item)
            if is_empty or index == self._equipped_item:
                self.equipped_item = index
            self.lvldata.inv_menu.buttons[index].set_image(new_item.image_base)
        else:
            print("No items nearby.")


    def add_to_inventory(self, item, index=None):
        if index is None:
            try:
                index = self.inventory.index(None)
                self.inventory[index] = item
            except IndexError:
                print("Inventory full; item not added")
                return None
        else:
            self.inventory[index] = item
        item.owner = self
        item.is_on_ground = False
        item.is_hidden = True
        return index


    def drop_item(self, index):
        item = self.inventory[index]
        if item is not None:
            item.is_on_ground = True
            item.pos = pg.Vector2(self.pos)
            item.update()
            self.inventory[index] = None
            self.lvldata.inv_menu.buttons[index].set_empty()


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
        if self.equipped_item is not None:
            self.update_item_position()


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
        self.pos.update(self.lvldata.screen_pos + self.rect.center)
        # Update the screen's position relative to the map.
        self.lvldata.screen_pos.update(self.pos - config.SCREEN_MID)
        # Update the player's position relative to the screen.
        self.rect = self.image.get_rect(center=self.pos - self.lvldata.screen_pos)


    def update_item_position(self):
        item = self.equipped_item
        # Sets the default position of the object (i.e. facing east) to be
        # at the owner's position with some offset so that it is placed at
        # the owner's side.
        item.pos = self.pos + self.item_pos_offset

        # A vector describing the displacement from the radius, which the
        # object will be rotated about, to the object.
        radial_vector = item.pos - (self.lvldata.screen_pos + self.rect.center)

        # A vector describing the change in position as the radial vector is
        # rotated about the radius.
        change_vector = radial_vector.rotate(-(self.rotation + 90)) - radial_vector

        # Applying the change in position.
        item.pos += change_vector

        # Applying the rotation to the image.
        item.image = pg.transform.rotate(item.image_base, self.rotation)


    ### unnecessary?
    def primary_action(self):
        if self.equipped_item is not None:
            self.equipped_item.action()



def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()


