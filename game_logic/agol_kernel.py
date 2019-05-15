from random import choice

from game_logic.field import Field


class AGOLKernel:

    def __init__(self, field_size, kinds, spawn_chances):
        self.kinds = tuple(kinds)
        self._entities = []
        self._kinds_arrays = {kind: list() for kind in self.kinds}  # TODO: rename
        self.ticks_since_start = 0
        self.field = Field(size=field_size, agol_kernel=self, spawn_chances=spawn_chances)

    def next_tick(self):
        entity = choice(self._entities)
        entity.next_tick()
        self.ticks_since_start += 1

    def add_entity(self, entity):
        self._entities.append(entity)
        self._kinds_arrays[type(entity)].append(entity)

    def remove_entity(self, entity):
        self._entities.remove(entity)
        self._kinds_arrays[type(entity)].remove(entity)

    def count_entities(self):
        return len(self._entities)

    def count_kind(self, kind):
        return len(self._kinds_arrays[kind])
