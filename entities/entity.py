from abc import ABCMeta, abstractmethod
from itertools import product


class Entity(metaclass=ABCMeta):
    alive = None
    _game_logic = None
    pos = None

    @abstractmethod
    def next_tick(self):
        pass

    @property
    def kind(self):
        return type(self)

    @property
    def directions(self):
        area = list(self._get_area(1))
        area.remove(self.pos)
        return tuple(area)

    def _get_area(self, radius):
        x, y = self.pos
        offsets = range(-radius, radius+1)
        x_range = map(x.__add__, offsets)
        y_range = map(y.__add__, offsets)
        area = product(x_range, y_range)
        area = filter(self._game_logic.is_pos_correct, area)
        return tuple(area)

    def is_near(self, *args):
        return len(self.find_near(*args)) > 0

    def find_near(self, *kinds):
        mobs_near = map(self._game_logic.get_entity_by_pos, self.directions)
        found = filter(lambda mob: isinstance(mob, kinds), mobs_near)
        return tuple(found)
