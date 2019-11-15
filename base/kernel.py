# TODO: Remove Kernel class?
class Kernel:

    def __init__(self, simulation_class):
        self._simulation_class = simulation_class
        self._simulation = None
        # TODO: input_data/output_data observer?

    def next_tick(self, input_data):
        if self._simulation is None:
            self._simulation, output_data = \
                self._simulation_class.initial_next_tick(input_data)
        else:
            output_data = self._simulation.next_tick(input_data)
        return output_data
