from abc import ABCMeta, abstractmethod

from base.cell_content import CellContent


class World(metaclass=ABCMeta):
    """Superclass of any type of world.

    Any world is graph. Vertices are cells, edges are cell joints.
    """

    def __init__(self):
        self.is_mutable = None
        self.make_immutable()

    def make_immutable(self):
        if self.is_mutable is not None and not self.is_mutable:
            raise AssertionError("already immutable")
        self.is_mutable = False

    def make_mutable(self):
        if self.is_mutable is not None and self.is_mutable:
            raise AssertionError("already mutable")
        self.is_mutable = True

    @property
    @abstractmethod
    def cells(self):
        pass

    @property
    def cells_quantity(self):
        return len(self.cells)

    @abstractmethod
    def get_adjacent_cells(self, cell):
        pass

    @abstractmethod
    def get_cell_content(self, cell):
        pass

    @abstractmethod
    def set_cell_content(self, cell, new_content):
        old_content = self.get_cell_content(cell)
        if isinstance(old_content, CellContent) and old_content.cell == cell:
            old_content.cell = None
        new_content.cell = cell

    def _set_cells_content(self, new_cells_content):
        if len(new_cells_content) != len(self.cells):
            raise ValueError("argument length must be equal cells amount")
        for cell, content in zip(self.cells, new_cells_content):
            self.set_cell_content(cell, content)


class MakeMutable:

    def __init__(self, world):
        self._world = world

    def __enter__(self):
        self._world.make_mutable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._world.make_immutable()
