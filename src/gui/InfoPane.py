import tkinter as tk
from typing import List

from gui.DisplayConstants import BACKDROP_COLOR, UI_FONT, UI_TEXT_COLOR
from gui.PieceWidget import PieceWidget
from game.piece.TetrisPiece import TetrisPiece
from game.GameState import PIECE_QUEUE_LEN

INFO_PANE_WIDTH = 200
QUEUED_PIECES_TEXT = "Next"

PIECE_WIDGET_ROW_SPAN = 1
SCORE_TITLE_TEXT = "Score"
INITAL_SCORE_TEXT = "0"
SCORE_LABEL_WIDTH = 20


class InfoPane:
    """A UI element that displays the pieces up next and the current score"""
    def __init__(self, parentWidget):
        self.__masterWidget = tk.Frame(parentWidget, bg=BACKDROP_COLOR)
        self.queuedPiecesWidget = tk.Frame(self.__masterWidget, bg=BACKDROP_COLOR)
        self.queuedPieceWidgets = None
        self.initPieceQueueWidget()
        self.scoreWidget = tk.Label(self.__masterWidget, bg=BACKDROP_COLOR, fg=UI_TEXT_COLOR,
                                    text=INITAL_SCORE_TEXT, font=UI_FONT, width=20)
        self.placeWidgets()

    def initPieceQueueWidget(self):
        pieceQueueLabel = tk.Label(self.queuedPiecesWidget, fg=UI_TEXT_COLOR, bg=BACKDROP_COLOR,
                                   text=QUEUED_PIECES_TEXT, font=UI_FONT)
        pieceQueueLabel.grid(row=0, column=0)
        self.queuedPieceWidgets = [PieceWidget(self.queuedPiecesWidget) for i in range(0, PIECE_QUEUE_LEN)]
        for i in range(0, PIECE_QUEUE_LEN):
            self.queuedPieceWidgets[i].getFrame().grid(row=(i + 1), column=0, sticky='n')

    def placeWidgets(self):
        self.queuedPiecesWidget.grid(row=0, column=0)
        tk.Label(self.__masterWidget, bg=BACKDROP_COLOR, fg=UI_TEXT_COLOR, text=SCORE_TITLE_TEXT,
                 font=UI_FONT).grid(row=1, column=0)
        self.scoreWidget.grid(row=2, column=0)

    def getFrame(self):
        return self.__masterWidget

    def setQueuedPieces(self, pieces: List[TetrisPiece]):
        if len(pieces) != PIECE_QUEUE_LEN:
            raise ValueError("trying to set queued pieces with incorrect length")
        for i in range(0, PIECE_QUEUE_LEN):
            self.queuedPieceWidgets[i].setPiece(pieces[i])

    def setScoreText(self, scoreText: str):
        self.scoreWidget.configure(text=scoreText)
