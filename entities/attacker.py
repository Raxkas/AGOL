from abc import ABCMeta, abstractmethod

from entities.mob import Mob


class Attacker(Mob, metaclass=ABCMeta):
    __slots__ = ()

    @abstractmethod
    def _movement_cost(self):
        pass

    @abstractmethod
    def _energy_from_prey(self):
        pass

    def move(self, pos):
        self._game_logic.swap(self, pos)
        self.energy -= self._movement_cost

    def eat(self, pos):
        self.kill(pos)
        self._game_logic.swap(self, pos)
        self.energy += self._energy_from_prey
