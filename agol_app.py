from kivy.app import App
from kivy.clock import Clock

from game_logic.agol_kernel import AGOLKernel


class AGOLApp(App):
    agol_kernel = None
    app_ticks_per_second = None

    def __init__(self, *, field_size, kinds, kinds_colors, spawn_chances, app_ticks_per_second):
        super().__init__()
        self.agol_kernel = AGOLKernel(field_size, kinds, spawn_chances)
        self.kinds_colors = kinds_colors.copy()
        self.app_ticks_per_second = app_ticks_per_second
        Clock.schedule_interval(lambda dt: self.next_tick(), 1/self.app_ticks_per_second)

    def next_tick(self):
        ids = self.root.ids
        ids.field_widget.update()
        ids.population_graph_widget.update()
        kernel_ticks_per_app_tick = int(self.game_speed * self.agol_kernel.count_entities())
        for _ in range(kernel_ticks_per_app_tick):
            self.agol_kernel.next_tick()

    def on_pause(self):
        return True

    @property
    def game_speed(self):
        ids = self.root.ids
        return ids.speed_slider.value
