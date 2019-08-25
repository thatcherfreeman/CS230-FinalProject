from grid.OffsetOverlay import OffsetOverlay
from piece.standard.StandardColor import StandardColor


class TetrisPiece:
    def __init__(self, overlay: OffsetOverlay, color: StandardColor):
        self.overlay = overlay
        self.color = color

    def rotateCW(self):
        raise NotImplementedError

    def rotateCCW(self):
        raise NotImplementedError
