import tkinter as tk

from grid.ListGrid import ListGrid
from state.GameState import PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT, PIECE_QUEUE_LEN

# Combined cell width is the sum of the width of the colored cell and the width of the left gridline.
# The same is true of combined cell height, except in the vertical direction.
COMBINED_CELL_WIDTH = 45
COMBINED_CELL_HEIGHT = 45
GRID_LINE_THICKNESS = 5

TOTAL_PLAYFIELD_WIDTH = COMBINED_CELL_WIDTH * PLAYFIELD_WIDTH + GRID_LINE_THICKNESS
TOTAL_PLAYFIELD_HEIGHT = COMBINED_CELL_HEIGHT * PLAYFIELD_HEIGHT + GRID_LINE_THICKNESS

EMPTY_CELL_COLOR = "gray"
GRID_LINE_COLOR = "black"
INFO_PANE_COLOR = "blanched almond"


class GameDisplay:
    """An object that abstracts the technical details of the GUI into a simple interface"""
    def __init__(self, parentWidget):
        self.mainCanvas = tk.Canvas(parentWidget)  # Main canvas has a flexible size
        self.playfieldCanvas = tk.Canvas(self.mainCanvas, width=TOTAL_PLAYFIELD_WIDTH, height=TOTAL_PLAYFIELD_HEIGHT)
        self.playfield = ListGrid(PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT, None)
        self.heldPiece = None
        self.queuedPieces = [None] * PIECE_QUEUE_LEN
        self.titleLabel = None
        self.infoCanvas = tk.Canvas(self.mainCanvas, width=COMBINED_CELL_WIDTH * 4, height=TOTAL_PLAYFIELD_HEIGHT)
        self.infoCanvas.configure(background=INFO_PANE_COLOR)
        self.initGui()
        self.mainCanvas.pack()

    def initGui(self):
        self.initTitle()
        self.initInfoCanvas()
        self.initPlayfieldCells()
        self.initGridlines()
        self.titleLabel.pack()
        self.playfieldCanvas.pack(side=tk.LEFT)
        self.infoCanvas.pack(side=tk.LEFT)

    def initTitle(self):
        # TODO: get this text from a param in the constructor?
        self.titleLabel = tk.Label(self.mainCanvas, text="Danny's Tetris")

    def initInfoCanvas(self):
        # TODO: create sidebar with info like points, held piece, next pieces, etc.
        pass

    def initPlayfieldCells(self):
        # fill playfield
        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(0, PLAYFIELD_HEIGHT):
                topLeftX = x * COMBINED_CELL_WIDTH + GRID_LINE_THICKNESS
                topLeftY = (y + 1) * COMBINED_CELL_HEIGHT
                bottomRightX = topLeftX + COMBINED_CELL_WIDTH - GRID_LINE_THICKNESS
                bottomRightY = topLeftY - COMBINED_CELL_HEIGHT + GRID_LINE_THICKNESS
                tile = self.playfieldCanvas.create_rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY,
                                                             fill=EMPTY_CELL_COLOR)
                self.playfield.set(x, y, tile)

    def initGridlines(self):
        # fill vertical gridlines
        for x in range(0, PLAYFIELD_WIDTH + 1):
            topLeftX = x * COMBINED_CELL_WIDTH
            topLeftY = COMBINED_CELL_HEIGHT * PLAYFIELD_HEIGHT + GRID_LINE_THICKNESS
            bottomRightX = topLeftX + GRID_LINE_THICKNESS
            bottomRightY = 0
            self.playfieldCanvas.create_rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY, fill=GRID_LINE_COLOR)

        # fill horizontal gridlines
        for y in range(0, PLAYFIELD_HEIGHT + 1):
            topLeftX = 0
            topLeftY = y * COMBINED_CELL_HEIGHT + GRID_LINE_THICKNESS
            bottomRightX = COMBINED_CELL_WIDTH * PLAYFIELD_WIDTH + GRID_LINE_THICKNESS
            bottomRightY = y * COMBINED_CELL_HEIGHT
            self.playfieldCanvas.create_rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY, fill=GRID_LINE_COLOR)