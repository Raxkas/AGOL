from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle

from entities.mob import Mob


class FieldWidget(Widget):
    field = ObjectProperty()
    colors = DictProperty()
    _field_texture = None

    def on_colors(self, instance, new_colors):
        transform_color_to_24bit_color = lambda color: tuple(int(k * 255) for k in color)
        self._colors = {key: transform_color_to_24bit_color(color)
                        for key, color in new_colors.items()}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=lambda *args: self._update_canvas())

    def update(self):
        size = self.field.size
        texture = Texture.create(size=size)
        texture.mag_filter = 'nearest'
        buf = [None] * (4 * size.x*size.y)
        for y in range(size.y):
            for x in range(size.x):
                entity = self.field[x, y]
                color = self._get_color_by_entity(entity)
                i = x + y*size.x
                start, end = 4*i, 4*(i+1)
                buf[start:end] = color
        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt='rgba')
        self._field_texture = texture
        self._update_canvas()

    def _update_canvas(self):
        self.canvas.clear()
        if self._field_texture is None:
            return;
        cell_side_px = min(
            self.size[0] / self.field.size.x,
            self.size[1] / self.field.size.y
        )  # cell must have square shape
        cell_side_px = int(cell_side_px)
        rect_size = (cell_side_px * self.field.size.x,
                     cell_side_px * self.field.size.y)
        with self.canvas:
            Rectangle(pos=self.pos, size=rect_size, texture=self._field_texture)

    def _get_color_by_entity(self, entity):
        kind_name = type(entity).__name__
        color = self._colors[kind_name]
        if len(color) == 3:
            opacity = int(self._compute_opacity(entity)*255)
            color += (opacity,)
        return color

    @staticmethod
    def _compute_opacity(entity):
        min_opacity = 0.25
        max_opacity = 1
        if not isinstance(entity, Mob):
            return max_opacity
        k = entity.energy / entity.energy_limit
        return min_opacity + k*(max_opacity-min_opacity)