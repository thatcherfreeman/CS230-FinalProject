from src.grid.Grid import Grid

# A grid decorator that applies an offset to the indexing of a grid. Useful for more intuitive programming,
# allowing indexing like a traditional 2D cartesian plane
class OffsetOverlay(Grid):
    def __init__(self, grid: Grid, startX: int, startY: int):
        self.__grid = grid
        self.__startX = startX
        self.__startY = startY
        super().__init__(grid.width, grid.height)

    def __transformInputs(self, x: int, y: int):
        return (x - self.__startX, y - self.__startY)

    def get(self, x: int, y: int):
        x, y = self.__transformInputs(x, y)
        self.__checkBounds(x, y)
        return self.__grid.get(x, y)

    def set(self, x: int, y: int, value):
        x, y = self.__transformInputs(x, y)
        self.__checkBounds(x, y)
        self.__grid.set(x, y, value)

    def __checkBounds(self, x: int, y: int):
        if (x < 0) or (y < 0) or (x >= self.width) or (y >= self.height):
            raise "Out of bounds"
