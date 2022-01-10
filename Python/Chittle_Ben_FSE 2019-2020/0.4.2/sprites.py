"""
Date: May 14, 2020
Version: 0.4.2
Added:

Removed:

Changed:

"""

import math
import pygame as pg
import config, items


class ShipSprite(pg.sprite.Sprite):
    """Sprite template optimized for use with 'Ship' objects."""
    def __init__(self):
        super().__init__()
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
            new_tiles = self.lvldata.ship.locate_sprite(self)
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
            return [current_tile] + [tile for tile in current_tile.neighbours().values()
                                     if tile is not None]

        # Return an empty list if the sprite isnt't in any Tile(s) or doesn't
        # know what Tile(s) it's in.
        except IndexError:
            return []


    def get_walls(self):
        """Returns a list of the 'Block' sprites that wall the sprite's current Tile(s)."""
        return [wall for tile in self.tiles for wall in tile.room.walls]


##########
class LiveSprite(ShipSprite):
    def __init__(self):
        super().__init__()




class Sentry(ShipSprite):
    size = (config.SENTRY_SIZE, config.SENTRY_SIZE)
    def __init__(self, lvldata, tile):
        super().__init__()
        self.lvldata = lvldata
        self.lvldata.all_sprites.add(self, layer=config.SPRITE_LAYER)
        self.add(self.lvldata.enemies)

        self.tile = tile
        self.pos = (tile.pos + (config.TILE_SIZE / 2, config.TILE_SIZE / 2))

        self.colour = config.ORANGE
        self.image_base = pg.Surface(self.size, pg.SRCALPHA)
        self.image_base.fill(self.colour)
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect()
        self.rotation = 0

        self.item_pos_offset = (0 ,config.SENTRY_SIZE / 1.5)
        self.blaster = items.SentryBlaster(self.lvldata, self.pos)
        self.detect_radius = config.TILE_SIZE // 2
        self.hp = 100


    def update(self):
        if pg.time.get_ticks() - self.blaster.last_shot_time > self.blaster.cooldown:
            player_pos = self.lvldata.player.pos
            player_dist = self.pos.distance_to(player_pos)
            if player_dist < self.detect_radius:
                self.rotation = (player_pos - self.pos).angle_to((1, 0))
                self.update_item_position()

                if player_dist > 10:
                    self.blaster.action()

        self.rect.center = self.pos - self.lvldata.screen_pos


    def update_item_position(self):
        # Sets the default position of the object (i.e. facing east) to be
        # at the owner's position with some offset so that it is placed at
        # the owner's side.
        self.blaster.pos = self.pos + self.item_pos_offset

        # A vector describing the displacement from the radius, which the
        # object will be rotated about, to the object.
        radial_vector = self.blaster.pos - self.pos

        # A vector describing the change in position as the radial vector is
        # rotated about the radius.
        change_vector = radial_vector.rotate(-(self.rotation + 90)) - radial_vector

        # Applying the change in position.
        self.blaster.pos += change_vector

        # Applying the rotation to the image.
        self.blaster.image = pg.transform.rotate(self.blaster.image_base, self.rotation)


    def draw_hitbox(self):
        pg.draw.rect(self.lvldata.screen, config.RED, self.rect, 2)
        pg.draw.circle(self.lvldata.screen, config.RED, self.rect.center,
                       self.detect_radius, 1)



def main():
    print("Run the 'main' module, not this one")

if __name__ == "__main__":
    main()
