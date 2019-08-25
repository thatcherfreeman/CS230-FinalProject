from piece.standard import PieceUtils
from piece.standard.StandardColor import StandardColor


def initRotations():
    twelveOverlay = PieceUtils.initOverlay()
    twelveOverlay.set(-2, 0, True)
    twelveOverlay.set(-1, 0, True)
    twelveOverlay.set(0, 0, True)
    twelveOverlay.set(1, 0, True)

    threeOverlay = PieceUtils.initOverlay()
    threeOverlay.set(0, -2, True)
    threeOverlay.set(0, -1, True)
    threeOverlay.set(0, 0, True)
    threeOverlay.set(0, 1, True)

    sixOverlay = PieceUtils.initOverlay()
    sixOverlay.set(-2, -1, True)
    sixOverlay.set(-1, -1, True)
    sixOverlay.set(0, -1, True)
    sixOverlay.set(1, -1, True)

    nineOverlay = PieceUtils.initOverlay()
    nineOverlay.set(-1, -2, True)
    nineOverlay.set(-1, -1, True)
    nineOverlay.set(-1, 0, True)
    nineOverlay.set(-1, 1, True)

    return [twelveOverlay, threeOverlay, sixOverlay, nineOverlay]


class CyanPiece:
    color = StandardColor.CYAN
    rotations = initRotations()
