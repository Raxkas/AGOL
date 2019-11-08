class Kernel:

    def __init__(self, next_tick_function):
        self._next_tick_function = next_tick_function
        self._simulation_state = None
        self._accumulated_input_data = []

    def next_tick(self, input_data):
        self._accumulated_input_data.append(input_data)
        self._simulation_state, output_data = self._next_tick_function(
            self._simulation_state, input_data
        )
        return output_data
