from abc import ABCMeta, abstractmethod
from typing import Iterable

from base.action import Action


class Tickable(metaclass=ABCMeta):

    def __init__(self, *, world):
        self._world = world

    @abstractmethod
    def next_tick(self, cell, random) -> Iterable[Action]:
        pass

    def __setattr__(self, name, value):
        if name == "_world" or self._world.is_mutable:
            super().__setattr__(name, value)
        else:
            raise AttributeError(
                "can't change cell content state when "
                "world is immutable"
            )
