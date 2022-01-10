"""
Date: April 27, 2020
Version: 0.4.0
Added:
    Ship.get_tile_coord

Removed:

Changed:

"""


import random, typing
import pygame as pg
import config, environment, sprites

# 1 quad grid for 0 to 42 tiles
# 2 for 43 to 170
# 3 for 171 to 682



class TileGrid(list):
    def __init__(self, ship, rows, columns):
        super().__init__([[None] * columns for row in range(rows)])
        self.ship = ship
        self.rows = rows
        self.columns = columns

        # For an even length row, the two middle positions will each be
        # determined and stored. For an odd length row, right_mid and left_mid
        # will be the same since there is only one middle.
        right_mid = self.columns // 2
        left_mid = right_mid - 1 if self.columns % 2 == 0 else right_mid

        # Initializes to a random number.
        row_span = self.columns // 2 - 1#random.randint(1, self.columns // 2 - 1)

        # Generate a semi-random number of tiles centered in each row of the
        # grid.
        for row in range(self.rows):
            if left_mid - row_span <= 0 or right_mid + row_span >= self.columns - 1:
                row_span -= random.randint(0, 1)
            else:
                row_span -= random.randint(-1, 1)

            # Generate Tiles on either side of the center of the row.
            if self.columns % 2 == 0:
                self[row][left_mid] = Tile(self.ship, row, left_mid)
                self[row][right_mid] = Tile(self.ship, row, right_mid)
            else:
                self[row][left_mid] = Tile(self.ship, row, left_mid)

            for col in range(1, row_span + 1):
                self[row][left_mid - col] = Tile(self.ship, row, left_mid - col)
                self[row][right_mid + col] = Tile(self.ship, row, right_mid + col)


    def __str__(self):
        string = ""
        for row in self:
            for tile in row:
                if tile is None:
                    tile = ""
                string += "|{:^7}|".format(str(tile))
            string += "\n" + "-" * len(row) * 9 + "\n"
        return string


    def find_neighbours(self, row, col):
        tiles = {}
        adjacent_coords = {
            "n" : (row - 1, col),
            "e" : (row, col + 1),
            "s" : (row + 1, col),
            "w" : (row, col - 1)
            }

        for loc, (adj_row, adj_col) in adjacent_coords.items():
            if 0 <= adj_row < self.rows and 0 <= adj_col < self.columns: ### ACCOUNT FOR THIS
                tiles[loc] = self[adj_row][adj_col]
            else:
                tiles[loc] = None
        return tiles


    def depth_first_path(self, start, end):
        start_tile = self[start[0]][start[1]]
        end_tile = self[end[0]][end[1]]
        visited = set()
        path = []
        is_complete = self._depth_first_path(start_tile, end_tile, path, visited)
        return is_complete, path


    def _depth_first_path(self, current_tile, end_tile, path, visited):
        path.append(current_tile)
        visited.add(current_tile)

        if current_tile is not end_tile:
            for loc in current_tile.entrances:
                neighbour = current_tile.neighbours()[loc]
                if neighbour not in visited:
                    if self._depth_first_path(neighbour, end_tile, path, visited):
                        return True
                    path.pop()
        else:
            return True
        return False


    def is_accessible(self, row, col):
        start_tile = self.find_by_tags("start")[0]
        return self.depth_first_path(start_tile.rowcol, (row, col))[0]


    def get_start_end_path(self):
        start_tile = self.find_by_tags("start")[0]
        end_tile = self.find_by_tags("end")[0]
        is_playable, path = self.depth_first_path(start_tile.rowcol, end_tile.rowcol)
        if is_playable:
            return path
        else:
            return False


    def transposed(self):
        """Generates the transposed matrix."""
        for col in zip(*self):
            yield col


    def filter_row(self, row):
        """Returns a list containing only the 'Tile' objects in the given row."""
        # Assume 'row' is an iterable containing the row's elements.
        try:
            return [tile for tile in row if tile is not None]
        # Assume 'row' is the index of the desired row.
        except TypeError:
            return [tile for tile in self[row] if tile is not None]


    def filter_col(self, col):
        """Returns a list containing only the 'Tile' objects in the given column."""
        # Assume 'col' is an iterable containing the column's elements.
        try:
            return [tile for tile in col if tile is not None]
        # Assume 'col' is the index of the desired column.
        except TypeError:
            return [tile for tile in self.transposed()[col] if tile is not None]


    def filtered_rows(self):
        """Returns the matrix with each row filtered ('None' values removed)."""
        return [self.filter_row(row) for row in self]


    def filtered_cols(self):
        """Returns the transposed matrix with each column filtered ('None' values removed)."""
        return [self.filter_col(col) for col in self.transposed()]


    def iter_tiles(self):
        """Iterate by row over each tile in the filtered matrix."""
        for row in self.filtered_rows():
            for tile in row:
                yield tile


    def find_by_tags(self, *args):
        """Returns a list of the 'Tile' objects that have all of the given tags."""
        tiles = []
        for tile in self.iter_tiles():
            if tile.tags.issuperset(args):
                tiles.append(tile)
        return tiles



