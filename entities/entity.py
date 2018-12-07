from abc import ABCMeta, abstractmethod


class Entity(metaclass=ABCMeta):
    __slots__ = ("_game_logic", "alive", "pos")

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
        return self._game_logic.get_region_points(self.pos, radius)

    def is_near(self, *args):
        return len(self.find_near(*args)) > 0

    def find_near(self, *kinds):
        mobs_near = map(self._game_logic.get_entity_by_pos, self.directions)
        found = filter(lambda mob: isinstance(mob, kinds), mobs_near)
        return tuple(found)
