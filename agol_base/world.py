from abc import ABCMeta, abstractmethod


class World(metaclass=ABCMeta):
    """Superclass of any type of world.

    Any world is graph. Vertices are cells, edges are cell joints.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @classmethod
    def create(cls, *, generate_cells_content, **kwargs):
        new_world = cls(**kwargs)
        cells_content = generate_cells_content(new_world)
        new_world._set_cells_content(cells_content)
        return new_world

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
