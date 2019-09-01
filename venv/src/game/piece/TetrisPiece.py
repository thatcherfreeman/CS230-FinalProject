from typing import Tuple, List

from game.piece.WallKicks import WallKicks
from grid.OffsetOverlay import OffsetOverlay
from game.piece.standard.StandardColor import StandardColor


class TetrisPiece:
    def __init__(self, overlay: OffsetOverlay, wallKicks: WallKicks, color: StandardColor):
        self.overlay = overlay
        self.color = color
        self.wallKicks = wallKicks

    def rotateCW(self):
        raise NotImplementedError

    def rotateCCW(self):
        raise NotImplementedError
