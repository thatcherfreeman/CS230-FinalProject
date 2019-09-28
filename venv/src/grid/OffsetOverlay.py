from grid.Grid import Grid


class OffsetOverlay(Grid):
    """A grid decorator that applies an offset to the indexing of a grid."""
    def __init__(self, grid: Grid, startX: int, startY: int):
        self.__grid = grid
        self.__startX = startX
        self.__startY = startY
        super().__init__(grid.width, grid.height)

    def __transformInputs(self, x: int, y: int):
        return x - self.__startX, y - self.__startY

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
            raise Exception("Out of bounds")

    # for debug purposes only
    def printOverlay(self):
        for y in range(self.height - 1, -1, -1):
            row = ["."] * 5
            for x in range(0, self.width):
                if self.__grid.get(x, y):
                    row[x] = "X"
            line = row[0]
            for x in range(1, self.width):
                line = line + " " + row[x]
            print(line)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if self.__startX != other.__startX or self.__startY != other.__startY:
            return False
        return self.__grid == other.__grid
