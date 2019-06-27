from collections import namedtuple

from kivy.properties import ObjectProperty
from kivy.uix.slider import Slider


class SpeedController(Slider):

    get_current_time = ObjectProperty()
    slider_value_to_speed = ObjectProperty(defaultvalue=lambda value: value)
    speed_to_slider_value = ObjectProperty(defaultvalue=lambda speed: speed)

    _SpeedChange = namedtuple("SpeedChange", "time speed")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._accumulated = 0
        self._latest_speed_change = None

    @property
    def accumulated(self):
        if self._latest_speed_change is None:
            return self._accumulated
        speed = self._latest_speed_change.speed
        time_since_latest_speed_change = self.get_current_time() - self._latest_speed_change.time
        return self._accumulated + speed * time_since_latest_speed_change

    def on_value(self, instance, value):
        assert instance is self
        self._accumulated = self.accumulated
        speed = self.slider_value_to_speed(value)
        self._latest_speed_change = self._SpeedChange(time=self.get_current_time(), speed=speed)
