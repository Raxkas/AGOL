import time


class AppUsageTimeCounter:

    def __init__(self):
        self._get_current_time = time.time
        self._time_offset = self._get_current_time()
        self._pause_start_time = None

    def get_usage_time(self):
        return self._get_current_time() - self._get_time_offset()

    def pause(self):
        if self._is_paused():
            raise ValueError("already paused")
        self._pause_start_time = self._get_current_time()

    def resume(self):
        if not self._is_paused():
            raise ValueError("already resumed")
        self._time_offset += self._get_pause_duration_time()
        self._pause_start_time = None

    def _get_time_offset(self):
        pause_duration_time = self._get_pause_duration_time() if self._is_paused() else 0
        return self._time_offset + pause_duration_time

    def _get_pause_duration_time(self):
        return self._get_current_time() - self._pause_start_time

    def _is_paused(self):
        return self._pause_start_time is not None
