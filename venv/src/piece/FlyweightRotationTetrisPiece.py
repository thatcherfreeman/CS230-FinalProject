from typing import List

from grid.OffsetOverlay import OffsetOverlay
from piece.TetrisPiece import TetrisPiece
from piece.standard.StandardColor import StandardColor


class FlyweightRotationTetrisPiece(TetrisPiece):
    """A tetris piece that uses the flyweight pattern to avoid duplicating common overlays"""
    def __init__(self, color: StandardColor, rotations: List[OffsetOverlay]):
        """The parameter 'rotations' should be length 4 and have the overlays in the following order:
        12 o'Clock, 3 o'Clock, 6 o'Clock, 9 o'Clock"""
        self.__rotations = rotations
        self.__rotIdx = 0
        super().__init__(self.__rotations[self.__rotIdx], color)

    def rotateCW(self):
        self.__rotIdx = (self.__rotIdx + 1) % 4
        self.overlay = self.__rotations[self.__rotIdx]

    def rotateCCW(self):
        self.__rotIdx = (self.__rotIdx - 1) % 4
        self.overlay = self.__rotations[self.__rotIdx]