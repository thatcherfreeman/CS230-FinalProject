from piece.standard import PieceUtils
from piece.standard.StandardColor import StandardColor


def initRotations():
    # The yellow piece is a square, so rotation doesn't do anything
    twelveOverlay = PieceUtils.initOverlay()
    twelveOverlay.set(0, 0, True)
    twelveOverlay.set(0, -1, True)
    twelveOverlay.set(-1, 0, True)
    twelveOverlay.set(-1, -1, True)

    return [twelveOverlay] * 4


class YellowPiece:
    color = StandardColor.YELLOW
    rotations = initRotations()
