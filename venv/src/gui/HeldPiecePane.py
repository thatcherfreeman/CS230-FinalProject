import tkinter as tk

from gui.DisplayConstants import BACKDROP_COLOR, UI_FONT
from gui.PieceWidget import PieceWidget
from game.piece.TetrisPiece import TetrisPiece

HELD_PIECE_TEXT = "Hold (Press Q)"
HOLD_AVAILABLE_COLOR = "black"
HOLD_UNAVAILABLE_COLOR = "gray68"


class HeldPiecePane:
    """A UI element that displays the currently held piece"""
    def __init__(self, parentWidget):
        self.__masterWidget = tk.Frame(parentWidget, bg=BACKDROP_COLOR)
        self.pieceWidget = PieceWidget(self.__masterWidget)
        self.holdLabel = tk.Label(self.__masterWidget, bg=BACKDROP_COLOR, text=HELD_PIECE_TEXT,
                                  fg=HOLD_AVAILABLE_COLOR, font=UI_FONT)
        self.placeWidgets()

    def placeWidgets(self):
        self.holdLabel.pack()
        self.pieceWidget.getFrame().pack()

    def getFrame(self):
        return self.__masterWidget

    def setHeldPiece(self, piece: TetrisPiece):
        self.pieceWidget.setPiece(piece)

    def setHoldAvailable(self, holdAvailable: bool):
        fontColor = HOLD_AVAILABLE_COLOR if holdAvailable else HOLD_UNAVAILABLE_COLOR
        self.holdLabel.configure(fg=fontColor)
