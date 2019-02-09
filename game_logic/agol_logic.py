from itertools import accumulate, product
from operator import mul
from random import random, randrange

from game_logic.field_base import FieldBase


# TODO: rename
class AGOLLogic(FieldBase):
    def __init__(self, width, height, kinds, spawn_chances):
        super().__init__(width, height)
        self.kinds = tuple(kinds)
        self._kinds_arrays = {kind: list() for kind in self.kinds}
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
        width = self.size.x
        area = mul(*self.size)
        i = randrange(area)
        x, y = i % width, i // width
        entity = self[x, y]
        entity.next_tick()
        self.tick_number += 1

    def get_entity_by_pos(self, pos):
        return self[pos]

    def replace(self, pos, kind):
        x, y = pos
        old_entity = self.get_entity_by_pos(pos)
        if old_entity is not None:
            self[x, y] = None
            self._kinds_arrays[type(old_entity)].remove(old_entity)
            old_entity.is_alive = False
        new_entity = kind.__new__(kind)
        self[x, y] = new_entity
        self._kinds_arrays[kind].append(new_entity)
        new_entity.__init__(game_logic=self, pos=pos)
        new_entity.is_alive = True

    def swap(self, pos1, pos2):
        entity1, entity2 = map(self.get_entity_by_pos, [pos1, pos2])
        entity1.pos, entity2.pos = pos2, pos1
        super().swap(pos1, pos2)

    def get_entities_in_region(self, pos, radius):
        sides = []
        for axis_index, value in enumerate(pos):
            min_, max_ = value - radius, value + radius
            side = range(min_, max_+1)
            side = map(lambda v: v % self.size[axis_index], side)
            sides.append(side)
        positions_in_region = product(*sides)
        return list(map(self.__getitem__, positions_in_region))

    def count_kind(self, kind):
        return len(self._kinds_arrays[kind])
