from random import choice

from entities.air import Air
from entities.mob import Mob


class Grass(Mob):
    __slots__ = ()

    _default_energy = 4
    energy_limit = 10
    _energy_increment_per_tick = 1

    def _next_tick(self):
        if self._do_multiply_on(Air) and self._is_near(Air):
            pos = choice(self._find_near(Air)).pos
            self._multiply(pos)
