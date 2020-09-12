from game.piece.WallKicks import WallKicks
from grid.OffsetOverlay import OffsetOverlay


class RotationData:
    def __init__(self, overlay: OffsetOverlay, wallKicks: WallKicks):
        self.overlay = overlay
        self.wallKicks = wallKicks
