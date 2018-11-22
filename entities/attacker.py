from abc import ABCMeta, abstractmethod

from entities.air import Air
from entities.mob import Mob


class Attacker(Mob, metaclass=ABCMeta):
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
        self._game_logic.replace(pos, Air)
        self._game_logic.swap(self, pos)
        self.energy += self._energy_from_prey
