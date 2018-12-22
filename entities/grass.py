from random import choice

from entities.air import Air
from entities.mob import Mob


class Grass(Mob):
    __slots__ = ()

    _default_energy = 1
    _multiplication_cost = 4
    _energy_limit = 10
    _energy_increment_per_tick = 1

    def _next_tick(self):
        if self.can_multiply() and self.is_near(Air):
            cell = choice(self.find_near(Air)).pos
            self.multiply(cell)
