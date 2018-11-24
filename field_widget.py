from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

from entities.mob import Mob


class FieldWidget(Widget):
    COLORS = {
        "Air": (1, 1, 1, 0),
        "Grass": (0, 0.5, 0),
        "Xotaker": (1, 1, 0),
        "Predator": (1, 0, 0),
        "Creeper": (0, 0.25, 0.75),
        "Monorem": (1, 1, 1)
    }

    def __init__(self, agol_logic, **kwargs):
        self._agol_logic = agol_logic
        super().__init__(**kwargs)

    def update(self):
        self.canvas.clear()
        for y in range(self._agol_logic.height):
            for x in range(self._agol_logic.width):
                entity = self._agol_logic.get_entity_by_pos((x, y))
                self._draw_entity(entity)

    def _draw_entity(self, entity):
        cell_side_px = min(
            self.size[0] / self._agol_logic.width,
            self.size[1] / self._agol_logic.height
        )  # cell must have square shape
        cell_sides_px = (cell_side_px, cell_side_px)
        x, y = entity.pos
        color = self._get_color_by_entity(entity)
        x_pos_px = self.pos[0] + x * cell_sides_px[0]
        y_pos_px = self.pos[1] + y * cell_sides_px[1]
        pos_px = (x_pos_px, y_pos_px)
        with self.canvas:
            Color(*color)
            Rectangle(pos=pos_px, size=cell_sides_px)

    @classmethod
    def _get_color_by_entity(cls, entity):
        kind_name = type(entity).__name__
        color = cls.COLORS[kind_name]
        if len(color) == 3:
            opacity = cls._compute_opacity(entity)
            color += (opacity,)
        return color

    @staticmethod
    def _compute_opacity(entity):
        min_opacity = 0.25
        max_opacity = 1
        if not isinstance(entity, Mob):
            return max_opacity
        k = entity.energy / entity._energy_limit
        return min_opacity + k*(max_opacity-min_opacity)
