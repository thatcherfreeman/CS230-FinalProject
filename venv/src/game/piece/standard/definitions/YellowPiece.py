from game.piece.WallKicks import WallKicks
from game.piece.standard import PieceUtils
from game.piece.standard.RotationData import RotationData
from game.piece.standard.StandardColor import StandardColor


def initRotations():
    # The yellow piece is a square, so rotation doesn't do anything
    twelveOverlay = PieceUtils.initOverlay()
    twelveOverlay.set(0, 0, True)
    twelveOverlay.set(0, -1, True)
    twelveOverlay.set(-1, 0, True)
    twelveOverlay.set(-1, -1, True)
    twelveRotData = RotationData(twelveOverlay, WallKicks([(0, 0)], [(0, 0)]))

    return [twelveRotData] * 4


class YellowPiece:
    color = StandardColor.YELLOW
    rotations = initRotations()
