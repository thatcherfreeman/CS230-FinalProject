from enum import Enum

from piece.standard.definitions.BluePiece import BluePiece
from piece.standard.definitions.CyanPiece import CyanPiece
from piece.standard.definitions.GreenPiece import GreenPiece
from piece.standard.definitions.OrangePiece import OrangePiece
from piece.standard.definitions.PurplePiece import PurplePiece
from piece.standard.definitions.RedPiece import RedPiece
from piece.standard.definitions.YellowPiece import YellowPiece


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

    # def color(self):
    #     return self.color
    #
    # def rotations(self):
    #     return self.rotations
