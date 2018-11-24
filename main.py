from kivy.app import App
from kivy.clock import Clock

from field_widget import FieldWidget

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


class AGOLApp(App):
    LOGIC = None
    field_widget = None
    FPS = 5

    def next_tick(self):
        self.field_widget.update()
        self.LOGIC.next_tick()

    def build(self):
        self.LOGIC = AGOLLogic(WIDTH, HEIGHT, KINDS, SPAWN_CHANCES)
        self.field_widget = FieldWidget(self.LOGIC)
        Clock.schedule_interval(lambda dt: self.next_tick(), 1/self.FPS)
        root_widget = self.field_widget
        return root_widget


if __name__ == "__main__":
    AGOLApp().run()
