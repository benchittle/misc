import random
import pygame as pg
import config, environment



class Sub:
    def __init__(self, game, pos, max_width, height):
        self.game = game
        self.pos = pos
        self.max_w = max_width
        self.h = height
        mid = self.max_w // 2

        #self.rect = pg.Rect(0, 0, pixelw, pixelh)
        self.grid = [[None] * self.max_w for i in range(self.h)]

        for row in range(self.h):
            for radius in range(1, mid + 1):
                self.grid[row][mid + radius] = Tile(self)
                self.grid[row][mid - radius] = Tile(self)

        for tile in self.iter_tiles():
            tile.build()


    def iter_rows(self):
        for row in self.grid:
            yield row


    def iter_columns(self):
        for col in zip(*self.grid):
            yield col


    def iter_tiles(self):
        """Iterate over the tiles in the grid by row."""
        for row in self.iter_rows():
            for tile in row:
                yield tile


    def find_tile(self, tile):
        for row, tiles in enumerate(self.iter_rows()):
            try:
                return (row, list(tiles).index(tile))
            except ValueError:
                pass



class Tile:
    def __init__(self, container):
        self.game = container.game
        self.container = container


    def build(self):
        self.row, self.col = self.container.find_tile(self)
        self.pos = self.container.pos + pg.Vector2(self.col, self.row) * config.TILE_SIZE

        self.rect = pg.Rect(self.pos, (config.TILE_SIZE, config.TILE_SIZE))

        self.kind = random.choice(["room", "hall"])



def main():
    #s = Sub(None, pg.Vector2(0, 0), 5, 8)
    pass


if __name__ == "__main__":
    main()