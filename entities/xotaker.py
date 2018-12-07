from random import choice

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker


class Xotaker(Attacker):
    __slots__ = ()

    _default_energy = 2
    _multiplication_cost = 2
    _energy_limit = 4
    _movement_cost = 0.1
    _energy_from_prey = 0.2

    def _next_tick(self):
        if self.is_near(Air) and self.can_multiply():
            cell = choice(self.find_near(Air)).pos
            self.multiply(cell)

        elif self.is_near(Grass) and self.can_multiply() and self.energy == self._energy_limit:
            cell = choice(self.find_near(Grass)).pos
            old_pos = self.pos
            self.eat(cell)
            self.multiply(old_pos)

        elif self.is_near(Grass):
            cell = choice(self.find_near(Grass)).pos
            self.eat(cell)

        elif self.is_near(Air):
            cell = choice(self.find_near(Air)).pos
            self.move(cell)
