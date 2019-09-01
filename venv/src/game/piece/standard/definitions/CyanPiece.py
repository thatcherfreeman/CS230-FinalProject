from game.piece.WallKicks import WallKicks
from game.piece.standard import PieceUtils
from game.piece.standard.RotationData import RotationData
from game.piece.standard.StandardColor import StandardColor

TWELVE_CW_KICKS = [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]
TWELVE_CCW_KICKS = [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]

THREE_CW_KICKS = [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
THREE_CCW_KICKS = [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)]

SIX_CW_KICKS = [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)]
SIX_CCW_KICKS = [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]

NINE_CW_KICKS = [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]
NINE_CCW_KICKS = [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]


def initRotations():
    twelveOverlay = PieceUtils.initOverlay()
    twelveOverlay.set(-2, 0, True)
    twelveOverlay.set(-1, 0, True)
    twelveOverlay.set(0, 0, True)
    twelveOverlay.set(1, 0, True)
    twelveRotData = RotationData(twelveOverlay, WallKicks(TWELVE_CW_KICKS, TWELVE_CCW_KICKS))

    threeOverlay = PieceUtils.initOverlay()
    threeOverlay.set(0, -2, True)
    threeOverlay.set(0, -1, True)
    threeOverlay.set(0, 0, True)
    threeOverlay.set(0, 1, True)
    threeRotData = RotationData(threeOverlay, WallKicks(THREE_CW_KICKS, THREE_CCW_KICKS))

    sixOverlay = PieceUtils.initOverlay()
    sixOverlay.set(-2, -1, True)
    sixOverlay.set(-1, -1, True)
    sixOverlay.set(0, -1, True)
    sixOverlay.set(1, -1, True)
    sixRotData = RotationData(sixOverlay, WallKicks(SIX_CW_KICKS, SIX_CCW_KICKS))

    nineOverlay = PieceUtils.initOverlay()
    nineOverlay.set(-1, -2, True)
    nineOverlay.set(-1, -1, True)
    nineOverlay.set(-1, 0, True)
    nineOverlay.set(-1, 1, True)
    nineRotData = RotationData(nineOverlay, WallKicks(NINE_CW_KICKS, NINE_CCW_KICKS))

    return [twelveRotData, threeRotData, sixRotData, nineRotData]


class CyanPiece:
    color = StandardColor.CYAN
    rotations = initRotations()
