from abc import ABCMeta, abstractmethod
from typing import Any, Tuple


_OutputData = Any


class Simulation(metaclass=ABCMeta):

    @abstractmethod
    def next_tick(self, input_data) -> _OutputData:
        pass

    @classmethod
    @abstractmethod
    def initial_next_tick(cls, input_data) -> Tuple["Simulation", _OutputData]:
        pass
