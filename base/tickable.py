from abc import ABCMeta, abstractmethod
from typing import Iterable

from base.action import Action


class Tickable(metaclass=ABCMeta):

    @abstractmethod
    def next_tick(self, world, cell, random) -> Iterable[Action]:
        pass
