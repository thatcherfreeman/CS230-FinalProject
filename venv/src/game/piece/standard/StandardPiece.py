from enum import Enum

from game.piece.standard.definitions.BluePiece import BluePiece
from game.piece.standard.definitions.CyanPiece import CyanPiece
from game.piece.standard.definitions.GreenPiece import GreenPiece
from game.piece.standard.definitions.OrangePiece import OrangePiece
from game.piece.standard.definitions.PurplePiece import PurplePiece
from game.piece.standard.definitions.RedPiece import RedPiece
from game.piece.standard.definitions.YellowPiece import YellowPiece


class StandardPiece(Enum):

    I = (CyanPiece.color, CyanPiece.rotations)
    O = (YellowPiece.color, YellowPiece.rotations)
    T = (PurplePiece.color, PurplePiece.rotations)
    S = (GreenPiece.color, GreenPiece.rotations)
    Z = (RedPiece.color, RedPiece.rotations)
    J = (BluePiece.color, BluePiece.rotations)
    L = (OrangePiece.color, OrangePiece.rotations)

    def __init__(self, color, rotations):
        self.color = color
        self.rotations = rotations
