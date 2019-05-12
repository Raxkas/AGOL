class Matrix:

    def __init__(self, *, size):
        self.size = tuple(size)
        del size
        self.__content = [
            [
                None
                for x in range(self.size[0])
            ]
            for y in range(self.size[1])
        ]

    def __getitem__(self, pos):
        x, y = pos
        return self.__content[y][x]

    def __setitem__(self, pos, value):
        x, y = pos
        self.__content[y][x] = value
