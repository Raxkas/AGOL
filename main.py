from agol_app import AGOLApp

from entities.air import Air
from entities.grass import Grass
from entities.xotaker import Xotaker
from entities.predator import Predator
from entities.creeper import Creeper
from entities.monorem import Monorem


KINDS = [Air, Grass, Xotaker, Predator, Creeper, Monorem]
SPAWN_CHANCES = [128, 1, 1, 1, 1, 1]
WIDTH = 64
HEIGHT = 64
COLORS = {
    "Air": (1, 1, 1, 0),
    "Grass": (0, 0.5, 0),
    "Xotaker": (1, 1, 0),
    "Predator": (1, 0, 0),
    "Creeper": (0, 0.25, 0.75),
    "Monorem": (1, 1, 1)
}
TICKS_PER_SECOND = 10


if __name__ == "__main__":
    agol_app = AGOLApp(WIDTH, HEIGHT, KINDS, SPAWN_CHANCES, TICKS_PER_SECOND)
    agol_app.run()
