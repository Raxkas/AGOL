from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle


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

        # cell must have square shape
        cell_side_px = min(
            self.size[0] / self.field.size.x,
            self.size[1] / self.field.size.y
        )
        # if cell_side_px is fractional,
        # then the cells will have different sizes
        cell_side_px = int(cell_side_px)
        rect_size = (cell_side_px * self.field.size.x,
                     cell_side_px * self.field.size.y)
        rect_pos = (self.center[0] - rect_size[0]/2,
                    self.center[1] - rect_size[1]/2)
        # if rect_pos is fractional, then artifacts will appear
        rect_pos = (int(rect_pos[0]), int(rect_pos[1]))

        with self.canvas:
            Rectangle(pos=rect_pos, size=rect_size, texture=self._field_texture)

    def _get_color_by_entity(self, entity):
        color = self._colors[type(entity)]
        if len(color) == 3:
            opacity = int(self._compute_opacity(entity)*255)
            color += (opacity,)
        return color

    @staticmethod
    def _compute_opacity(entity):
        min_opacity = 0.25
        max_opacity = 1
        try:
            k = entity.energy / entity.energy_limit
        except AttributeError:
            k = 1
        return min_opacity + k*(max_opacity-min_opacity)
