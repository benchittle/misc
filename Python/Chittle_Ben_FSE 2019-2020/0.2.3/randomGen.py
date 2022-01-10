import random
import pygame as pg
import environment, config


class Sub:
    def __init__(self, game, width, height):
        self.game = game
        self.w = width
        self.h = height
        pixelw = (self.w + config.TILE_GAP) * config.ROOM_SCALE
        pixelh = (self.h + config.TILE_GAP) * config.ROOM_SCALE

        self.rect = pg.Rect(0, 0, pixelw, pixelh)
        self.grid = [[None] * self.w for i in range(self.h)]

        for row in range(self.h):
            for col in range(self.w):
                self.grid[row][col] = Tile(self, row, col)

        random.choice(self.rows[0]).tags.add("start")

        self.build()


    def __str__(self):
        string = ""
        for row in self.rows:
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
            if 0 <= r < self.h and 0 <= c < self.w:
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


    @property
    def columns(self):
        return tuple(zip(*self.grid))

    @property
    def rows(self):
        return tuple(self.grid)

    def _attribute_grid(self, attribute):
        return tuple([[getattr(tile, attribute) for tile in row] for row in self.rows])


    def iter_tiles(self):
        """Iterate over the tiles in the grid by row."""
        for row in self.rows:
            for tile in row:
                yield tile


    def build(self):
        for tile in self.iter_tiles():
            tile.build()

        path = self.generate_path()

        # Completely block off each room in the path.
        for tile in path:
            for loc, adj_tile in tile.adjacent_tiles.items():
                if adj_tile is not None:
                    if "path" not in adj_tile.tags:
                        tile.room.block_entrance(loc)

        for tile in self.iter_tiles():
            # Cleans up the floating walls around any rooms with closed doors.
            for loc in tile.room.doors:
                if tile.room.doors[loc]:
                    tile.remove_connector(loc)

            # Cleans up the floating walls and closes doors to any rooms next to
            # to a closed door.
            for loc, adj_tile in tile.adjacent_tiles.items():
                if adj_tile is not None:
                    for door_loc in adj_tile.room.doors:
                        if adj_tile.room.doors[door_loc]:
                            if loc == self.game.OPPOSITES[door_loc]:
                                tile.room.block_entrance(loc)
                                tile.remove_connector(loc)

        for tile in self.iter_tiles():
            if not tile.is_accessible():
                tile.remove()


    def generate_path(self):
        # Gets a list of the tiles in the grid
        tiles = list(self.iter_tiles())
        # Starts the path at the tile with the 'start' tag (list)
        path = self.find_by_tags("start")

        # Crude method of randomly getting a path: chooses a random adjacent
        # tile from the previous tile. If no path can be taken
        fail_count = 0
        while path[-1].row != self.h - 1:
            next_tile = random.choice([tile for tile in path[-1].adjacent_tiles.values() if tile is not None])
            if next_tile not in path:
                path.append(next_tile)
            else:
                fail_count += 1
                if fail_count > 4:
                    path = [tiles[0]]

        for tile in path:
            tile.tags.add("path")

        return path



class Tile:
    def __init__(self, sub, row, col, *tags):
        self.game = sub.game
        self.sub = sub
        self.tags = set(tags)

        self.row = row
        self.col = col
        self.pos = pg.Vector2(self.col, self.row) * config.TILE_SCALE
        self.rect = pg.Rect(self.pos, (config.TILE_SCALE, config.TILE_SCALE))
        self.kind = random.choices([Hall, Room], weights=[2, 3])[0]
        self.connectors = {
            "n" : [],
            "e" : [],
            "s" : [],
            "w" : []
            }


    def build(self):
        self.room = self.kind(self, self.pos)

        for loc, tile in self.adjacent_tiles.items():
            if tile is not None:
                self.add_connector(loc)


    def add_connector(self, loc):
        length = config.ROOM_SCALE // 2
        if loc == "n" or loc == "s":
            kind = environment.VWall
            anchor1 = self.game.DIRECTIONS[loc] + "right"
            anchor2 = self.game.DIRECTIONS[loc] + "left"
        elif loc == "e" or loc == "w":
            kind = environment.HWall
            anchor1 = "bottom" + self.game.DIRECTIONS[loc]
            anchor2 = "top" + self.game.DIRECTIONS[loc]

        self.connectors[loc].append(kind(self.game, getattr(self, loc)[1], length, anchor1))
        self.connectors[loc].append(kind(self.game, getattr(self, loc)[3], length, anchor2))


    def remove_connector(self, loc):
        for wall in self.connectors[loc]:
            wall.kill()
        self.connectors[loc].clear()


    def is_accessible(self):
        for loc, doors in self.room.doors.items():
            if not doors:
                return True
        return False


    def remove(self):
        for wall in self.room.walls.values():
            wall.kill()
        for wall in self.room.doors.values():
            wall.kill()

        del self


    def __str__(self):
        return "{}({}, {})".format(self.kind.name, self.row, self.col)

    def __repr__(self):
        return str(self)

    @property
    def adjacent_tiles(self):
        return self.sub.adjacent_tiles(self.row, self.col)

    @property
    def n(self):
        return [
            self.rect.topleft,
            (self.rect.centerx - config.DOOR_WIDTH / 2, self.rect.top),
            self.rect.midtop,
            (self.rect.centerx + config.DOOR_WIDTH / 2, self.rect.top),
            self.rect.topright
            ]

    @property
    def e(self):
        return [
            (self.rect.right, self.rect.top),
            (self.rect.right, self.rect.centery - config.DOOR_WIDTH / 2),
            (self.rect.right, self.rect.centery),
            (self.rect.right, self.rect.centery + config.DOOR_WIDTH / 2),
            (self.rect.right, self.rect.bottom)
            ]

    @property
    def s(self):
        return [
            (self.rect.left, self.rect.bottom),
            (self.rect.centerx - config.DOOR_WIDTH / 2, self.rect.bottom),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.centerx + config.DOOR_WIDTH / 2, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
            ]

    @property
    def w(self):
        return [
            self.rect.topleft,
            (self.rect.left, self.rect.centery - config.DOOR_WIDTH / 2),
            self.rect.midleft,
            (self.rect.left, self.rect.centery + config.DOOR_WIDTH / 2),
            self.rect.bottomleft
            ]



