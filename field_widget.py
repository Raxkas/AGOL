from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle

from entities.mob import Mob


class FieldWidget(Widget):
    # TODO: move to constructor
    COLORS = {
        "Air": (1, 1, 1, 0),
        "Grass": (0, 0.5, 0),
        "Xotaker": (1, 1, 0),
        "Predator": (1, 0, 0),
        "Creeper": (0, 0.25, 0.75),
        "Monorem": (1, 1, 1)
    }
    _agol_texture = None

    def __init__(self, agol_logic, **kwargs):
        self._agol_logic = agol_logic
        super().__init__(**kwargs)
        self.bind(size=lambda *args: self._update_canvas())

    def update(self):
        size = self._agol_logic.size
        texture = Texture.create(size=size)
        texture.mag_filter = 'nearest'
        buf = [None] * (4 * size.x*size.y)
        for y in range(size.y):
            for x in range(size.x):
                entity = self._agol_logic.get_entity_by_pos((x, y))
                color = self._get_color_by_entity(entity)
                color = map(lambda k: int(k*255), color)
                i = x + y*size.x
                start, end = 4*i, 4*(i+1)
                buf[start:end] = color
        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt='rgba')
        self._agol_texture = texture
        self._update_canvas()

    def _update_canvas(self):
        self.canvas.clear()
        if self._agol_texture is None:
            return;
        cell_side_px = min(
            self.size[0] / self._agol_logic.size.x,
            self.size[1] / self._agol_logic.size.y
        )  # cell must have square shape
        rect_size = (cell_side_px * self._agol_logic.size.x,
                     cell_side_px * self._agol_logic.size.y)
        with self.canvas:
            Rectangle(pos=self.pos, size=rect_size, texture=self._agol_texture)

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