class Ship:
    def __init__(self, lvldata, pos, max_width, length):
        self.lvldata = lvldata
        self.grid = TileGrid(self, length, max_width)
        self.tiles = list(self.grid.iter_tiles())
        self.rect = self.tiles[0].rect.unionall(self.tiles[1:])
        self.pos = self.lvldata.screen_pos + self.rect.topleft
        self.radius = self.pos.distance_to(self.rect.center)

        # Make a random tile in the first row the start tile and a random tile
        # in the last row the end tile.
        random.choice([tile for tile in self.grid[0] if tile is not None]).tags.add("start")
        random.choice([tile for tile in self.grid[-1] if tile is not None]).tags.add("end")

        for row in range(self.grid.rows):
            # Create entrances between each tile in the row.
            for tile in self.grid[row]:
                if tile is not None:
                    n = tile.neighbours()

                    if tile.neighbours()["w"] is not None:
                        tile.entrances.add("w")
                    if tile.neighbours()["e"] is not None:
                        tile.entrances.add("e")

            if row > 0:
                # Generate a random number of doors leading to the previous row
                # (unless the current row is the first row).
                common = []
                for col in range(self.grid.columns):
                    if self.grid[row][col] is not None and self.grid[row - 1][col] is not None:
                        common.append(self.grid[row][col])
                for tile in random.sample(common, k=random.randint(1, len(common))):
                    tile.add_entrance("n")

                # Randomly remove doors between tiles in the same row if they
                # have entrances to the previous or next row.
                for tile in self.grid[row - 1]:
                    if tile is not None:
                        removeable = [loc for loc in tile.entrances
                                      if (loc == "e" or loc == "w")
                                      and ("n" in tile.neighbours()[loc].entrances
                                            or "s" in tile.neighbours()[loc].entrances)]
                        for loc in random.sample(removeable, k=random.randint(0, len(removeable))):
                            tile.remove_entrance(loc)
                            if (not tile.is_accessible()
                            or not tile.neighbours()[loc].is_accessible()):
                                tile.add_entrance(loc)
        self.build()

    def update(self):
        self.rect.topleft = self.pos - self.lvldata.screen_pos


    def add_entrance(self, row, col, loc):
        tile = self.grid[row][col]
        neighbour = tile.neighbours()[loc]
        tile.entrances.add(loc)
        if neighbour is not None:
            neighbour.entrances.add(config.OPPOSITES[loc])


    def remove_entrance(self, row, col, loc):
        tile = self.grid[row][col]
        neighbour = tile.neighbours()[loc]
        tile.entrances.remove(loc)
        if neighbour is not None:
            neighbour.entrances.remove(config.OPPOSITES[loc])


    def build(self):
        for tile in self.grid.iter_tiles():
            if tile is not None:
                tile.build()


    def locate_sprite(self, sprite):
        """Returns a tuple containing the Tiles the sprite is currently in."""
        return pg.sprite.spritecollide(sprite, self.tiles, False)


    def get_tile_coord(self, grid_pos):
        """Returns the position relative to the map of the Tile at the given grid position."""
        return self.grid[grid_pos[0]][grid_pos[1]].pos



class Tile(pg.sprite.Sprite):
    def __init__(self, ship, row, col, *tags):
        super().__init__()
        self.lvldata = ship.lvldata
        self.lvldata.all_sprites.add(self, layer=config.TILE_LAYER)
        self.ship = ship
        self.row = row
        self.col = col
        self.rowcol = (self.row, self.col)
        self.pos = pg.Vector2(self.col, self.row) * config.TILE_SIZE
        self.pos += (config.TILE_GAP * self.col, config.TILE_GAP * self.row)

        self.image = pg.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.image.fill(config.TILE_COLOUR)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos - self.lvldata.screen_pos

        self.tags = set(tags)
        self.entrances = set()
        self.room = random.choice([Corridor, Room])(self)


    def __repr__(self):
        return "{:}@{},{}".format(self.room, self.row, self.col)


    def update(self):
        self.rect.topleft = self.pos - self.lvldata.screen_pos


    def add_entrance(self, loc):
        self.ship.add_entrance(self.row, self.col, loc)


    def remove_entrance(self, loc):
        self.ship.remove_entrance(self.row, self.col, loc)


    def is_accessible(self):
        return self.ship.grid.is_accessible(self.row, self.col)


    def build(self):
        self.room.build()



    def neighbours(self):
        return self.ship.grid.find_neighbours(self.row, self.col)



