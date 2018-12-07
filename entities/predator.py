from random import choice

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker
from entities.xotaker import Xotaker


class Predator(Attacker):
    __slots__ = ()

    _default_energy = 10
    _multiplication_cost = 3
    _energy_limit = 20
    _movement_cost = 0.1
    _energy_from_prey = 1

    def _next_tick(self):
        if self.is_near(Air) and self.can_multiply():
            cell = choice(self.find_near(Air)).pos
            self.multiply(cell)

        elif self.is_near(Xotaker):
            cell = choice(self.find_near(Xotaker)).pos
            self.eat(cell)

        elif self.is_near(Air, Grass):
            cell = choice(self.find_near(Air, Grass)).pos
            self.move(cell)
