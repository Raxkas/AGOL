from app.agol_app import AGOLApp

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
    Grass: (0, 1/2, 0),
    Xotaker: (1, 1, 0),
    Predator: (1, 0, 0),
    Creeper: (0, 1/3, 1),
    Monorem: (1, 1, 1)
}


def main():
    agol_app = AGOLApp(
        field_size=FIELD_SIZE,
        kinds=KINDS,
        kinds_colors=COLORS,
        spawn_chances=SPAWN_CHANCES
    )
    agol_app.run()


if __name__ == "__main__":
    main()
