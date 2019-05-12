from abc import ABCMeta, abstractmethod

from entities.mob import Mob


class Attacker(Mob, metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def _movement_cost(self):
        pass

    @property
    @abstractmethod
    def _energy_from_prey(self):
        pass

    def _move(self, pos):
        self.field.swap(self.pos, pos)
        self.energy -= self._movement_cost

    def _eat(self, pos):
        self._kill(pos)
        self.field.swap(self.pos, pos)
        self.energy += self._energy_from_prey
