from bisect import bisect_left
from collections import namedtuple

from kivy.properties import BoundedNumericProperty, DictProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


# TODO: self._draw_history_frames(history_frames)
# TODO: slow Line.points increment?
# TODO: decomposition


class PopulationGraphWidget(Widget):
    _HistoryFrame = namedtuple("HistoryFrame", "ticks_since_start population_info")

    agol_kernel = ObjectProperty()
    area_ticks_to_display = BoundedNumericProperty(defaultvalue=1, min=0)
    colors = DictProperty()
    get_height_by_kind_quantity = ObjectProperty(defaultvalue=lambda quantity: quantity)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._history = []
        self.__ticks_history = []
        self.bind(size=lambda *args: self._reload_canvas())
        self.bind(pos=lambda *args: self._reload_canvas())

    def _init_graphs(self):
        self._graphs = {}
        for kind in self.agol_kernel.kinds:
            color = self._get_color_by_kind(kind)
            with self.canvas:
                Color(*color)
                self._graphs[kind] = Line(points=(), width=1)

    def _clear_graphs(self):
        for graph in self._graphs.values():
            graph.points = ()

    # TODO: observer?
    def update(self):
        if not hasattr(self, "_graphs"):
            self._init_graphs()
        previous_history_frame = self._history[-1] if self._history else None
        new_history_frame = self._make_history_frame()
        self._add_history_frame(new_history_frame)
        if previous_history_frame is not None:
            if not self._is_history_frame_visible(previous_history_frame):
                self._reload_canvas()

    def _reload_canvas(self):
        self._clear_graphs()
        for history_frame in self._get_visible_history_piece():
            self._draw_history_frame(history_frame)

    def _get_oldest_visible_tick(self):
        current_ticks_since_start = self._history[-1].ticks_since_start
        ticks_to_display = self.agol_kernel.field.area * self.area_ticks_to_display
        now_ticks_displayed = current_ticks_since_start % ticks_to_display
        return current_ticks_since_start - now_ticks_displayed

    def _is_history_frame_visible(self, history_frame):
        return history_frame.ticks_since_start >= self._get_oldest_visible_tick()

    def _get_visible_history_piece(self):
        oldest_visible_tick = self._get_oldest_visible_tick()
        start_index = bisect_left(self.__ticks_history, oldest_visible_tick)
        return self._history[start_index:]

    def _add_history_frame(self, history_frame):
        self._history.append(history_frame)
        self.__ticks_history.append(history_frame.ticks_since_start)
        self._draw_history_frame(history_frame)

    def _draw_history_frame(self, history_frame):
        ticks_since_start = history_frame.ticks_since_start
        x = self._get_x_by_ticks_since_start(ticks_since_start)
        for kind, quantity in history_frame.population_info.items():
            y = self._get_y_by_kind_quantity(quantity)
            self._graphs[kind].points += (x, y)

    def _make_history_frame(self):
        ticks_since_start = self.agol_kernel.ticks_since_start
        population_info = self._get_population_info()
        return self._HistoryFrame(ticks_since_start=ticks_since_start, population_info=population_info)

    def _get_population_info(self):
        keys = tuple(self.agol_kernel.kinds)
        values = map(self.agol_kernel.count_kind, keys)
        result = zip(keys, values)
        return dict(result)

    def _get_x_by_ticks_since_start(self, ticks_since_start):
        area_ticks = ticks_since_start / self.agol_kernel.field.area
        area_ticks_since_last_erasing = area_ticks % self.area_ticks_to_display
        k = area_ticks_since_last_erasing / self.area_ticks_to_display
        x = k * self.size[0]
        return self.pos[0] + x

    def _get_y_by_kind_quantity(self, quantity):
        height = self.get_height_by_kind_quantity(quantity)
        max_entity_count = self.agol_kernel.field.area
        max_height = self.get_height_by_kind_quantity(max_entity_count)
        k = height / max_height
        y = k * self.size[1]
        return self.pos[1] + y

    def _get_color_by_kind(self, kind):
        kind_name = kind.__name__
        return self.colors[kind_name]
