from random import choice

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker


class Xotaker(Attacker):
    __slots__ = ()

    _default_energy = 2
    _energy_limit = 4
    _energy_increment_per_tick = 0
    _movement_cost = 0.1
    _energy_from_prey = 0.2

    def _next_tick(self):
        if self._do_multiply_on(Air) and self._is_near(Air):
            cell = choice(self._find_near(Air)).pos
            self._multiply(cell)

        elif self._do_multiply_on(Grass) and self._is_near(Grass):
            cell = choice(self._find_near(Grass)).pos
            old_pos = self.pos
            self._eat(cell)
            self._multiply(old_pos)

        elif self._is_near(Grass):
            cell = choice(self._find_near(Grass)).pos
            self._eat(cell)

        elif self._is_near(Air):
            cell = choice(self._find_near(Air)).pos
            self._move(cell)

    def _do_multiply_on(self, kind):
        if kind is Grass:
            return self.energy == self._energy_limit
        return super()._do_multiply_on(kind)
