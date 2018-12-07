from itertools import accumulate
from collections import namedtuple
from collections.abc import Sequence
from random import random


def _get_random_of(kinds, spawn_chances):
    assert len(kinds) == len(spawn_chances)
    chances_sum = sum(spawn_chances)
    seed = random() * chances_sum
    for kind, passed_chances_sum in zip(kinds, accumulate(spawn_chances)):
        if passed_chances_sum > seed:
            return kind


_Size = namedtuple("Size", "x y")


# TODO: rename
class AGOLLogic:
    def __init__(self, width, height, kinds, spawn_chances):
        self.size = _Size(width, height)
        self.kinds = tuple(kinds)
        self._arrays = tuple(list() for kind in self.kinds)
        self._matrix = []
        for y in range(self.size.y):
            row = [None] * self.size.x
            self._matrix.append(row)
        self._generate_entities(spawn_chances)
        self.tick_number = 0

    def _generate_entities(self, spawn_chances):
        for y in range(self.size.y):
            for x in range(self.size.x):
                kind = _get_random_of(self.kinds, spawn_chances)
                self.replace((x, y), kind)

    def next_tick(self):
        entities = sum(self._arrays, [])
        for entity in entities:
            if entity.alive:
                entity.next_tick()
        self.tick_number += 1

    def is_pos_correct(self, pos):
        x, y = pos
        return 0 <= x < self.size.x and 0 <= y < self.size.y

    def get_entity_by_pos(self, pos):
        if not self.is_pos_correct(pos):
            raise ValueError("Incorrect pos: " + pos)
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
            self._get_array_by(old_entity).remove(old_entity)
            old_entity.alive = False

        new_entity = kind()
        new_entity.pos = pos
        new_entity._game_logic = self
        self._matrix[y][x] = new_entity
        self._get_array_by(new_entity).append(new_entity)
        new_entity.alive = True

    def swap(self, value1, value2):
        entity1, entity2 = map(self._get_entity_by, [value1, value2])
        pos1, pos2 = entity1.pos, entity2.pos
        entity1.pos, entity2.pos = pos2, pos1
        (x1, y1), (x2, y2) = pos1, pos2
        self._matrix[y1][x1], self._matrix[y2][x2] = entity2, entity1

    def _get_array_by(self, value):
        id = self._get_id(value)
        return self._arrays[id]

    def _get_id(self, value):
        if value in self._arrays:
            return self._arrays.index(value)
        elif value in self.kinds:
            return self.kinds.index(value)
        elif type(value) in self.kinds:
            return self.kinds.index(type(value))
        elif isinstance(value, Sequence):
            return self.get_entity_by_pos(value)
        else:
            raise TypeError("Incorrect value: %s" % value)

    def _get_entity_by(self, value):
        if type(value) in self.kinds:
            if not value.alive:
                raise AssertionError("Dead entity")
            return value
        else:
            return self.get_entity_by_pos(value)

    def count_kind(self, kind):
        return len(self._get_array_by(kind))
