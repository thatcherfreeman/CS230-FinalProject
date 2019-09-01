import tkinter as tk

from grid.InvertedHeightOverlay import InvertedHeightOverlay
from grid.ListGrid import ListGrid
from gui.DisplayConstants import COLOR_MAP
from game.piece.standard.StandardColor import StandardColor

GRID_LINE_COLOR = "black"


class ColorDisplayGrid:
    """A UI element displaying a grid of variable-colored squares"""

    def __init__(self, parentWidget, gridHeight, gridWidth, cellHeight, cellWidth, gridLineThickness):
        self.__masterFrame = tk.Frame(parentWidget)
        self.__masterFrame.configure(bg=GRID_LINE_COLOR)
        self.displayGrid = ListGrid(gridWidth, gridHeight, None)
        self.initGrid(cellHeight, cellWidth, gridLineThickness)

    def getFrame(self):
        return self.__masterFrame

    # TODO: delete this if unused
    def get(self, x: int, y: int):
        return self.displayGrid.get(x, y)

    # this one too
    def set(self, x: int, y: int, value):
        self.displayGrid.set(x, y, value)

    def setColor(self, x: int, y: int, color: str):
        self.displayGrid.get(x, y).configure(bg=color)

    def initGrid(self, cellHeight, cellWidth, gridLineThickness):
        for x in range(0, self.displayGrid.width):
            for y in range(0, self.displayGrid.height):
                tile = tk.Label(self.__masterFrame, height=cellHeight, width=cellWidth)
                tile.grid(column=x, row=y, padx=gridLineThickness, pady=gridLineThickness)
                tile.configure(bg=COLOR_MAP[StandardColor.NONE])
                self.displayGrid.set(x, y, tile)
        self.displayGrid = InvertedHeightOverlay(self.displayGrid)
