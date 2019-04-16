from random import choice

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker


class Xotaker(Attacker):
    __slots__ = ()

    _default_energy = 2
    energy_limit = 4
    _energy_increment_per_tick = 0
    _movement_cost = 0.1
    _energy_from_prey = 0.2

    def _next_tick(self):
        if self._do_multiply_on(Air) and self._is_near(Air):
            pos = choice(self._find_near(Air)).pos
            self._multiply(pos)

        elif self._do_multiply_on(Grass) and self._is_near(Grass):
            pos = choice(self._find_near(Grass)).pos
            old_pos = self.pos
            self._eat(pos)
            self._multiply(old_pos)

        elif self._is_near(Grass):
            pos = choice(self._find_near(Grass)).pos
            self._eat(pos)

        elif self._is_near(Air):
            pos = choice(self._find_near(Air)).pos
            self._move(pos)

    def _do_multiply_on(self, kind):
        if kind is Grass:
            return self.energy >= 2*self._default_energy
        return super()._do_multiply_on(kind)
