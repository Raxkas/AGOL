from collections import namedtuple
from functools import lru_cache
from itertools import product

from base.world import World


class Field(World):
    # TODO: doc

    _Size = namedtuple("Size", "x y")

    def __init__(self, *, size):
        super().__init__()
        size = tuple(size)
        if len(size) != 2:
            raise IndexError("Field size consists of 2 elements")
        if set(map(type, size)) != {int}:
            raise TypeError("Field size consists of int objects")
        self.size = self._Size(*size)
        size_x, size_y = size
        self._cells_content = tuple(
            [None] * size_x for y in range(size_y)
        )
        cells = product(range(size_x), range(size_y))
        cells = self.__get_sorted_cells(cells)
        cells = tuple(cells)
        self._cells = cells

    @property
    def cells(self):
        return self._cells

    @staticmethod
    def __get_sorted_cells(cells):
        return sorted(cells, key=lambda cell: (cell[1], cell[0]))

    # TODO: maybe should be implemented in subclasses
    #       or depending on special property "neighbors_pattern"
    # TODO: maybe should precompute and use 2d list instead of dict
    @lru_cache(maxsize=None)
    def get_adjacent_cells(self, cell):
        x, y = cell
        size_x, size_y = self.size
        neighbors_offsets = product(range(-1, +1 + 1), repeat=2)
        neighbors_offsets = self.__get_sorted_cells(neighbors_offsets)
        result = tuple(
            ((x + dx) % size_x, (y + dy) % size_y)
            for dx, dy in neighbors_offsets
        )
        return result

    def get_cell_content(self, cell):
        x, y = cell
        return self._cells_content[y][x]

    def set_cell_content(self, cell, new_content):
        super().set_cell_content(cell, new_content)
        x, y = cell
        self._cells_content[y][x] = new_content
