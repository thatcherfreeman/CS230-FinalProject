from grid.Grid import Grid


class InvertedHeightOverlay(Grid):
    """A grid decorator that applies inversion to the y-indexing of a grid."""
    def __init__(self, grid: Grid):
        self.__grid = grid
        super().__init__(grid.width, grid.height)

    def __transformInputs(self, x: int, y: int):
        return x, self.__grid.height - y - 1

    def get(self, x: int, y: int):
        x, y = self.__transformInputs(x, y)
        return self.__grid.get(x, y)

    def set(self, x: int, y: int, value):
        x, y = self.__transformInputs(x, y)
        self.__grid.set(x, y, value)