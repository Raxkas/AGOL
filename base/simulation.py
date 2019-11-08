from abc import ABCMeta, abstractmethod


class Simulation(metaclass=ABCMeta):

    @abstractmethod
    def next_tick(self, input_data):
        pass

    @classmethod
    @abstractmethod
    def initial_next_tick(cls, input_data):
        pass
