from abc import ABCMeta, abstractmethod

from entities.entity import Entity
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
    def _energy_limit(self):
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
        if self._energy > self._energy_limit:
            self._energy = self._energy_limit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def _do_multiply_on(self, kind):
        if kind is Air:
            return self.energy >= 2*self._default_energy
        return False

    def multiply(self, pos):
        self.spawn(type(self), pos)
        self.energy -= self._default_energy

    def next_tick(self):
        self.energy += self._energy_increment_per_tick
        self._next_tick()
        if self.is_alive and self.energy <= 0:
            self.kill(self)
