from kivy.app import App
from kivy.clock import Clock

from game_logic.agol_logic import AGOLLogic


class AGOLApp(App):
    logic = None
    app_ticks_per_second = None

    def __init__(self, field_size, kinds, spawn_chances, app_ticks_per_second):
        super().__init__()
        self.logic = AGOLLogic(field_size, kinds, spawn_chances)
        self.app_ticks_per_second = app_ticks_per_second
        Clock.schedule_interval(lambda dt: self.next_tick(), 1/self.app_ticks_per_second)

    def next_tick(self):
        ids = self.root.ids
        ids.field_widget.update()
        ids.population_graph_widget.update()
        logic_ticks_per_app_tick = int(self.game_speed * self.logic.count_entities())
        for _ in range(logic_ticks_per_app_tick):
            self.logic.next_tick()

    def on_pause(self):
        return True

    @property
    def game_speed(self):
        ids = self.root.ids
        return ids.speed_slider.value
