from collections import namedtuple
from itertools import accumulate
from operator import mul
from random import random, randrange


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
        # random.shuffle is not something AGOL needed
        width = self.size.x
        area = mul(*self.size)
        for _ in range(area):
            i = randrange(area)
            x, y = i % width, i // width
            entity = self._matrix[y][x]
            if entity.is_alive:
                entity.next_tick()
        self.tick_number += 1

    def is_pos_correct(self, pos):
        x, y = pos
        return 0 <= x < self.size.x and 0 <= y < self.size.y

    def get_entity_by_pos(self, pos):
        x, y = pos
        return self._matrix[y][x]

    def replace(self, pos, kind):
        x, y = pos
        old_entity = self.get_entity_by_pos(pos)
        if old_entity is not None:
            self._matrix[y][x] = None
            self._kinds_arrays[type(old_entity)].remove(old_entity)
            old_entity.is_alive = False
        new_entity = kind.__new__(kind)
        self._matrix[y][x] = new_entity
        self._kinds_arrays[kind].append(new_entity)
        new_entity.__init__(game_logic=self, pos=pos)
        new_entity.is_alive = True

    def swap(self, pos1, pos2):
        entity1, entity2 = map(self.get_entity_by_pos, [pos1, pos2])
        entity1.pos, entity2.pos = pos2, pos1
        (x1, y1), (x2, y2) = pos1, pos2
        self._matrix[y1][x1], self._matrix[y2][x2] = entity2, entity1

    def get_entities_in_region(self, pos, radius):
        x, y = pos
        x_min, x_max = x-radius, x+radius
        y_min, y_max = y-radius, y+radius
        x_slice = slice(
            max(x_min, 0),
            min(x_max+1, self.size.x)
        )
        y_slice = slice(
            max(y_min, 0),
            min(y_max+1, self.size.y)
        )
        rows = self._matrix[y_slice]
        entities_rows = map(lambda row: row[x_slice], rows)
        return sum(entities_rows, [])

    def count_kind(self, kind):
        return len(self._kinds_arrays[kind])
