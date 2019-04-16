from random import choice

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker


class Monorem(Attacker):
    __slots__ = ()

    _default_energy = 15
    energy_limit = 40
    _energy_increment_per_tick = 1
    _movement_cost = 0
    _energy_from_prey = None

    def _next_tick(self):
        if self._do_multiply_on(Air) and self._is_near(Air):
            pos = choice(self._find_near(Air)).pos
            self._multiply(pos)

        elif self._do_multiply_on(Grass) and self._is_near(Grass):
            pos = choice(self._find_near(Grass)).pos
            self._kill(pos)
            self._multiply(pos)

        elif self._is_near(Air, Grass):
            pos = choice(self._find_near(Air, Grass)).pos
            self._move(pos)

    def _do_multiply_on(self, kind):
        if kind is Grass:
            return self.energy >= 2*self._default_energy + self._energy_increment_per_tick
        return super()._do_multiply_on(kind)
