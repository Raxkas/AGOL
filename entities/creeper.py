from random import choice, sample

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker
from entities.monorem import Monorem


class Creeper(Attacker):
    _default_energy = 20
    _multiplication_cost = 3
    _energy_limit = 27
    _movement_cost = 0.1
    _energy_from_prey = 1
    _bang_radius = 5
    _children_per_multiplication = 6

    def _next_tick(self):
        if self.can_multiply():
            self.bang()
            available_cells = list(self._get_area(self._bang_radius))
            cells_to_spawn = sample(available_cells, self._children_per_multiplication)
            for cell in cells_to_spawn:
                self.spawn(Creeper, cell)

        elif self.is_near(Monorem):
            cell = choice(self.find_near(Monorem)).pos
            self.eat(cell)

        elif self.is_near(Air, Grass):
            cell = choice(self.find_near(Air, Grass)).pos
            self.move(cell)

    def bang(self):
        damaged = self._get_area(self._bang_radius)
        for pos in damaged:
            self.kill(pos)
