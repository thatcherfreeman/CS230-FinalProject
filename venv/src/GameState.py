from grid.ListGrid import ListGrid
from grid.Grid import Grid
from grid.InvertedHeightOverlay import InvertedHeightOverlay


# The state of the game, minimal for rigorous Policy performance
class GameState:
    def __init__(self):
        # TODO: replace this with a bit-vector Grid implementation for lower memory use
        grid: Grid = ListGrid(10, 20, False)
        self.overlay = InvertedHeightOverlay(grid)
