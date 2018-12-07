from random import choice

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker


# TODO: remove global value
_monorems_joint_energy = 0


class Monorem(Attacker):
    __slots__ = ()

    _default_energy = 10
    _multiplication_cost = 5
    _energy_limit = 20
    _movement_cost = 0
    _energy_from_prey = None

    def _next_tick(self):
        self.energy += 1

        if self.is_near(Air) and self.can_multiply():
            cell = choice(self.find_near(Air)).pos
            self.multiply(cell)

        elif self.is_near(Grass) and self.can_multiply() and self.energy >= self._default_energy + self._multiplication_cost + 1:
            cell = choice(self.find_near(Grass)).pos
            self.kill(cell)
            self.multiply(cell)

        elif self.is_near(Air, Grass):
            cell = choice(self.find_near(Air, Grass)).pos
            self.move(cell)

    @property
    def energy(self):
        if not hasattr(self, "_game_logic"):
            return self._default_energy
        return _monorems_joint_energy/self._game_logic.count_kind(type(self))

    @energy.setter
    def energy(self, value):
        global _monorems_joint_energy
        _monorems_joint_energy -= self.energy
        _monorems_joint_energy += value
        if hasattr(self, "_game_logic"):
            if self.energy > self._energy_limit:
                _monorems_joint_energy = self._energy_limit * self._game_logic.count_kind(type(self))
