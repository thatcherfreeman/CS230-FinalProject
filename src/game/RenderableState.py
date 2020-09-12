from grid.Grid import Grid
from grid.InvertedHeightOverlay import InvertedHeightOverlay
from grid.ListGrid import ListGrid
from game.piece.standard.StandardColor import StandardColor
from game.GameState import GameState


class RenderableState(GameState):
    """The state of the game with enough information for a GUI to render a display"""
    # game state should have:
    # held piece, and whether you may swap the held piece (resets to True on piece placement)
    # piece on board
    # board state (which spaces are occupied)
    # board color state (which spaces should be colored and what color to do so)
    # piece queue
    # random piece generator (reproducible/seeded and adherent to tetris spec)
    # points
    # game speed

    def __init__(self):
        super().__init__()
        grid: Grid = ListGrid(10, 20, StandardColor.NONE)
        self.colorOverlay = InvertedHeightOverlay(grid)
