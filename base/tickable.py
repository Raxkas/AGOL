from abc import ABCMeta, abstractmethod

from base.action import Action
from base.cell_content import CellContent


class Tickable(CellContent, metaclass=ABCMeta):

    @abstractmethod
    def next_tick(self, random) -> Action:
        pass
