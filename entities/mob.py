from abc import ABCMeta, abstractmethod

from game_logic.entity import Entity
from entities.air import Air


class Mob(Entity, metaclass=ABCMeta):
    __slots__ = ("_energy",)

    @abstractmethod
    def _next_tick(self):
        pass

    @property
    @abstractmethod
    def _default_energy(self):
        pass

    @property
    @abstractmethod
    def energy_limit(self):
        pass

    @property
    @abstractmethod
    def _energy_increment_per_tick(self):
        pass

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        if self._energy > self.energy_limit:
            self._energy = self.energy_limit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.energy = self._default_energy

    @property
    def __adjacent_entities(self):
        entities = self.field.get_entities_in_area(self.pos, 1)
        entities.remove(self)
        return entities

    def _is_near(self, *kinds_needed):
        kinds_near = frozenset(map(type, self.__adjacent_entities))
        return any(map(lambda kind: issubclass(kind, kinds_needed), kinds_near))

    def _find_near(self, *kinds):
        found = filter(lambda entity: isinstance(entity, kinds), self.__adjacent_entities)
        return tuple(found)

    def _spawn(self, kind, pos):
        if not isinstance(self.field[pos], Air):
            raise ValueError("Is not empty cell: %s" % pos)
        self.field.replace(pos, kind)

    def _kill(self, value):
        if not isinstance(value, Entity):
            value = self.field[value]
        entity = value
        if isinstance(entity, Mob):
            if entity.energy > 0:
                entity.energy = 0
        self.field.replace(entity.pos, Air)

    def _do_multiply_on(self, kind):
        if kind is Air:
            return self.energy >= 2*self._default_energy
        return False

    def _multiply(self, pos):
        self._spawn(type(self), pos)
        self.energy -= self._default_energy

    def next_tick(self):
        self.energy += self._energy_increment_per_tick
        self._next_tick()
        if self.energy <= 0:
            self._kill(self)
