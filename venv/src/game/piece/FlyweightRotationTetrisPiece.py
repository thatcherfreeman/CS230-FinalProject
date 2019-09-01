from typing import List, Tuple

from game.piece.WallKicks import WallKicks
from game.piece.standard.RotationData import RotationData
from grid.OffsetOverlay import OffsetOverlay
from game.piece.TetrisPiece import TetrisPiece
from game.piece.standard.StandardColor import StandardColor


class FlyweightRotationTetrisPiece(TetrisPiece):
    """A tetris piece that uses the flyweight pattern to avoid duplicating common overlays and rotation data"""
    def __init__(self, color: StandardColor, rotations: List[RotationData]):
        """The parameter 'rotations' should be length 4 and have the overlays in the following order:
        12 o'Clock, 3 o'Clock, 6 o'Clock, 9 o'Clock"""
        self.__rotations = rotations
        self.__rotIdx = 0
        super().__init__(self.__rotations[self.__rotIdx].overlay, self.__rotations[self.__rotIdx].wallKicks, color)

    def rotateCW(self):
        self.__rotIdx = (self.__rotIdx + 1) % 4
        self.overlay = self.__rotations[self.__rotIdx].overlay
        self.wallKicks = self.__rotations[self.__rotIdx].wallKicks

    def rotateCCW(self):
        self.__rotIdx = (self.__rotIdx - 1) % 4
        self.overlay = self.__rotations[self.__rotIdx].overlay
        self.wallKicks = self.__rotations[self.__rotIdx].wallKicks
