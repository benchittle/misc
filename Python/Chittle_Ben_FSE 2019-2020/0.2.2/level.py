import settings
import pygame as pg




class Wall:
    def __init__(self, position, kind):
        if type(position) == pg.Vector2:
            self.pos = position * 1
        else:
            self.pos = pg.Vector2(position)

        if kind == "vertical":
            self.vec = pg.Vector2(0, settings.ROOM_SIZE)
        elif kind == "horizontal":
            self.vec = pg.Vector2(settings.ROOM_SIZE, 0)
        else:
            raise ValueError("unrecognized value for <kind>: {}".format(kind))


    @classmethod
    def spawn_at_wall(cls, wall, loc, kind):
        new_wall = Wall((0, 0), kind)
        new_wall.connect_to(wall, loc)
        return new_wall

    def to_tuple(self):
        if self.vec.y == 0:
            return (self.pos.x, self.pos.y, self.vec.x, settings.WALL_WIDTH)
        elif self.vec.x == 0:
            return (self.pos.x, self.pos.y, settings.WALL_WIDTH, self.vec.y)
        else:
            raise NotImplementedError("diagonal walls are not implemented")


    @property
    def start(self):
        return self.pos * 1

    @property
    def end(self):
        return self.pos + self.vec

    @property
    def mid(self):
        return (self.start + self.end) / 2

    def __str__(self):
        return "Pos: ({}) || Vec: ({})".format(self.pos, self.vec)


    def join(self, wall, dim):
        if dim == "x":
            return Wall(self.pos, (self.vec.x + wall.vec.x, self.pos.y))
        elif dim == "y":
            return Wall(self.pos, (self.pos.x, self.vec.y + wall.vec.y))


    def split(self, gap=0):
        new_vec = self.vec * 1
        new_vec.scale_to_length((self.vec.magnitude() - gap) / 2)

        return Wall(self.pos, new_vec), Wall(self.pos + self.vec - new_vec, new_vec)


    def connect_to(self, wall, loc):
        if loc == "s":
            self.pos.update(wall.start)
        elif loc == "m":
            self.pos.update(wall.mid)
        elif loc == "e":
            self.pos.update(wall.end)
        else:
            raise ValueError("'{}' is not a recognized value for <loc>".format(loc))





















'''class Room:
    def __init__(self, x, y, doors):
        self.walls = {
            "top" : Wall((x, y), (settings.ROOM_SIZE, 0), settings.WALL_WIDTH),
            "left" : Wall((0, 0), (0, settings.ROOM_SIZE), settings.WALL_WIDTH),
            "right" : Wall((0, 0), (0, settings.ROOM_SIZE), settings.WALL_WIDTH),
            "bottom" : Wall((0, 0), (settings.ROOM_SIZE, 0), settings.WALL_WIDTH)
            }

        self.walls["left"].connect_to(self.walls["top"], "s")
        self.walls["right"].connect_to(self.walls["top"], "e")
        self.walls["bottom"].connect_to(self.walls["left"], "e")

        for i in doors:
            if i not in ["top", "left", "right", "bottom"]:
                raise ValueError("invalid element in <doors>: {}".format(i))

            self.walls[i].split(settings.DOOR_WIDTH)

    def to_list(self):
        return [i.to_tuple() for i in self.walls.values()]


'''