class Room(pg.sprite.Sprite):
    def __init__(self, tile):
        super().__init__()
        self.lvldata = tile.lvldata
        self.lvldata.all_sprites.add(self, layer=config.ROOM_LAYER)
        self.tile = tile

        self.walls = pg.sprite.Group()

        self.image = pg.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.image.fill(config.ROOM_COLOUR)
        self.rect = self.tile.rect


    def __str__(self):
        return "R"


    # Use this as keys for sides
    @property
    def placements(self):
        return {
            "n" : self.tile.pos,
            "e" : self.tile.pos + (config.TILE_SIZE, 0) - (config.WALL_WIDTH, 0),
            "s" : self.tile.pos + (0, config.TILE_SIZE) - (0, config.WALL_WIDTH),
            "w" : self.tile.pos
            }
    @property
    def sides(self):
        return {
            "n" : environment.HWallDoor if "n" in self.tile.entrances else environment.HWall,
            "e" : environment.VWallDoor if "e" in self.tile.entrances else environment.VWall,
            "s" : environment.HWallDoor if "s" in self.tile.entrances else environment.HWall,
            "w" : environment.VWallDoor if "w" in self.tile.entrances else environment.VWall
            }


    def build(self):
        for loc, Kind in self.sides.items():
            Kind(self.lvldata, self.placements[loc], self.walls)


        if random.randint(1, 100) < 20:
            self.walls.add(sprites.Sentry(self.lvldata, self.tile))


'''
class OpenRoom(pg.sprite.Group):
    def __init__(self, tile):
        super().__init__()
        self.lvldata = tile.lvldata
        self.tile = tile

        # Use this as keys for sides
    @property
    def placements(self):
        return {
            "n" : self.tile.pos,
            "e" : self.tile.pos + (config.TILE_SIZE, 0) - (config.WALL_WIDTH, 0),
            "s" : self.tile.pos + (0, config.TILE_SIZE) - (0, config.WALL_WIDTH),
            "w" : self.tile.pos
            }

    @property
    def sides(self):
        return {
            "n" : environment.HWallDoor if "n" in self.tile.entrances else environment.HWall,
            "e" : environment.VWallDoor if "e" in self.tile.entrances else environment.VWall,
            "s" : environment.HWallDoor if "s" in self.tile.entrances else environment.HWall,
            "w" : environment.VWallDoor if "w" in self.tile.entrances else environment.VWall
            }


    def build(self):
        for loc, kind in self.sides.items():
            if type(self.tile.find_neighbours[loc].room) != OpenRoom:
                kind(self.lvldata, self.placements[loc], groups=(self, self.lvldata.walls))
'''


class Corridor(pg.sprite.Sprite):
    _p1 = (config.TILE_SIZE - config.DOOR_SIZE) // 2
    _p2 = (config.TILE_SIZE + config.DOOR_SIZE) // 2
    _image_rects = {
        "n" : pg.Rect(_p1, 0, config.DOOR_SIZE, _p2),
        "e" : pg.Rect(_p1, _p1, _p2, config.DOOR_SIZE),
        "s" : pg.Rect(_p1, _p1, config.DOOR_SIZE, _p2),
        "w" : pg.Rect(0, _p1, _p2, config.DOOR_SIZE)
    }

    def __init__(self, tile):
        super().__init__()#rooms)
        self.lvldata = tile.lvldata
        self.lvldata.all_sprites.add(self, layer=config.ROOM_LAYER)
        self.tile = tile

        self.walls = pg.sprite.Group()

        self.image = pg.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.image.set_colorkey(config.BLACK, pg.RLEACCEL)
        self.rect = self.tile.rect


    def __str__(self):
        return "C"


        # Use this as keys for sides
    @property
    def placements(self):
        return {
            "n" : self.tile.pos + (config.TILE_SIZE // 2, (config.TILE_SIZE - config.DOOR_SIZE) // 2),
            "e" : self.tile.pos + ((config.TILE_SIZE + config.DOOR_SIZE) // 2, config.TILE_SIZE // 2),
            "s" : self.tile.pos + (config.TILE_SIZE // 2, (config.TILE_SIZE + config.DOOR_SIZE) // 2),
            "w" : self.tile.pos + ((config.TILE_SIZE - config.DOOR_SIZE) // 2, config.TILE_SIZE // 2)
            }

    @property
    def sides(self):
        return {
            "n" : environment.VCorr if "n" in self.tile.entrances else environment.VCorrDoor,
            "e" : environment.HCorr if "e" in self.tile.entrances else environment.HCorrDoor,
            "s" : environment.VCorr if "s" in self.tile.entrances else environment.VCorrDoor,
            "w" : environment.HCorr if "w" in self.tile.entrances else environment.HCorrDoor
            }


    def build(self):
        for loc, rect in Corridor._image_rects.items():
            if loc in self.tile.entrances:
                self.image.fill(config.ROOM_COLOUR, rect=rect)

        for loc, Kind in self.sides.items():
            anchor = "mid" + config.OPPOSITES[config.CONVERSIONS[loc]]
            Kind(self.lvldata, self.placements[loc], self.walls, anchor=anchor)


def main():
    print("RUN THE OTHER ONE DAMMIT BEN")

if __name__ == "__main__":
    main()


