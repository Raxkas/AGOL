from kivy.app import App
from kivy.clock import Clock

from app_usage_time_counter import AppUsageTimeCounter
from game_logic.agol_kernel import AGOLKernel


class AGOLApp(App):

    def __init__(self, *, field_size, kinds, kinds_colors, spawn_chances):
        super().__init__()
        self._app_usage_time_counter = AppUsageTimeCounter()
        self.agol_kernel = AGOLKernel(field_size, kinds, spawn_chances)
        self.kinds_colors = kinds_colors.copy()
        Clock.schedule_interval(self.next_tick, 0)

    def next_tick(self, dt):
        ids = self.root.ids
        ids.field_widget.update()
        ids.population_graph_widget.update()
        for _ in range(self._get_undone_kernel_ticks_quantity()):
            self.agol_kernel.next_tick()

    def _get_undone_kernel_ticks_quantity(self):
        accumulated_area_ticks = self.root.ids.speed_controller.accumulated
        accumulated_kernel_ticks = int(accumulated_area_ticks * self.agol_kernel.count_entities())
        return accumulated_kernel_ticks - self.agol_kernel.ticks_since_start

    def get_usage_time(self):
        return self._app_usage_time_counter.get_usage_time()

    def on_pause(self):
        self._app_usage_time_counter.pause()
        return True

    def on_resume(self):
        self._app_usage_time_counter.resume()
