from enum import Enum

from piece.standard.definitions import BluePiece, OrangePiece
from piece.standard.definitions.CyanPiece import CyanPiece
from piece.standard.definitions.GreenPiece import GreenPiece
from piece.standard.definitions.PurplePiece import PurplePiece
from piece.standard.definitions.RedPiece import RedPiece
from piece.standard.definitions.YellowPiece import YellowPiece


class PieceInfo:
    def __init__(self, color, rotations):
        self.color = color
        self.rotations = rotations


class StandardPiece(Enum):

    I = PieceInfo(CyanPiece.color, CyanPiece.rotations),
    O = PieceInfo(YellowPiece.color, YellowPiece.rotations),
    T = PieceInfo(PurplePiece.color, PurplePiece.rotations),
    S = PieceInfo(GreenPiece.color, GreenPiece.rotations),
    Z = PieceInfo(RedPiece.color, RedPiece.rotations),
    J = PieceInfo(BluePiece.color, BluePiece.rotations),
    L = PieceInfo(OrangePiece.color, OrangePiece.rotations)
