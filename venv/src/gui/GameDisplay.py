import tkinter as tk

from gui.ColorDisplayGrid import ColorDisplayGrid
from gui.DisplayConstants import CELL_HEIGHT, CELL_WIDTH, \
    GRID_LINE_THICKNESS
from gui.InfoPane import InfoPane
from state.GameState import PIECE_QUEUE_LEN, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT


class GameDisplay:
    """An object that abstracts the technical details of the GUI into a simple interface"""
    def __init__(self, parentWidget):
        self.__masterFrame = tk.Frame(parentWidget)  # Master frame has a flexible size
        self.playfieldDisplay = ColorDisplayGrid(self.__masterFrame, PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH,
                                                 CELL_HEIGHT, CELL_WIDTH, GRID_LINE_THICKNESS)
        self.titleLabel = None
        self.infoPanel = InfoPane(self.__masterFrame)
        self.initGui()
        self.__masterFrame.pack()

    def initGui(self):
        self.initTitle()
        self.titleLabel.pack()
        self.playfieldDisplay.getFrame().pack(side=tk.LEFT)
        self.infoPanel.getFrame().pack(padx=40, side=tk.LEFT)

    def initTitle(self):
        # TODO: get this text from a param in the constructor?
        self.titleLabel = tk.Label(self.__masterFrame, text="Danny's Tetris")

    def getFrame(self):
        return self.__masterFrame
