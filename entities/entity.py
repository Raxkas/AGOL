from abc import ABCMeta, abstractmethod


class Entity(metaclass=ABCMeta):
    __slots__ = ("_game_logic", "is_alive", "pos")

    def __init__(self, *, game_logic, pos):
        self._game_logic = game_logic
        self.pos = pos

    @abstractmethod
    def next_tick(self):
        pass

    @property
    def __adjacent_entities(self):
        entities = self._game_logic.get_entities_in_region(self.pos, 1)
        entities.remove(self)
        return entities

    def _is_near(self, *kinds_needed):
        kinds_near = frozenset(map(type, self.__adjacent_entities))
        return any(map(lambda kind: issubclass(kind, kinds_needed), kinds_near))

    def _find_near(self, *kinds):
        found = filter(lambda entity: isinstance(entity, kinds), self.__adjacent_entities)
        return tuple(found)
