from operator import mul

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


class GraphWidget(Widget):
    def __init__(self, agol_logic, colors, *, scaling_function=lambda x: x, **kwargs):
        self._agol_logic = agol_logic
        self._colors = colors
        self._population_history = [self._get_population_info()]
        self._scaling_function = scaling_function
        super().__init__(**kwargs)
        self.bind(size=lambda *args: self._reload_canvas())
        self.bind(pos=lambda *args: self._reload_canvas())

    def update(self):
        self._population_history.append(self._get_population_info())
        last_x = (len(self._population_history)-1) % self.size[0]
        last_x = int(last_x)
        if last_x == 0:
            self.canvas.clear()
        for kind in self._agol_logic.kinds:
            self._draw_one_line(indices=[-2, -1], kind=kind)

    def _reload_canvas(self):
        self.canvas.clear()
        history_length = len(self._population_history)
        lines_count = int(history_length % self.size[0])
        lines_ends_indices_range = range(
            history_length - lines_count,
            history_length
        )
        for index2 in lines_ends_indices_range:
            index1 = index2 - 1 if index2 != 0 else index2
            for kind in self._agol_logic.kinds:
                self._draw_one_line(indices=[index1, index2], kind=kind)

    def _draw_one_line(self, *, indices, kind):
        x1, x2 = map(self._get_x_by_history_index, indices)
        if x1 > x2:
            x1 = x2
        counts = map(lambda index: self._population_history[index][kind], indices)
        y1, y2 = map(self._get_y_by_kind_count, counts)
        color = self._get_color_by_kind(kind)
        with self.canvas:
            Color(*color)
            Line(points=[(x1, y1), (x2, y2)], width=1)

    def _get_population_info(self):
        keys = tuple(self._agol_logic.kinds)
        values = map(self._agol_logic.count_kind, keys)
        result = zip(keys, values)
        return dict(result)

    def _get_x_by_history_index(self, index):
        if index < 0:
            index = len(self._population_history) + index
            assert index >= 0
        x = index % self.size[0]
        return self.pos[0] + x

    def _get_y_by_kind_count(self, count):
        max_entity_count = mul(*self._agol_logic.size)
        k = self._scaling_function(count) / self._scaling_function(max_entity_count)
        y = k * self.size[1]
        return self.pos[1] + y

    def _get_color_by_kind(self, kind):
        kind_name = kind.__name__
        return self._colors[kind_name]
