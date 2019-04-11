from bisect import bisect_left
from collections import namedtuple
from operator import mul

from kivy.properties import BoundedNumericProperty, DictProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


class GraphWidget(Widget):
    _HistoryFrame = namedtuple("HistoryFrame", "tick_number population_info")

    agol_logic = ObjectProperty()
    area_ticks_to_display = BoundedNumericProperty(defaultvalue=512, min=0)
    colors = DictProperty()
    scaling_function = ObjectProperty(defaultvalue=lambda x: x)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._history = []
        self.__ticks_history = []
        self.bind(size=lambda *args: self._reload_canvas())
        self.bind(pos=lambda *args: self._reload_canvas())

    def _init_graphs(self):
        self._graphs = {}
        for kind in self.agol_logic.kinds:
            color = self._get_color_by_kind(kind)
            with self.canvas:
                Color(*color)
                self._graphs[kind] = Line(points=(), width=1)

    def _clear_graphs(self):
        for graph in self._graphs.values():
            graph.points = ()

    def update(self):
        if not hasattr(self, "_graphs"):
            self._init_graphs()
        previous_history_frame = self._history[-1] if self._history else None
        new_history_frame = self._make_history_frame()
        self._add_history_frame(new_history_frame)
        if not self._is_history_frame_visible(previous_history_frame):
            self._reload_canvas()

    def _reload_canvas(self):
        self._clear_graphs()
        for history_frame in self._get_visible_history_piece():
            self._draw_history_frame(history_frame)

    def _get_range_of_visible_history_indexes(self):
        current_tick_number = self._history[-1].tick_number
        ticks_to_display = self.agol_logic.area * self.area_ticks_to_display
        first_tick_to_display = current_tick_number - current_tick_number % ticks_to_display
        start_index = bisect_left(self.__ticks_history, first_tick_to_display)
        stop_index = len(self._history)
        return range(start_index, stop_index)

    def _is_history_frame_visible(self, history_frame):
        return history_frame in self._get_range_of_visible_history_indexes()

    def _get_visible_history_piece(self):
        visible_range = self._get_range_of_visible_history_indexes()
        slice_for_visible_history = slice(visible_range.start, visible_range.stop)
        return self._history[slice_for_visible_history]

    def _add_history_frame(self, history_frame):
        self._history.append(history_frame)
        self.__ticks_history.append(history_frame.tick_number)
        self._draw_history_frame(history_frame)

    def _draw_history_frame(self, history_frame):
        tick_number = history_frame.tick_number
        x = self._get_x_by_tick_number(tick_number)
        for kind, count in history_frame.population_info.items():
            y = self._get_y_by_kind_count(count)
            self._graphs[kind].points += (x, y)

    def _make_history_frame(self):
        tick_number = self.agol_logic.tick_number
        population_info = self._get_population_info()
        return self._HistoryFrame(tick_number=tick_number, population_info=population_info)

    def _get_population_info(self):
        keys = tuple(self.agol_logic.kinds)
        values = map(self.agol_logic.count_kind, keys)
        result = zip(keys, values)
        return dict(result)

    def _get_x_by_tick_number(self, tick_number):
        area_ticks = tick_number / self.agol_logic.area
        area_ticks_since_last_erasing = area_ticks % self.area_ticks_to_display
        k = area_ticks_since_last_erasing / self.area_ticks_to_display
        x = k * self.size[0]
        return self.pos[0] + x

    def _get_y_by_kind_count(self, count):
        max_entity_count = mul(*self.agol_logic.size)
        k = self.scaling_function(count) / self.scaling_function(max_entity_count)
        y = k * self.size[1]
        return self.pos[1] + y

    def _get_color_by_kind(self, kind):
        kind_name = kind.__name__
        return self.colors[kind_name]
