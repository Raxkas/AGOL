from collections.abc import Sequence
from random import random


# TODO: use itertools.accumulate
def _getRandomOf(kinds, spawnChances):
    assert len(kinds) == len(spawnChances)
    chancesSum = sum(spawnChances)
    seed = random() * chancesSum
    passedChancesSum = 0
    for kind, chance in zip(kinds, spawnChances):
        passedChancesSum += chance
        if passedChancesSum > seed:
            return kind


class AGOLLogic:
    def __init__(self, width, height, kinds, spawnChances):
        self.width = width
        self.height = height
        self._KINDS = tuple(kinds)
        self._ARRAYS = tuple(list() for kind in self._KINDS)
        self._matrix = []
        for y in range(self.height):
            row = [None] * self.width
            self._matrix.append(row)
        self._generateEntities(spawnChances)
        self.tickNumber = 0

    def _generateEntities(self, spawnChances):
        for y in range(self.height):
            for x in range(self.width):
                kind = _getRandomOf(self._KINDS, spawnChances)
                self.replace((x, y), kind)

    def nextTick(self):
        entities = sum(self._ARRAYS, [])
        for entity in entities:
            if entity.alive:
                entity.next_tick()
        self.tickNumber += 1

    def isPosCorrect(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def getEntityByPos(self, pos):
        if not self.isPosCorrect(pos):
            raise ValueError("Incorrect pos: " + pos)
        x, y = pos
        return self._matrix[y][x]

    def replace(self, value, kind):
        oldEntity = self._getEntityBy(value)
        if value is oldEntity:
            pos = oldEntity.pos
        else:
            pos = value
        x, y = pos

        if oldEntity is not None:
            self._matrix[y][x] = None
            self.getArrayBy(oldEntity).remove(oldEntity)
            oldEntity.alive = False

        newEntity = kind()
        newEntity.pos = pos
        newEntity._game_logic = self
        self._matrix[y][x] = newEntity
        self.getArrayBy(newEntity).append(newEntity)
        newEntity.alive = True

    def swap(self, value1, value2):
        entity1, entity2 = map(self._getEntityBy, [value1, value2])
        pos1, pos2 = entity1.pos, entity2.pos
        entity1.pos, entity2.pos = pos2, pos1
        (x1, y1), (x2, y2) = pos1, pos2
        self._matrix[y1][x1], self._matrix[y2][x2] = entity2, entity1

    def getArrayBy(self, value):
        id = self._getId(value)
        return self._ARRAYS[id]

    def _getId(self, value):
        if value in self._ARRAYS:
            return self._ARRAYS.index(value)
        elif value in self._KINDS:
            return self._KINDS.index(value)
        elif type(value) in self._KINDS:
            return self._KINDS.index(type(value))
        elif isinstance(value, Sequence):
            return self.getEntityByPos(value)
        else:
            raise TypeError("Incorrect value: %s" % value)

    def _getEntityBy(self, value):
        if type(value) in self._KINDS:
            if not value.alive:
                raise AssertionError("Dead entity")
            return value
        else:
            return self.getEntityByPos(value)

    def count(self, kind):
        return len(self.getArrayBy(kind))
