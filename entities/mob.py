from abc import ABCMeta, abstractmethod

from entities.entity import Entity
from entities.air import Air


class Mob(Entity, metaclass=ABCMeta):
    __slots__ = ("_energy",)

    @abstractmethod
    def _next_tick(self):
        pass

    @abstractmethod
    def _default_energy(self):
        pass

    @abstractmethod
    def _multiplication_cost(self):
        pass

    @abstractmethod
    def _energy_limit(self):
        pass

    @abstractmethod
    def _energy_increment_per_tick(self):
        pass

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        if self._energy > self._energy_limit:
            self._energy = self._energy_limit

    def __init__(self):
        super().__init__()
        self.energy = self._default_energy

    def spawn(self, kind, pos):
        if not isinstance(self._game_logic.get_entity_by_pos(pos), Air):
            raise ValueError("Is not empty cell: %s" % pos)
        self._game_logic.replace(pos, kind)

    def kill(self, value):
        if not isinstance(value, Entity):
            value = self._game_logic.get_entity_by_pos(value)
        if isinstance(value, Mob):
            if value.energy > 0:
                value.energy = 0
        self._game_logic.replace(value, Air)

    def can_multiply(self):
        return self.energy >= self._default_energy + self._multiplication_cost

    def multiply(self, pos):
        self.spawn(type(self), pos)
        self.energy -= self._multiplication_cost

    def next_tick(self):
        self.energy += self._energy_increment_per_tick
        self._next_tick()
        if self.alive and self.energy <= 0:
            self.kill(self)
