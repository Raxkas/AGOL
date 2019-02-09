from math import log2
from operator import mul

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider

from widgets.field_widget import FieldWidget
from widgets.graph_widget import GraphWidget

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
        self.field_widget.update()
        self.graph_widget.update()
        area = mul(*self.LOGIC.size)
        logic_ticks_per_app_tick = int(self.game_speed * area)
        for _ in range(logic_ticks_per_app_tick):
            self.LOGIC.next_tick()

    def on_pause(self):
        return True

    def build(self):
        self.field_widget = FieldWidget(self.LOGIC, COLORS)
        self.graph_widget = GraphWidget(self.LOGIC, COLORS, scaling_function=lambda c: log2(1 + c))
        self.speed_slider = Slider(min=0, max=1, value=0.5, size_hint=[1, 0.1])
        root_widget = BoxLayout(orientation="vertical")
        main_widget = BoxLayout(spacing=16, size_hint=[1, 0.9])
        main_widget.add_widget(self.field_widget)
        main_widget.add_widget(self.graph_widget)
        root_widget.add_widget(self.speed_slider)
        root_widget.add_widget(main_widget)
        return root_widget

    @property
    def game_speed(self):
        return self.speed_slider.value


if __name__ == "__main__":
    AGOLApp().run()
