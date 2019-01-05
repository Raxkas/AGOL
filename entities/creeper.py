from random import choice, sample

from entities.air import Air
from entities.grass import Grass
from entities.attacker import Attacker
from entities.monorem import Monorem


class Creeper(Attacker):
    __slots__ = ()

    _default_energy = 0.5
    _energy_limit = 4
    _energy_increment_per_tick = 0
    _movement_cost = 0.015
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
                self._spawn(Creeper, air.pos)

        elif self._is_near(Monorem):
            cell = choice(self._find_near(Monorem)).pos
            self._eat(cell)

        elif self._is_near(Air, Grass):
            cell = choice(self._find_near(Air, Grass)).pos
            self._move(cell)

    def bang(self):
        damaged_entities = self._game_logic.get_entities_in_region(self.pos, self._bang_radius)
        for entity in damaged_entities:
            self._kill(entity)

    def _do_multiply_on(self, kind):
        return self.energy >= self._default_energy * self._children_per_multiplication
