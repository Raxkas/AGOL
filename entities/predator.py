from random import choice

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker
from entities.xotaker import Xotaker


class Predator(Attacker):
    __slots__ = ()

    _default_energy = 3
    _energy_limit = 20
    _energy_increment_per_tick = 0
    _movement_cost = 0.05
    _energy_from_prey = 1

    def _next_tick(self):
        if self._do_multiply_on(Air) and self._is_near(Air):
            cell = choice(self._find_near(Air)).pos
            self._multiply(cell)

        elif self._is_near(Xotaker):
            cell = choice(self._find_near(Xotaker)).pos
            self._eat(cell)

        elif self._is_near(Air, Grass):
            cell = choice(self._find_near(Air, Grass)).pos
            self._move(cell)
