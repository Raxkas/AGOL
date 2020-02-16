class CellContent:
    
    def __init__(self, *, world):
        self._world = world
        self.cell = None

    def __setattr__(self, name, value):
        if name == "_world" or self._world.is_mutable:
            super().__setattr__(name, value)
        else:
            raise AttributeError(
                "can't change cell content state when "
                "world is immutable"
            )
