from math import log2

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from field_widget import FieldWidget
from graph_widget import GraphWidget

from game_logic import AGOLLogic
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
    FPS = 5

    def __init__(self):
        super().__init__()
        self.LOGIC = AGOLLogic(WIDTH, HEIGHT, KINDS, SPAWN_CHANCES)
        Clock.schedule_interval(lambda dt: self.next_tick(), 1/self.FPS)

    def next_tick(self):
        self.field_widget.update()
        self.graph_widget.update()
        self.LOGIC.next_tick()

    def on_pause(self):
        return True

    def build(self):
        self.field_widget = FieldWidget(self.LOGIC, COLORS)
        self.graph_widget = GraphWidget(self.LOGIC, COLORS, scaling_function=lambda c: log2(1 + c))
        root_widget = BoxLayout(spacing=16)
        root_widget.add_widget(self.field_widget)
        root_widget.add_widget(self.graph_widget)
        return root_widget


if __name__ == "__main__":
    AGOLApp().run()
