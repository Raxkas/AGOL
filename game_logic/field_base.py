from collections import namedtuple


_Size = namedtuple("Size", "x y")


class FieldBase:
    def __init__(self, width, height):
        self.size = _Size(width, height)
        self.__matrix = [[None] * self.size.x  # row
                         for y in range(self.size.y)]

    def is_pos_correct(self, pos):
        x, y = pos
        return 0 <= x < self.size.x and 0 <= y < self.size.y

    def __getitem__(self, pos):
        x, y = pos
        return self.__matrix[y][x]

    def __setitem__(self, pos, value):
        x, y = pos
        self.__matrix[y][x] = value

    def swap(self, pos1, pos2):
        self[pos1], self[pos2] = self[pos2], self[pos1]
