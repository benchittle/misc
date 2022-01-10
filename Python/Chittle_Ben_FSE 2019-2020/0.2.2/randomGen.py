import random


class Sub:
    def __init__(self, size=7):
        self.size = size
        self.w = size
        self.h = size
        self.grid = [[None] * self.size for i in range(self.size)]

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col] = random.choices(["blank", Tile(self, row, col)], weights=[4, 1])[0]


    def adjacent_tiles(self, row, col):
        tiles = {}
        coords = {
            "s" : (row + 1, col),
            "n" : (row - 1, col),
            "e" : (row, col + 1),
            "w" : (row, col - 1)
            }

        for direction, (row, col) in coords.items():
            if 0 <= row <= self.w and 0 <= col <= self.h:
                tiles[direction] = self.grid[row][col]
            else:
                tiles[direction] = None

        return tiles



    def output(self):
        for row in self.grid:
            print(row)

    @property
    def columns(self):
        return [[self.grid[row][col] for row in range(len(self.grid))] for col in range(len(self.grid[0]))]

    @property
    def rows(self):
        return self.grid()








class Tile:
    def __init__(self, sub, row, col):
        self.sub = sub
        self.row = row
        self.col = col

    def __str__(self):
        return "({}, {})".format(self.row, self.col)

    def __repr__(self):
        return self.__str__()




sub1 = Sub()
sub1.output()
print()
print(sub1.adjacent_tiles(0, 1))
#print(sub1.columns)