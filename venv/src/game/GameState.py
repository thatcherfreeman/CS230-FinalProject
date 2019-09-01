from grid.ListGrid import ListGrid
from grid.Grid import Grid
from grid.InvertedHeightOverlay import InvertedHeightOverlay
from game.PieceGenerator import PieceGenerator

PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20
BUFFER_HEIGHT = 2
PIECE_QUEUE_LEN = 3


class GameState:
    """The state of the game, minimal for memory-intensive policies that may instantiate many of these"""
    def __init__(self):
        # TODO: replace this with a bit-vector Grid implementation for lower memory use?
        grid: Grid = ListGrid(PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT + BUFFER_HEIGHT, False)
        self.overlay = InvertedHeightOverlay(grid) # TODO: Remove this overlay later to save memory?
        # TODO: It's debatable whether or not which pieces have shown up in the sequence so far should be an input to
        #  an agent. You could get better performance that way (sometimes the agent would know that the next piece
        #  that would be queued MUST be a T-piece, for example, and that way it could simulate/explore fewer game
        #  states), but unless I'm just really bad at Tetris, I don't think this is something a human would do. For
        #  now, let's exclude piece generation info from the game state. Revisit this later.
        self.currentPiece = None
        self.currentPieceLocation = None
        self.pieceQueue = None # TODO: Use a queue library for this?
        self.heldPiece = None
        self.points = 0
