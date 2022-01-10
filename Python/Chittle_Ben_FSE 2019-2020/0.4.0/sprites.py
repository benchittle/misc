"""
Date: April 27, 2020
Version: 0.4.0
Added:
    Sentry

Removed:

Changed:

"""

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



class Sentry(ShipSprite):
    cooldown = 50
    def __init__(self, lvldata, tile):
        super().__init__()
        self.lvldata = lvldata
        self.lvldata.all_sprites.add(self, layer=config.SPRITE_LAYER)
        self.add(self.lvldata.enemies)

        self.tile = tile
        self.pos = (tile.pos + (config.TILE_SIZE / 2, config.TILE_SIZE / 2))

        self.colour = config.ORANGE
        self.image_base = pg.Surface((config.SENTRY_SIZE, config.SENTRY_SIZE), pg.SRCALPHA)
        self.image_base.fill(self.colour)
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect(center=self.pos - self.lvldata.screen_pos)

        self.detect_radius = 80
        self.hp = 100
        self.last_shot_time = 0


    def update(self):
        player_pos = self.lvldata.player.pos
        if pg.time.get_ticks() - self.last_shot_time > self.cooldown:
            if self.pos.distance_to(player_pos) < self.detect_radius:
                items.RegularShot(self.lvldata, self, player_pos - self.pos)
                self.last_shot_time = pg.time.get_ticks()

        self.rect.center = self.pos - self.lvldata.screen_pos

    def draw_radius(self):
        pg.draw.circle(self.lvldata.screen, config.RED, self.rect.center,
                       self.detect_radius, 1)












def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()
