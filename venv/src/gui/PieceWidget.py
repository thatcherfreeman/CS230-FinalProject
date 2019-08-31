import tkinter as tk

from grid.ListGrid import ListGrid
from gui.ColorDisplayGrid import ColorDisplayGrid
from gui.DisplayConstants import COLOR_MAP
from piece.TetrisPiece import TetrisPiece
from piece.standard.StandardColor import StandardColor

PIECE_BACKGROUND_COLOR = "black"

PIECE_GRID_WIDTH = 5
PIECE_GRID_HEIGHT = 5

PIECE_CELL_HEIGHT = 1
PIECE_CELL_WIDTH = 1
GRID_LINE_THICKNESS = 0


class PieceWidget:
    """A UI element that has a 5x5 grid to display a single tetris piece."""
    def __init__(self, parentWidget):
        self.displayGrid = ColorDisplayGrid(parentWidget, PIECE_GRID_HEIGHT, PIECE_GRID_WIDTH,
                                            PIECE_CELL_HEIGHT, PIECE_CELL_WIDTH, GRID_LINE_THICKNESS)
        self.initOutsides()

    def initOutsides(self):
        """The tetris pieces are 4x4, but we want to center them, so this initializes the outer layer of grid cells
        to the empty color """
        color = COLOR_MAP[StandardColor.NONE]
        for i in range(0, PIECE_GRID_WIDTH):
            self.displayGrid.setColor(i, PIECE_GRID_WIDTH - 1, color)
            self.displayGrid.setColor(PIECE_GRID_WIDTH - 1, i, color)

    def setPiece(self, tetrisPiece: TetrisPiece):
        absentColor = COLOR_MAP[StandardColor.NONE]
        presentColor = COLOR_MAP[tetrisPiece.color]
        for x in range(0, 4):
            xIdx = x - 2
            for y in range(0, 4):
                yIdx = y - 2
                color = presentColor if tetrisPiece.overlay.get(xIdx, yIdx) else absentColor
                self.displayGrid.setColor(x, y, color)

    def getFrame(self):
        return self.displayGrid.getFrame()