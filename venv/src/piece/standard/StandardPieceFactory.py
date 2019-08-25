from piece.FlyweightRotationTetrisPiece import FlyweightRotationTetrisPiece
from piece.standard.StandardPiece import StandardPiece


def getPiece(kind: StandardPiece):
    return FlyweightRotationTetrisPiece(kind.color, kind.rotations)
