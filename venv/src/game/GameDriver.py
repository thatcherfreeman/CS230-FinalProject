from collections import deque
from math import trunc
from typing import List, Tuple, Deque

from game.piece.TetrisPiece import TetrisPiece
from game.Direction import Direction
from game.GameState import GameState, PIECE_QUEUE_LEN, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT, BUFFER_HEIGHT
from game.PieceGenerator import PieceGenerator

# the value at each index is the score reward for clearing (index + 1) lines. This system is from level 1 of the
# popular Nintendo Game Boy version.
CLEAR_POINTS = [40, 100, 300, 1200]

PIECE_SPAWN_X = 5
PIECE_SPAWN_Y = PLAYFIELD_HEIGHT + 1


def getClearPoints(numRowsCleared: int):
    return CLEAR_POINTS[numRowsCleared - 1]


class GameDriver:
    """A class containing a tetris game state as well as being able to update the state in response to player actions.
    This class contains all of the game logic for Tetris."""
    def __init__(self):
        self.state = GameState()
        self.pieceGenerator = PieceGenerator()
        self.initGameState()

    def initGameState(self):
        self.setCurrentPiece(self.pieceGenerator.generatePiece())
        self.setCurrentPieceLocation((int(trunc(PLAYFIELD_WIDTH/2)), PLAYFIELD_HEIGHT))
        self.state.pieceQueue = deque()
        for i in range(0, PIECE_QUEUE_LEN):
            self.state.pieceQueue.append(self.pieceGenerator.generatePiece())

    def setCurrentPiece(self, piece: TetrisPiece):
        self.state.currentPiece = piece

    def setCurrentPieceLocation(self, location: Tuple[int, int]):
        self.state.currentPieceLocation = location

    def setQueuedPieces(self, pieces: List[TetrisPiece]):
        self.state.pieceQueue = pieces

    def setHoldAvailable(self, holdAvailable: bool):
        self.state.holdAvailable = holdAvailable

    def setHeldPiece(self, piece: TetrisPiece):
        self.state.heldPiece = piece
        self.setHoldAvailable(False)

    def holdPiece(self):
        """Returns True if and only if the hold was successful"""
        if not self.state.holdAvailable:
            return False
        priorHeldPiece = self.state.heldPiece
        pieceToHold = self.state.currentPiece
        self.setHeldPiece(pieceToHold)
        if priorHeldPiece is None:
            self.generateNewPiece()
        else:
            self.state.currentPiece = priorHeldPiece
            self.setCurrentPieceLocation((PIECE_SPAWN_X, PIECE_SPAWN_Y))
        return True

    def generateNewPiece(self):
        newPiece = self.state.pieceQueue.popleft()
        self.state.pieceQueue.append(self.pieceGenerator.generatePiece())
        self.state.currentPiece = newPiece
        self.setCurrentPieceLocation((PIECE_SPAWN_X, PIECE_SPAWN_Y))

    def rotatePiece(self, clockwise: bool):
        """Returns True if the rotation was performed, returns False if it was not."""
        piece = self.state.currentPiece
        kickTranslations = None
        if clockwise:
            kickTranslations = piece.wallKicks.cwKicks
            piece.rotateCW()
        else:
            kickTranslations = piece.wallKicks.ccwKicks
            piece.rotateCCW()
        currentLocation = self.state.currentPieceLocation
        for kickTranslation in kickTranslations:
            if not self.checkCollision(kickTranslation[0], kickTranslation[1]):
                location = (currentLocation[0] + kickTranslation[0], currentLocation[1] + kickTranslation[1])
                self.setCurrentPieceLocation(location)
                return True
        # no legal kick configuration worked so this is an illegal rotation, revert it
        if clockwise:
            piece.rotateCCW()
        else:
            piece.rotateCW()
        return False

    # Generally, it's the caller's responsibility to finalize the piece placement (clear rows, generate a new piece,
    # reset the piece position) if this is a downward movement that failed.
    def movePiece(self, direction: Direction):
        """Returns True if the move was performed, returns False if it was not."""
        collision = self.checkCollision(direction.deltaX, direction.deltaY)
        if not collision:
            location = self.state.currentPieceLocation
            centerX = location[0]
            centerY = location[1]
            deltaX = direction.deltaX
            deltaY = direction.deltaY
            self.setCurrentPieceLocation((centerX + deltaX, centerY + deltaY))
            return True
        return False

    def checkCollision(self, deltaX, deltaY):
        piece = self.state.currentPiece
        location = self.state.currentPieceLocation
        centerX = location[0]
        centerY = location[1]
        for x in range(-2, 2):
            for y in range(-2, 2):
                pieceOccupies = piece.overlay.get(x, y)
                boardOccupies = self.isBoardSpaceOccupied(x + centerX + deltaX, y + centerY + deltaY)
                if pieceOccupies and boardOccupies:
                    return True
        return False

    def placePiece(self):
        piece = self.state.currentPiece
        centerX = self.state.currentPieceLocation[0]
        centerY = self.state.currentPieceLocation[1]
        for x in range(-2, 2):
            for y in range(-2, 2):
                if piece.overlay.get(x, y):
                    self.state.overlay.set(x + centerX, y + centerY, True)
        self.setHoldAvailable(True)

    def checkAndClearLines(self):
        """Returns (point value generated by clears, game over)"""
        piece = self.state.currentPiece
        centerY = self.state.currentPieceLocation[1]
        rowsToClear = []
        # Find each row the piece occupies
        for y in range(-2, 2):
            for x in range(-2, 2):
                if piece.overlay.get(x, y):
                    if self.isRowFull(y + centerY):
                        rowsToClear.append(y + centerY)
                    break
        points = self.clearLines(rowsToClear)
        # check for game over
        for x in range(0, PLAYFIELD_WIDTH):
            if self.state.overlay.get(x, PLAYFIELD_HEIGHT):
                return points, True
        self.addPoints(points)
        return points, False

    def isRowFull(self, y: int):
        for x in range(0, PLAYFIELD_WIDTH):
            if not self.state.overlay.get(x, y):
                return False
        return True

    def clearLines(self, rowsToClear: List[int]):
        """Returns point value generated by clears"""
        if len(rowsToClear) == 0:
            return 0

        clearParamsList = []
        # (bottom of block that needs to be shifted down, top of block that needs to be shifted
        # down (inclusive), rows to shift by)
        curClearParams = None
        for i in range(0, len(rowsToClear)):
            rowNum = rowsToClear[i]
            if curClearParams is not None:
                if curClearParams[0] == rowNum:
                    curClearParams[0] = rowNum + 1
                    curClearParams[2] = i + 1
                else:
                    curClearParams[1] = rowNum - 1
                    clearParamsList.append(curClearParams)
                    curClearParams = [rowNum + 1, PLAYFIELD_HEIGHT + BUFFER_HEIGHT - 1, i + 1]
            else:
                curClearParams = [rowNum + 1, PLAYFIELD_HEIGHT + BUFFER_HEIGHT - 1, i + 1]
        clearParamsList.append(curClearParams)
        rowsCleared = 0
        points = 0
        for clearParams in clearParamsList:
            # Clearing multiple non-contiguous rows is not worth as much as clearing the same number of contiguous rows
            points += getClearPoints(clearParams[2] - rowsCleared)
            rowsCleared += clearParams[2]
            self.clearBlock(clearParams[0], clearParams[1], clearParams[2])
        # Clear the top rows out
        for y in range(PLAYFIELD_HEIGHT + BUFFER_HEIGHT - rowsCleared, PLAYFIELD_HEIGHT + BUFFER_HEIGHT):
            for x in range(0, PLAYFIELD_WIDTH):
                self.clearSquare(x, y)
        return points

    def clearBlock(self, bottomRowToShift: int, topRowToShift: int, rowsToShift: int):
        """Clears a block of fully completed lines and shifts the contents of higher blocks down"""
        for row in range(bottomRowToShift, topRowToShift + 1):
            for x in range(0, PLAYFIELD_WIDTH):
                self.copySquare((x, row), (x, row - rowsToShift))

    def copySquare(self, fromSquare: Tuple[int, int], toSquare: Tuple[int, int]):
        """Copies the contents of one grid location to another"""
        overlay = self.state.overlay
        overlay.set(toSquare[0], toSquare[1], overlay.get(fromSquare[0], fromSquare[1]))

    def clearSquare(self, x: int, y: int):
        """Clears the contents of a grid location"""
        self.state.overlay.set(x, y, False)

    def isBoardSpaceOccupied(self, x: int, y: int):
        if x < 0 or y < 0 or x >= PLAYFIELD_WIDTH or y >= (PLAYFIELD_HEIGHT + BUFFER_HEIGHT):
            return True
        return self.state.overlay.get(x, y)

    def addPoints(self, points: int):
        self.state.points += points
