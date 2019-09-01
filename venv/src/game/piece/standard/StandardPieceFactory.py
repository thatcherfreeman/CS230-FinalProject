from game.piece.FlyweightRotationTetrisPiece import FlyweightRotationTetrisPiece
from game.piece.standard.StandardPiece import StandardPiece


def getPiece(kind: StandardPiece):
    return FlyweightRotationTetrisPiece(kind.color, kind.rotations)
