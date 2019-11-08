from abc import ABCMeta, abstractmethod


# TODO: explain why actions system is necessary
class Action(metaclass=ABCMeta):

    @abstractmethod
    def apply(self, world):
        pass
