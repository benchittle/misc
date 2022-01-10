import random
import pygame as pg
import config, environment


class Sub:
    def __init__(self, game, pos, max_width, height):
        self.game = game
        self.pos = pg.Vector2(pos)
        self.max_w = max_width
        self.h = height

        self.grid = [[None] * self.max_w for i in range(self.h)]
        for row in range(self.h):
            for col in range(self.max_w):
                self.grid[row][col] = random.choices([Tile(self, row, col), None], weights=[3, 1])[0]

        self.build()


    def __str__(self):
        string = ""
        for row in self.iter_rows():
            for tile in row:
                string += "|{:^14}|".format(str(tile))
            string += "\n" + "-" * len(row) * 16 + "\n"
        return string


    def adjacent_tiles(self, row, col):
        tiles = {}
        coords = {
            "n" : (row - 1, col),
            "e" : (row, col + 1),
            "s" : (row + 1, col),
            "w" : (row, col - 1)
            }

        for direction, (r, c) in coords.items():
            if 0 <= r < self.h and 0 <= c < self.max_w: ### ACCOUNT FOR THIS
                tiles[direction] = self.grid[r][c]
            else:
                tiles[direction] = None
        return tiles


    def find_by_tags(self, *tags):
        tiles = []
        for tile in self.iter_tiles():
            if tile.tags.issuperset(tags):
                tiles.append(tile)
        return tiles


    def iter_columns(self):
        for col in zip(*self.grid):
            yield col


    def iter_rows(self):
        for row in self.grid:
            yield row


    def iter_tiles(self):
        """Iterate over the tiles in the grid by row."""
        for row in self.iter_rows():
            for tile in row:
                yield tile


    def build(self):
        for tile in self.iter_tiles():
            if tile is not None:
                tile.build()


class Tile:
    def __init__(self, container, row, col, *tags):
        self.game = container.game
        self.container = container
        self.row = row
        self.col = col
        self.pos = self.container.pos + pg.Vector2(self.col, self.row) * config.TILE_SIZE
        self.rect = pg.Rect(self.pos, (config.TILE_SIZE, config.TILE_SIZE))
        self.tags = set(tags)

        self.entrances = set()
        self.room = random.choice([Corridor, Room])(self)


    def build(self):
        for loc, tile in self.adjacent_tiles.items():
            if tile is not None:
                self.entrances.add(loc)

        self.room.build()


    @property
    def adjacent_tiles(self):
        return self.container.adjacent_tiles(self.row, self.col)


class Room(pg.sprite.Group):
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
            kind(self.game, self.placements[loc], groups=(self, self.game.walls))



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
            if type(self.tile.adjacent_tiles[loc].room) != OpenRoom:
                kind(self.game, self.placements[loc], groups=(self, self.game.walls))



class Corridor(pg.sprite.Group):
    def __init__(self, tile):
        super().__init__()
        self.game = tile.game
        self.tile = tile


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
        for loc, kind in self.sides.items():
            anchor = "mid" + self.game.OPPOSITES[self.game.DIRECTIONS[loc]]
            kind(self.game, self.placements[loc], anchor=anchor, groups=(self, self.game.walls))





