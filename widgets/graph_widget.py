from operator import mul

from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


# TODO: wrong output for different game speed
class GraphWidget(Widget):
    agol_logic = ObjectProperty()
    colors = DictProperty()
    scaling_function = ObjectProperty(defaultvalue=lambda x: x)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=lambda *args: self._reload_canvas())
        self.bind(pos=lambda *args: self._reload_canvas())

    def _init_graphs(self):
        self._graphs = {}
        for kind in self.agol_logic.kinds:
            color = self._get_color_by_kind(kind)
            with self.canvas:
                Color(*color)
                self._graphs[kind] = Line(points=(), width=1)

    def update(self):
        if not hasattr(self, "_population_history"):
            self._population_history = [self._get_population_info()]
        if not hasattr(self, "_graphs"):
            self._init_graphs()
        self._population_history.append(self._get_population_info())
        last_x = self._get_x_by_history_index(-1)
        if int(last_x) == int(self.pos[0]):
            self.canvas.clear()
            self._init_graphs()
        for kind in self.agol_logic.kinds:
            self._add_point(index=-1, kind=kind)

    def _reload_canvas(self):
        self.canvas.clear()
        self._init_graphs()
        history_length = len(self._population_history)
        points_count = history_length % int(self.size[0])
        history_indices_range = range(
            history_length - points_count,
            history_length
        )
        for index in history_indices_range:
            for kind in self.agol_logic.kinds:
                self._add_point(index=index, kind=kind)

    def _add_point(self, *, index, kind):
        x = self._get_x_by_history_index(index)
        count = self._population_history[index][kind]
        y = self._get_y_by_kind_count(count)
        self._graphs[kind].points += (x, y)

    def _get_population_info(self):
        keys = tuple(self.agol_logic.kinds)
        values = map(self.agol_logic.count_kind, keys)
        result = zip(keys, values)
        return dict(result)

    def _get_x_by_history_index(self, index):
        if index < 0:
            index = len(self._population_history) + index
            assert index >= 0
        x = index
        x %= int(self.size[0])
        return self.pos[0] + x

    def _get_y_by_kind_count(self, count):
        max_entity_count = mul(*self.agol_logic.size)
        k = self.scaling_function(count) / self.scaling_function(max_entity_count)
        y = k * self.size[1]
        return self.pos[1] + y

    def _get_color_by_kind(self, kind):
        kind_name = kind.__name__
        return self.colors[kind_name]
