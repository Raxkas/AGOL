from random import Random
from typing import Any, Dict, Tuple

from base.simulation import Simulation
from base.world import MakeMutable


_InputData = Dict[str, Any]
_OutputData = Dict[str, Any]


class AGOLSimulation(Simulation):

    def __init__(self, *, world_type, world_params, seed,
                 do_generate_entities=False, spawn_chances_by_kinds=None):
        self._world = world_type(**world_params)
        random_for_seeds = Random(seed)
        self._random_for_entity_choosing = Random(random_for_seeds.random())
        self._random_for_entities = Random(random_for_seeds.random())
        if not do_generate_entities:
            if spawn_chances_by_kinds is not None:
                raise TypeError("spawn_chances_by_kinds "
                                "should not be specified "
                                "if do_generate_entities is not True")
        if do_generate_entities:
            random_for_generation = Random(random_for_seeds.random())
            with MakeMutable(self._world):
                self._generate_entities(
                    self._world,
                    spawn_chances_by_kinds, random_for_generation
                )

    @classmethod
    def initial_next_tick(cls, input_data: _InputData) -> \
            Tuple["AGOLSimulation", _OutputData]:
        simulation = cls(**input_data)
        return simulation, {"world": simulation._world}

    def next_tick(self, input_data: _InputData) -> _OutputData:
        if input_data:
            raise TypeError("non-initial input_data should be empty")

        world = self._world
        cell = self._random_for_entity_choosing.choice(world.cells)
        entity = world.get_cell_content(cell)
        action = entity.next_tick(self._random_for_entities)
        with MakeMutable(world):
            action.apply()
        # TODO: should not be able to change world returned in output
        # TODO: maybe should return only changes
        return {"world": world}

    @staticmethod
    def _generate_entities(world, spawn_chances_by_kinds, random):
        kinds, spawn_chances = zip(*spawn_chances_by_kinds.items())
        for cell in world.cells:
            if world.get_cell_content(cell) is None:
                entity = random.choices(kinds, spawn_chances)[0](world=world)
                world.set_cell_content(cell, entity)
