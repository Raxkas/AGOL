from agol_app import AGOLApp

from entities.air import Air
from entities.grass import Grass
from entities.xotaker import Xotaker
from entities.predator import Predator
from entities.creeper import Creeper
from entities.monorem import Monorem


KINDS = [Air, Grass, Xotaker, Predator, Creeper, Monorem]
SPAWN_CHANCES = [128, 1, 1, 1, 1, 1]
FIELD_SIZE = (64, 64)
COLORS = {
    Air: (1, 1, 1, 0),
    Grass: (0, 0.5, 0),
    Xotaker: (1, 1, 0),
    Predator: (1, 0, 0),
    Creeper: (0, 0.25, 0.75),
    Monorem: (1, 1, 1)
}

if __name__ == "__main__":
    agol_app = AGOLApp(
        field_size=FIELD_SIZE,
        kinds=KINDS,
        kinds_colors=COLORS,
        spawn_chances=SPAWN_CHANCES
    )
    agol_app.run()
