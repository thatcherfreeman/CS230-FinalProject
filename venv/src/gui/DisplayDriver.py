from typing import Tuple, Set

from game.GameDriver import GameDriver
from game.GameState import PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH
from game.piece.TetrisPiece import TetrisPiece
from game.piece.standard.StandardColor import StandardColor
from grid.ListGrid import ListGrid
from gui.GameDisplay import GameDisplay


class DisplayDriver(GameDriver):
    """A subclass of GameDriver that alters the display to track the state of the game"""
    def __init__(self, display: GameDisplay):
        # A set of locations the current piece occupies on the playfield.
        self.currentPieceSquares: Set[Tuple[int, int]] = set()
        self.display = display
        self.playfieldColorGrid = ListGrid(PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT, StandardColor.NONE)
        super().__init__()
        # init display for queued pieces
        self.refreshQueuedPiecesDisplay()

    def setPlayfieldCellColor(self, x: int, y: int, color: StandardColor):
        if y < PLAYFIELD_HEIGHT:
            self.display.setPlayfieldCellColor(x, y, color)
            self.playfieldColorGrid.set(x, y, color)

    def placePiece(self):
        super().placePiece()
        self.currentPieceSquares.clear()
        # TODO: visual flair for piece placement?

    def setCurrentPieceLocation(self, location: Tuple[int, int]):
        oldPieceSquares = self.currentPieceSquares
        piece = self.state.currentPiece
        super().setCurrentPieceLocation(location)
        newPieceSquares = set()
        centerX = location[0]
        centerY = location[1]
        for x in range(-2, 2):
            for y in range(-2, 2):
                if piece.overlay.get(x, y):
                    newPieceSquares.add((x + centerX, y + centerY))
        self.currentPieceSquares = newPieceSquares
        relevantSquares = oldPieceSquares.union(newPieceSquares)
        # only change the color of the minimum number of grid squares on the playfield
        for square in relevantSquares:
            if square not in newPieceSquares:
                self.setPlayfieldCellColor(square[0], square[1], StandardColor.NONE)
            if square not in oldPieceSquares:
                self.setPlayfieldCellColor(square[0], square[1], piece.color)

    def setHeldPiece(self, piece: TetrisPiece):
        super().setHeldPiece(piece)
        self.display.setHeldPiece(piece)

    def setHoldAvailable(self, holdAvailable: bool):
        super().setHoldAvailable(holdAvailable)
        self.display.setHoldAvailable(holdAvailable)

    def addPoints(self, points: int):
        super().addPoints(points)
        self.display.setScoreText(str(self.state.points))

    def generateNewPiece(self):
        super().generateNewPiece()
        self.refreshQueuedPiecesDisplay()

    def refreshQueuedPiecesDisplay(self):
        queuedPieces = []
        for piece in self.state.pieceQueue:
            queuedPieces.append(piece)
        self.display.setQueuedPieces(queuedPieces)

    def copySquare(self, fromSquare: Tuple[int, int], toSquare: Tuple[int, int]):
        super().copySquare(fromSquare, toSquare)
        if toSquare[1] < PLAYFIELD_HEIGHT:
            color = StandardColor.NONE
            if fromSquare[1] < PLAYFIELD_HEIGHT:
                color = self.playfieldColorGrid.get(fromSquare[0], fromSquare[1])
            self.setPlayfieldCellColor(toSquare[0], toSquare[1], color)
        # Empty out copied-from squares for visual effect
        if fromSquare[1] < PLAYFIELD_HEIGHT:
            self.setPlayfieldCellColor(fromSquare[0], fromSquare[1], StandardColor.NONE)

    def clearSquare(self, x: int, y: int):
        super().clearSquare(x, y)
        if y < PLAYFIELD_HEIGHT:
            self.setPlayfieldCellColor(x, y, StandardColor.NONE)
