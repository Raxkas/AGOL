from abc import ABCMeta, abstractmethod


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

    def _set_cells_content(self, cells_content):
        for cell, content in zip(self.cells, cells_content):
            self.set_cell_content(cell, content)

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
        pass


class MakeMutable:

    def __init__(self, world):
        self._world = world

    def __enter__(self):
        self._world.make_mutable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._world.make_immutable()