class RoomBase:
    def __init__(self, tile, pos):
        self.game = tile.game
        self.sub = tile.sub
        self.tile = tile
        self.pos = pos
        self.doors = {"n" : [], "e" : [], "s" : [], "w" : []}

        self.rect = self.tile.rect.inflate(-config.ROOM_SCALE, -config.ROOM_SCALE)
        if self.rect.w != self.rect.h:
            raise ValueError("Rooms must be square")
        self.length = self.rect.w

    def remove(self):
        self.tile.remove()


    @property
    def n(self):
        return [
            self.rect.topleft,
            (self.rect.centerx - config.DOOR_WIDTH / 2, self.rect.top),
            self.rect.midtop,
            (self.rect.centerx + config.DOOR_WIDTH / 2, self.rect.top),
            self.rect.topright
            ]

    @property
    def e(self):
        return [
            (self.rect.right, self.rect.top),
            (self.rect.right, self.rect.centery - config.DOOR_WIDTH / 2),
            (self.rect.right, self.rect.centery),
            (self.rect.right, self.rect.centery + config.DOOR_WIDTH / 2),
            (self.rect.right, self.rect.bottom)
            ]

    @property
    def s(self):
        return [
            (self.rect.left, self.rect.bottom),
            (self.rect.centerx - config.DOOR_WIDTH / 2, self.rect.bottom),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.centerx + config.DOOR_WIDTH / 2, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
            ]

    @property
    def w(self):
        return [
            self.rect.topleft,
            (self.rect.left, self.rect.centery - config.DOOR_WIDTH / 2),
            self.rect.midleft,
            (self.rect.left, self.rect.centery + config.DOOR_WIDTH / 2),
            self.rect.bottomleft
            ]



class Room(RoomBase):
    name = "Room"
    def __init__(self, tile, pos):
        super().__init__(tile, pos)

        self.walls = {
            "n" : [environment.HWall(self.game, self.n[0], self.length, "topleft")],
            "e" : [environment.VWall(self.game, self.e[0], self.length, "topright")],
            "s" : [environment.HWall(self.game, self.s[0], self.length, "bottomleft")],
            "w" : [environment.VWall(self.game, self.w[0], self.length, "topleft")]
            }

        for loc, tile in self.tile.adjacent_tiles.items():
            if tile is not None:
                self.walls[loc] = list(self.walls[loc][0].split(config.DOOR_WIDTH))


    def block_entrance(self, loc):
        anchor = "mid" + self.game.DIRECTIONS[loc]

        if loc == "n" or loc == "s":
            block = environment.HWall(self.game, getattr(self, loc)[2], config.DOOR_WIDTH, anchor)
        elif loc == "e" or loc == "w":
            block = environment.VWall(self.game, getattr(self, loc)[2], config.DOOR_WIDTH, anchor)

        self.doors[loc].append(block)


class Hall(RoomBase):
    name = "Hall"
    def __init__(self, tile, pos):
        super().__init__(tile, pos)
        offset = config.DOOR_WIDTH / 2

        self.walls = {"n" : [], "e" : [], "s" : [], "w" : []}

        vwalls = [
            environment.VWall(self.game, self.n[1], self.length, "topright"),
            environment.VWall(self.game, self.n[3], self.rect.h, "topleft")
            ]
        hwalls = [
            environment.HWall(self.game, self.w[1], self.length, "bottomleft"),
            environment.HWall(self.game, self.w[3], self.length, "topleft")
        ]

        for wall in vwalls:
            nwall, swall = wall.split(config.DOOR_WIDTH)
            self.walls["n"].append(nwall)
            self.walls["s"].append(swall)
        for wall in hwalls:
            wwall, ewall = wall.split(config.DOOR_WIDTH)
            self.walls["w"].append(wwall)
            self.walls["e"].append(ewall)

        for loc, tile in self.tile.adjacent_tiles.items():
            if tile is None:
                self.block_entrance(loc)


    def block_entrance(self, loc):
        anchor = "mid" + self.game.DIRECTIONS[loc]

        if loc == "n" or loc == "s":
            block = environment.HWall(self.game, getattr(self, loc)[2], config.DOOR_WIDTH, anchor)
        elif loc == "e" or loc == "w":
            block = environment.VWall(self.game, getattr(self, loc)[2], config.DOOR_WIDTH, anchor)

        self.doors[loc].append(block)



def main():
    sub1 = Sub("test", 4, 7)
    print(sub1)
    print()
    print(sub1.adjacent_tiles(0, 1))


if __name__ == "__main__":
    main()