'''
class Wall:
    def __init__(self, position, vector, width):
        self.width = width
        if type(position) == pg.Vector2:
            self.pos = position * 1
        else:
            self.pos = pg.Vector2(position)

        if type(vector) == pg.Vector2:
            self.vec = vector * 1
        else:
            self.vec = pg.Vector2(vector)

        if self.vec.elementwise() < 0:
            raise ValueError("vec components must be greater than zero")

    def to_tuple(self):
        if self.vec.y == 0:
            return (self.pos.x, self.pos.y, self.vec.x, self.width)
        elif self.vec.x == 0:
            return (self.pos.x, self.pos.y, self.width, self.vec.y)
        else:
            raise NotImplementedError("diagonal walls are not implemented")


    @property
    def start(self):
        return self.pos * 1

    @property
    def end(self):
        return self.pos + self.vec

    @property
    def mid(self):
        return (self.start + self.end) / 2

    def __str__(self):
        return "Pos: ({}) || Vec: ({})".format(self.pos, self.vec)


    def join(self, wall, dim):
        if dim == "x":
            return Wall(self.pos, (self.vec.x + wall.vec.x, self.pos.y))
        elif dim == "y":
            return Wall(self.pos, (self.pos.x, self.vec.y + wall.vec.y))


    def split(self, gap=0):
        new_len = (self.vec.magnitude() - gap) / 2
        new_vec = self.vec * 1
        new_vec.scale_to_length(new_len)

        pos2 = self.pos + self.vec - new_vec

        return Wall(self.pos, new_vec), Wall(pos2, new_vec)


    def connect_to(self, wall, loc):
        if loc == "s":
            self.pos.update(wall.start)
        elif loc == "m":
            self.pos.update(wall.mid)
        elif loc == "e":
            self.pos.update(wall.end)
        else:
            raise ValueError("'{}' is not a recognized value for <loc>".format(loc))




class Room:
    def __init__(self, x, y, doors):
        self.walls = {
            "top" : Wall((x, y), (settings.ROOM_SIZE, 0), settings.WALL_WIDTH),
            "left" : Wall((0, 0), (0, settings.ROOM_SIZE), settings.WALL_WIDTH),
            "right" : Wall((0, 0), (0, settings.ROOM_SIZE), settings.WALL_WIDTH),
            "bottom" : Wall((0, 0), (settings.ROOM_SIZE, 0), settings.WALL_WIDTH)
            }

        self.walls["left"].connect_to(self.walls["top"], "s")
        self.walls["right"].connect_to(self.walls["top"], "e")
        self.walls["bottom"].connect_to(self.walls["left"], "e")

    def to_list(self):
        return [i.to_tuple() for i in self.walls.values()]



#w1 = Wall((0, 0), (100, 0))
#w2 = Wall((100, 0), (150, 0))
#w3 = Wall((0, 0), (0, 100))

#print(w1.join(w2))
#for i in w3.split(12):
#    print(i)

#print("Done")


'''






"""
class Group:
    def __init__(self, kind, length, data_struct=None):
        #Group.instances.append(self)
        self.kind = kind
        self.length = length
        if data_struct is not None:
            data_struct.append(self)

    def __str__(self):
        return "{}<{}>".format(self.length, self.kind)

    @staticmethod
    def collapse_string(string):
        group_list = []
        group = Group(string[0], 0, group_list)
        for char in string:
            if char == group.kind:
                group.length += 1
            else:
                group = Group(char, 1, group_list)

        return group_list


def parse_level_string(string):
    DIM_X = 10
    DIM_Y = 10
    # CHECK THIS IF DIM STUFF IS IMPLEMENTED
    rows = [string[i : i + DIM_X] for i in range(0, DIM_X * DIM_Y, DIM_X)]
    cols = [string[i::DIM_X] for i in range(DIM_Y)]

    row_groups = [] # List of group object eg [4<->, 2< >, 4<->]
    col_groups = []

    for row in rows:
        row_groups.append(Group.collapse_string(row))
    for col in cols:
        col_groups.append(Group.collapse_string(col))

    h_walls = []
    v_walls = []

    for y, row in enumerate(row_groups):
        x = 0
        for group in row:
            if group.kind == "-":
                wall = ()

                '''
                xpos = x / DIM_X * settings.ROOM_SCALE
                wall_length = group.length / DIM_X * settings.ROOM_SCALE
                h_walls.append(
                    (xpos + 1 / DIM_X * settings.ROOM_SCALE,# + wall_length / 3,
                    y / DIM_Y * settings.ROOM_SCALE,
                    wall_length + 80,
                    settings.WALL_WIDTH
                    ))
                '''

            x += group.length

    for x, col in enumerate(col_groups):
        y = 0
        for group in col:
            if group.kind == "|":


                '''
                ypos = y / DIM_Y * settings.ROOM_SCALE
                wall_height = group.length / DIM_Y * settings.ROOM_SCALE
                v_walls.append(
                    (x / DIM_X * settings.ROOM_SCALE,
                    ypos + 1 / DIM_Y * settings.ROOM_SCALE,# + wall_height / 3,
                    settings.WALL_WIDTH,
                    wall_height + 20
                    ))
                '''

            y += group.length
    print(v_walls + h_walls)
    return v_walls + h_walls



"""