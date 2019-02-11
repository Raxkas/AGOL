from operator import mul

from kivy.app import App
from kivy.clock import Clock

from game_logic.agol_logic import AGOLLogic
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


class AGOLApp(App):
    LOGIC = None
    field_widget = None
    graph_widget = None
    speed_slider = None
    app_ticks_per_second = 10

    def __init__(self):
        super().__init__()
        self.LOGIC = AGOLLogic(WIDTH, HEIGHT, KINDS, SPAWN_CHANCES)
        Clock.schedule_interval(lambda dt: self.next_tick(), 1/self.app_ticks_per_second)

    def next_tick(self):
        ids = self.root.ids
        ids["field_widget"].update()
        ids["graph_widget"].update()
        area = mul(*self.LOGIC.size)
        logic_ticks_per_app_tick = int(self.game_speed * area)
        for _ in range(logic_ticks_per_app_tick):
            self.LOGIC.next_tick()

    def on_pause(self):
        return True

    @property
    def game_speed(self):
        ids = self.root.ids
        return ids["speed_slider"].value


if __name__ == "__main__":
    AGOLApp().run()
