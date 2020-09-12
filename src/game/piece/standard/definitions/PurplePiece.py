from game.piece.standard import PieceUtils
from game.piece.standard.RotationData import RotationData
from game.piece.standard.StandardColor import StandardColor
from game.piece.standard.definitions.CommonKicks import SIX_KICKS, THREE_KICKS, NINE_KICKS, TWELVE_KICKS


def initRotations():
    # 'T' facing up
    twelveOverlay = PieceUtils.initOverlay()
    twelveOverlay.set(-1, 0, True)
    twelveOverlay.set(0, 0, True)
    twelveOverlay.set(1, 0, True)
    twelveOverlay.set(0, 1, True)
    twelveRotData = RotationData(twelveOverlay, TWELVE_KICKS)

    # 'T' facing right
    threeOverlay = PieceUtils.initOverlay()
    threeOverlay.set(0, -1, True)
    threeOverlay.set(0, 0, True)
    threeOverlay.set(0, 1, True)
    threeOverlay.set(1, 0, True)
    threeRotData = RotationData(threeOverlay, THREE_KICKS)

    # 'T' facing down
    sixOverlay = PieceUtils.initOverlay()
    sixOverlay.set(-1, 0, True)
    sixOverlay.set(0, 0, True)
    sixOverlay.set(1, 0, True)
    sixOverlay.set(0, -1, True)
    sixRotData = RotationData(sixOverlay, SIX_KICKS)

    # 'T' facing left
    nineOverlay = PieceUtils.initOverlay()
    nineOverlay.set(0, -1, True)
    nineOverlay.set(0, 0, True)
    nineOverlay.set(0, 1, True)
    nineOverlay.set(-1, 0, True)
    nineRotData = RotationData(nineOverlay, NINE_KICKS)

    return [twelveRotData, threeRotData, sixRotData, nineRotData]


class PurplePiece:
    color = StandardColor.PURPLE
    rotations = initRotations()
