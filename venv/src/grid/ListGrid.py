from src.grid.Grid import Grid


class ListGrid(Grid):
    """A really simple implementation of Grid that uses a 2D list"""
    def __init__(self, width: int, height: int, initVal):
        self.__grid = [[initVal for y in range(0, height)] for x in range(0, width)]
        super().__init__(width, height)

    def get(self, x: int, y: int):
        return self.__grid[x][y]

    def set(self, x: int, y: int, value):
        self.__grid[x][y] = value
