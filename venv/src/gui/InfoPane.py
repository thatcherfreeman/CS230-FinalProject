import tkinter as tk

from gui.PieceWidget import PieceWidget

INFO_PANE_WIDTH = 200
INFO_PANE_COLOR = "blanched almond"


class InfoPane:
    def __init__(self, parentWidget):
        self.__masterWidget = tk.Frame(parentWidget)
        self.heldPieceWidget = PieceWidget(self.__masterWidget)
        self.queuedPiecesWidget = None
        self.initPieceQueueWidget()
        self.placeWidgets()

    def initPieceQueueWidget(self):
        pass

    def placeWidgets(self):
        self.heldPieceWidget.getFrame().pack()
        pass

    def getFrame(self):
        return self.__masterWidget
