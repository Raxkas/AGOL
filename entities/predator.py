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
            pos = choice(self._find_near(Air)).pos
            self._multiply(pos)

        elif self._is_near(Xotaker):
            pos = choice(self._find_near(Xotaker)).pos
            self._eat(pos)

        elif self._is_near(Air, Grass):
            pos = choice(self._find_near(Air, Grass)).pos
            self._move(pos)
