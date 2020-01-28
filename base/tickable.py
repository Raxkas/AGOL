from abc import ABCMeta, abstractmethod
from typing import Iterable

from base.action import Action


class Tickable(metaclass=ABCMeta):

    def __init__(self, *, world):
        self._world = world

    @abstractmethod
    def next_tick(self, cell, random) -> Iterable[Action]:
        pass
