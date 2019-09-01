import tkinter as tk
from typing import List

from gui.ColorDisplayGrid import ColorDisplayGrid
from gui.DisplayConstants import BACKDROP_COLOR, COLOR_MAP, UI_FONT
from gui.HeldPiecePane import HeldPiecePane
from gui.InfoPane import InfoPane
from game.piece.TetrisPiece import TetrisPiece
from game.piece.standard.StandardColor import StandardColor
from game.GameState import PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT

PLAYFIELD_CELL_WIDTH = 4
PLAYFIELD_CELL_HEIGHT = 2
GRID_LINE_THICKNESS = 1

SPACE_BETWEEN_PANES = 40


class GameDisplay:
    """An object that abstracts the technical details of the GUI into a simple interface. Non-GUI logic should interact
    directly with this to modify the GUI."""
    def __init__(self, parentWidget):
        self.__masterFrame = tk.Frame(parentWidget, bg=BACKDROP_COLOR)  # Master frame has a flexible size
        self.playfieldDisplay = ColorDisplayGrid(self.__masterFrame, PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH,
                                                 PLAYFIELD_CELL_HEIGHT, PLAYFIELD_CELL_WIDTH, GRID_LINE_THICKNESS)
        self.titleLabel = None
        self.heldPiecePane = HeldPiecePane(self.__masterFrame)
        self.infoPane = InfoPane(self.__masterFrame)
        self.initGui()
        self.__masterFrame.pack()

    def setPlayfieldCellColor(self, x: int, y: int, color: StandardColor):
        self.playfieldDisplay.setColor(x, y, COLOR_MAP[color])

    def setHoldAvailable(self, holdAvailable: bool):
        self.heldPiecePane.setHoldAvailable(holdAvailable)

    def setHeldPiece(self, piece: TetrisPiece):
        self.heldPiecePane.setHeldPiece(piece)

    def setQueuedPieces(self, pieces: List[TetrisPiece]):
        self.infoPane.setQueuedPieces(pieces)

    def setScoreText(self, scoreText: str):
        self.infoPane.setScoreText(scoreText)

    def initGui(self):
        self.initTitle()
        self.titleLabel.pack()
        self.heldPiecePane.getFrame().pack(padx=SPACE_BETWEEN_PANES, side=tk.LEFT)
        self.playfieldDisplay.getFrame().pack(padx=SPACE_BETWEEN_PANES, side=tk.LEFT)
        self.infoPane.getFrame().pack(padx=SPACE_BETWEEN_PANES, side=tk.LEFT)

    def initTitle(self):
        # TODO: get this text from a param in the constructor?
        self.titleLabel = tk.Label(self.__masterFrame, text="Danny's Tetris", bg=BACKDROP_COLOR, font=UI_FONT)

    def getFrame(self):
        return self.__masterFrame
