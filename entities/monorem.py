from random import choice

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker


# TODO: remove global value
_monorems_joint_energy = 0


class Monorem(Attacker):
    __slots__ = ()

    _default_energy = 5
    _energy_limit = 20
    _energy_increment_per_tick = 1
    _movement_cost = 0
    _energy_from_prey = None

    def _next_tick(self):
        if self._do_multiply_on(Air) and self.is_near(Air):
            cell = choice(self.find_near(Air)).pos
            self.multiply(cell)

        elif self._do_multiply_on(Grass) and self.is_near(Grass):
            cell = choice(self.find_near(Grass)).pos
            self.kill(cell)
            self.multiply(cell)

        elif self.is_near(Air, Grass):
            cell = choice(self.find_near(Air, Grass)).pos
            self.move(cell)

    def _do_multiply_on(self, kind):
        if kind is Grass:
            return self.energy >= 2*self._default_energy + self._energy_increment_per_tick
        return super()._do_multiply_on(kind)

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
