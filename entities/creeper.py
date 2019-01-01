from random import choice, sample

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker
from entities.monorem import Monorem


class Creeper(Attacker):
    __slots__ = ()

    _default_energy = 20
    _multiplication_cost = 3
    _energy_limit = 27
    _energy_increment_per_tick = 0
    _movement_cost = 0.1
    _energy_from_prey = 1
    _bang_radius = 5
    _children_per_multiplication = 6

    def _next_tick(self):
        if self._do_multiply_on(Air):
            self.bang()
            available_air = self._game_logic.get_entities_in_region(self.pos, self._bang_radius)
            children_count = min(self._children_per_multiplication, len(available_air))
            air_to_spawn_on = sample(available_air, children_count)
            for air in air_to_spawn_on:
                self.spawn(Creeper, air.pos)

        elif self.is_near(Monorem):
            cell = choice(self.find_near(Monorem)).pos
            self.eat(cell)

        elif self.is_near(Air, Grass):
            cell = choice(self.find_near(Air, Grass)).pos
            self.move(cell)

    def bang(self):
        damaged_entities = self._game_logic.get_entities_in_region(self.pos, self._bang_radius)
        for entity in damaged_entities:
            self.kill(entity)
