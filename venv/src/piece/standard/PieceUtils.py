from grid.ListGrid import ListGrid
from grid.OffsetOverlay import OffsetOverlay


def initOverlay():
    grid = ListGrid(4, 4, False)
    return OffsetOverlay(grid, -2, -2)