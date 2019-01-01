from collections import namedtuple
from itertools import accumulate
from random import random


_Size = namedtuple("Size", "x y")


# TODO: rename
class AGOLLogic:
    def __init__(self, width, height, kinds, spawn_chances):
        self.size = _Size(width, height)
        self.kinds = tuple(kinds)
        self._kinds_arrays = {kind: list() for kind in self.kinds}
        self._matrix = [[None] * self.size.x  # row
                        for y in range(self.size.y)]
        self._generate_entities(spawn_chances)
        self.tick_number = 0

    def _generate_entities(self, spawn_chances):
        for y in range(self.size.y):
            for x in range(self.size.x):
                kind = self._choice_random_kind(self.kinds, spawn_chances)
                self.replace((x, y), kind)

    @staticmethod
    def _choice_random_kind(kinds, spawn_chances):
        assert len(kinds) == len(spawn_chances)
        chances_sum = sum(spawn_chances)
        seed = random() * chances_sum
        for kind, passed_chances_sum in zip(kinds, accumulate(spawn_chances)):
            if passed_chances_sum > seed:
                return kind

    def next_tick(self):
        entities = sum(self._kinds_arrays.values(), [])
        for entity in entities:
            if entity.alive:
                entity.next_tick()
        self.tick_number += 1

    def is_pos_correct(self, pos):
        x, y = pos
        return 0 <= x < self.size.x and 0 <= y < self.size.y

    def get_entity_by_pos(self, pos):
        x, y = pos
        return self._matrix[y][x]

    def replace(self, value, kind):
        old_entity = self._get_entity_by(value)
        if value is old_entity:
            pos = old_entity.pos
        else:
            pos = value
        x, y = pos

        if old_entity is not None:
            self._matrix[y][x] = None
            self._kinds_arrays[type(old_entity)].remove(old_entity)
            old_entity.alive = False
        new_entity = kind.__new__(kind)
        self._matrix[y][x] = new_entity
        self._kinds_arrays[kind].append(new_entity)
        new_entity.__init__(game_logic=self, pos=pos)
        new_entity.alive = True

    def swap(self, value1, value2):
        entity1, entity2 = map(self._get_entity_by, [value1, value2])
        pos1, pos2 = entity1.pos, entity2.pos
        entity1.pos, entity2.pos = pos2, pos1
        (x1, y1), (x2, y2) = pos1, pos2
        self._matrix[y1][x1], self._matrix[y2][x2] = entity2, entity1

    def get_entities_in_region(self, pos, radius):
        x, y = pos
        x_slice = slice(
            max(x - radius, 0),
            min(x + radius, self.size.x - 1) + 1
        )
        y_slice = slice(
            max(y - radius, 0),
            min(y + radius, self.size.y - 1) + 1
        )
        rows = self._matrix[y_slice]
        entities_rows = map(lambda row: row[x_slice], rows)
        return sum(entities_rows, [])

    def _get_entity_by(self, value):
        if type(value) in self.kinds:
            if not value.alive:
                raise AssertionError("Dead entity")
            return value
        else:
            return self.get_entity_by_pos(value)

    def count_kind(self, kind):
        return len(self._kinds_arrays[kind])
