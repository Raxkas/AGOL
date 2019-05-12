from abc import ABCMeta, abstractmethod


class Entity(metaclass=ABCMeta):
    __slots__ = ("field", "pos")

    def __init__(self, *, agol_kernel, field):
        agol_kernel.add_entity(self)
        self.field = field

    @abstractmethod
    def next_tick(self):
        pass
