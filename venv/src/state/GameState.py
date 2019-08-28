from grid.ListGrid import ListGrid
from grid.Grid import Grid
from grid.InvertedHeightOverlay import InvertedHeightOverlay

PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20
PIECE_QUEUE_LEN = 3

class GameState:
    """The state of the game, minimal for memory-intensive policies that may instantiate many of these"""
    def __init__(self):
        # TODO: replace this with a bit-vector Grid implementation for lower memory use
        grid: Grid = ListGrid(10, 20, False)
        self.overlay = InvertedHeightOverlay(grid)
