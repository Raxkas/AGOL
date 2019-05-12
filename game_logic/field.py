from collections import namedtuple
from itertools import accumulate, product
from random import random

from game_logic.matrix import Matrix


class Field:

    _Size = namedtuple("Size", "x y")

    # TODO: custom neighbors rule
    def __init__(self, *, agol_logic, size, spawn_chances):
        self._agol_logic = agol_logic  # TODO: remove knowledge about kernel?
        self.size = self._Size(*size)
        self.__matrix = Matrix(size=self.size)  # TODO: NullEntity?
        self._generate_entities(spawn_chances=spawn_chances)

    def pos_exists(self, pos):
        x, y = pos
        return 0 <= x < self.size.x and 0 <= y < self.size.y

    @property
    def area(self):
        return self.size.x * self.size.y

    def swap(self, pos_1, pos_2):
        pos_1, pos_2 = tuple(pos_1), tuple(pos_2)
        entity_1, entity_2 = self[pos_1], self[pos_2]
        self._set_entity(pos=pos_1, entity=entity_2)
        self._set_entity(pos=pos_2, entity=entity_1)

    def replace(self, pos, kind):
        self._agol_logic.remove_entity(self[pos])
        self._spawn_entity(kind, pos)

    # TODO: replace with get_entity?
    def __getitem__(self, pos):
        return self.__matrix[pos]

    def _set_entity(self, *, pos, entity):
        pos = tuple(pos)
        self.__matrix[pos] = entity
        entity.pos = pos

    def _spawn_entity(self, kind, pos):
        entity = kind(agol_kernel=self._agol_logic, field=self)
        self._set_entity(pos=pos, entity=entity)

    def get_entities_in_area(self, pos, radius):
        sides = []
        for axis_index, value in enumerate(pos):
            min_, max_ = value - radius, value + radius
            side = range(min_, max_+1)
            side = map(lambda v: v % self.size[axis_index], side)
            sides.append(side)
        positions_in_region = product(*sides)
        return list(map(self.__getitem__, positions_in_region))

    # TODO: move out
    def _generate_entities(self, spawn_chances):
        for y in range(self.size.y):
            for x in range(self.size.x):
                kind = self._choice_random_kind(self._agol_logic.kinds, spawn_chances)
                self._spawn_entity(kind, (x, y))

    @staticmethod
    def _choice_random_kind(kinds, spawn_chances):
        assert len(kinds) == len(spawn_chances)
        chances_sum = sum(spawn_chances)
        seed = random() * chances_sum
        for kind, passed_chances_sum in zip(kinds, accumulate(spawn_chances)):
            if passed_chances_sum > seed:
                return kind
