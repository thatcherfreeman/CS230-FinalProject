from game.piece.standard import PieceUtils
from game.piece.standard.RotationData import RotationData
from game.piece.standard.StandardColor import StandardColor
from game.piece.standard.definitions.CommonKicks import TWELVE_KICKS, THREE_KICKS, SIX_KICKS, NINE_KICKS


def initRotations():
    twelveOverlay = PieceUtils.initOverlay()
    twelveOverlay.set(-1, 1, True)
    twelveOverlay.set(-1, 0, True)
    twelveOverlay.set(0, 0, True)
    twelveOverlay.set(1, 0, True)
    twelveRotData = RotationData(twelveOverlay, TWELVE_KICKS)

    threeOverlay = PieceUtils.initOverlay()
    threeOverlay.set(1, 1, True)
    threeOverlay.set(0, 1, True)
    threeOverlay.set(0, 0, True)
    threeOverlay.set(0, -1, True)
    threeRotData = RotationData(threeOverlay, THREE_KICKS)

    sixOverlay = PieceUtils.initOverlay()
    sixOverlay.set(-1, 0, True)
    sixOverlay.set(0, 0, True)
    sixOverlay.set(1, 0, True)
    sixOverlay.set(1, -1, True)
    sixRotData = RotationData(sixOverlay, SIX_KICKS)

    nineOverlay = PieceUtils.initOverlay()
    nineOverlay.set(0, 1, True)
    nineOverlay.set(0, 0, True)
    nineOverlay.set(0, -1, True)
    nineOverlay.set(-1, -1, True)
    nineRotData = RotationData(nineOverlay, NINE_KICKS)

    return [twelveRotData, threeRotData, sixRotData, nineRotData]


class BluePiece:
    color = StandardColor.BLUE
    rotations = initRotations()
