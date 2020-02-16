from abc import ABCMeta, abstractmethod


# TODO: explain why actions system is necessary
class Action(metaclass=ABCMeta):

    def __init__(self, *, world):
        self._world = world

    @abstractmethod
    def apply(self):
        pass
