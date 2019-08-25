from piece.standard import PieceUtils
from piece.standard.StandardColor import StandardColor


def initRotations():
    # 'T' facing up
    twelveOverlay = PieceUtils.initOverlay()
    twelveOverlay.set(-1, 0, True)
    twelveOverlay.set(0, 0, True)
    twelveOverlay.set(1, 0, True)
    twelveOverlay.set(0, 1, True)

    # 'T' facing right
    threeOverlay = PieceUtils.initOverlay()
    threeOverlay.set(0, -1, True)
    threeOverlay.set(0, 0, True)
    threeOverlay.set(0, 1, True)
    threeOverlay.set(1, 0, True)

    # 'T' facing down
    sixOverlay = PieceUtils.initOverlay()
    sixOverlay.set(-1, 0, True)
    sixOverlay.set(0, 0, True)
    sixOverlay.set(1, 0, True)
    sixOverlay.set(0, -1, True)

    # 'T' facing left
    nineOverlay = PieceUtils.initOverlay()
    nineOverlay.set(0, -1, True)
    nineOverlay.set(0, 0, True)
    nineOverlay.set(0, 1, True)
    nineOverlay.set(-1, 0, True)

    return [twelveOverlay, threeOverlay, sixOverlay, nineOverlay]


class PurplePiece:
    color = StandardColor.PURPLE
    rotations = initRotations()
