class Room:
    def __init__(self, tile, string):
        self.tile = tile
        self.build(string)


    def build(self, string):
        """
        String goes 'nesw', where each letter is replaced with either:
        d - door
        f - full
        n - none
        """


