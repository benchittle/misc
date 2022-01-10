import random
import pygame as pg
import config, environment

# 1 quad grid for 0 to 42 tiles
# 2 for 43 to 170
# 3 for 171 to 682



class TileGrid(list):
    def __init__(self, sub, rows, columns):
        super().__init__([[None] * columns for row in range(rows)])
        self.sub = sub
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
                self[row][left_mid] = Tile(self.sub, row, left_mid)
                self[row][right_mid] = Tile(self.sub, row, right_mid)
            else:
                self[row][left_mid] = Tile(self.sub, row, left_mid)

            for col in range(1, row_span + 1):
                self[row][left_mid - col] = Tile(self.sub, row, left_mid - col)
                self[row][right_mid + col] = Tile(self.sub, row, right_mid + col)


    def __str__(self):
        string = ""
        for row in self.iter_rows():
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


    def iter_columns(self):
        for col in zip(*self):
            yield col


    def iter_rows(self):
        for row in self:
            yield row


    def iter_tiles(self):
        """Iterate over the tiles in the grid by row."""
        for row in self.iter_rows():
            for tile in row:
                if tile is not None:
                    yield tile


    def find_by_tags(self, *tags):
        tiles = []
        for tile in self.iter_tiles():
            if tile.tags.issuperset(tags):
                tiles.append(tile)
        return tiles



class Sub:
    def __init__(self, game, pos, max_width, length):
        self.game = game
        self.pos = pg.Vector2(pos)
        self.grid = TileGrid(self, length, max_width)
        self.tiles = pg.sprite.Group(self.grid.iter_tiles())
        '''self.quadrant_rects = []
        self.quadrant_tiles = []
        quad_tiles = []
        quad_rects = []
        for row in self.grid.iter_rows():
            quad_tiles += [tile for tile in row if tile is not None]
            quad_rects += [tile.rect for tile in row if tile is not None]

            if len(quad_rects) >= len(self.tiles) // 4:
                self.quadrant_rects.append(quad_rects[0].unionall(quad_rects[1:]))
                self.quadrant_tiles.append(quad_tiles[:])
                quad_tiles.clear()
                quad_rects.clear()'''



        # Make a random tile in the first row the start tile and a random tile
        # in the last row the end tile.
        random.choice([tile for tile in self.grid[0] if tile is not None]).tags.add("start")
        random.choice([tile for tile in self.grid[-1] if tile is not None]).tags.add("end")

        for row in range(self.grid.rows):
            # Create entrances between each tile in the row.
            for tile in self.grid[row]:
                if tile is not None:
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
                        removeable = [loc for loc in tile.entrances if (loc == "e" or loc == "w") and ("n" in tile.neighbours()[loc].entrances or "s" in tile.neighbours()[loc].entrances)]
                        for loc in random.sample(removeable, k=random.randint(0, len(removeable))):
                            tile.remove_entrance(loc)
                            if not tile.is_accessible() or not tile.neighbours()[loc].is_accessible():
                                tile.add_entrance(loc)

        self.build()


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



class Tile(pg.sprite.Sprite):
    def __init__(self, sub, row, col, *tags):
        super().__init__()
        sub.game.all_sprites.add(self, layer=config.TILE_LAYER)
        self.sub = sub
        self.row = row
        self.col = col
        self.rowcol = (self.row, self.col)
        self.pos = pg.Vector2(self.col, self.row) * config.TILE_SIZE
        self.pos += (config.TILE_GAP * self.col, config.TILE_GAP * self.row)

        self.image = pg.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos - self.sub.game.screen_pos

        self.tags = set(tags)
        self.entrances = set()
        self.room = random.choice([Corridor, Room])(self)


    def __repr__(self):
        return "{:}@{},{}".format(self.room, self.row, self.col)


    def update(self):
        self.rect.topleft = self.pos - self.sub.game.screen_pos


    def add_entrance(self, loc):
        self.sub.add_entrance(self.row, self.col, loc)


    def remove_entrance(self, loc):
        self.sub.remove_entrance(self.row, self.col, loc)


    def is_accessible(self):
        return self.sub.grid.is_accessible(self.row, self.col)


    def build(self):
        self.image.fill(config.TILE_COLOUR)
        self.room.build()


    def neighbours(self):
        return self.sub.grid.find_neighbours(self.row, self.col)



class Room(pg.sprite.Sprite):
    def __init__(self, tile):
        super().__init__()
        tile.sub.game.all_sprites.add(self, layer=config.ROOM_LAYER)
        self.sub = tile.sub
        self.tile = tile

        self.walls = pg.sprite.Group()

        self.image = pg.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.tile.pos - self.sub.game.screen_pos


    def __str__(self):
        return "R"


    def update(self):
        self.rect.topleft = self.tile.pos - self.sub.game.screen_pos


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
        self.image.fill(config.ROOM_COLOUR)

        for loc, Kind in self.sides.items():
            Kind(self.sub.game, self.placements[loc], self.walls)


'''
class OpenRoom(pg.sprite.Group):
    def __init__(self, tile):
        super().__init__()
        self.game = tile.game
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
                kind(self.game, self.placements[loc], groups=(self, self.game.walls))
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
        self.sub = tile.sub
        self.tile = tile
        self.tile.sub.game.all_sprites.add(self, layer=config.ROOM_LAYER)

        self.walls = pg.sprite.Group()

        self.image = pg.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.image.set_colorkey(config.BLACK, pg.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.tile.pos - self.sub.game.screen_pos


    def __str__(self):
        return "C"


    def update(self):
        self.rect.topleft = self.tile.pos - self.sub.game.screen_pos


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
            Kind(self.sub.game, self.placements[loc], self.walls, anchor=anchor)





