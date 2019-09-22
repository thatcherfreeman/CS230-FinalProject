from typing import Tuple, List

from agent.simulator.PiecePlacement import PiecePlacement
from agent.simulator.StateChangesStack import StateChangesStack
from game.GameDriver import GameDriver, PIECE_SPAWN_Y, PIECE_SPAWN_X
from game.GameState import GameState, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT, BUFFER_HEIGHT
from game.piece.TetrisPiece import TetrisPiece


class SimulatorDriver(GameDriver):
    def __init__(self, state: GameState = None):
        super().__init__(state)
        self.__reversalStack = StateChangesStack()

        """Since a simulation driver just simulates moves from a starting game state, it can remember how many new 
        points have been generated during the simulation. This can be helpful for evaluation functions."""
        self.pointsDelta = 0
        self.nextPiece = None

    def commit(self):
        self.__reversalStack.commit()

    def revert(self):
        self.__reversalStack.revert()

    def __revertToPlacement(self, prevLocation: Tuple[int, int], prevRotIdx: int):
        self.state.currentPieceLocation = prevLocation
        self.state.currentPiece.setRotIdx(prevRotIdx)

    def setToPlacement(self, placement: PiecePlacement):
        prevLocation = self.state.currentPieceLocation
        prevRotIdx = self.state.currentPiece.getRotIdx()
        self.state.currentPiece.setRotIdx(placement.rotIdx)
        self.state.currentPieceLocation = placement.location
        self.__reversalStack.addRevertAction(lambda: self.__revertToPlacement(prevLocation, prevRotIdx))

    def __putNextPiece(self, piece: TetrisPiece):
        self.nextPiece = piece

    def setNextPiece(self, piece: TetrisPiece):
        prevNextPiece = self.nextPiece
        self.nextPiece = piece
        self.__reversalStack.addRevertAction(lambda: self.__putNextPiece(prevNextPiece))

    def __restoreQueuedPiece(self, piece: TetrisPiece):
        self.state.pieceQueue.appendleft(piece)

    def generateNewPiece(self):
        prevPiece = self.state.currentPiece
        prevLocation = self.state.currentPieceLocation
        self.setCurrentPieceLocation((PIECE_SPAWN_X, PIECE_SPAWN_Y))
        self.__reversalStack.addRevertAction(lambda: self.setCurrentPiece(prevPiece))
        self.__reversalStack.addRevertAction(lambda: self.setCurrentPieceLocation(prevLocation))

        if len(self.state.pieceQueue) > 0:
            self.state.currentPiece = self.state.pieceQueue.popleft()
            self.__reversalStack.addRevertAction(lambda: self.__restoreQueuedPiece(self.state.currentPiece))
        else:
            self.state.currentPiece = self.nextPiece
            self.nextPiece = None
            self.__reversalStack.addRevertAction(lambda: self.__putNextPiece(self.state.currentPiece))

    def setHeldPiece(self, piece: TetrisPiece):
        self.state.heldPiece = piece

    def __reverseHoldPiece(self, priorHeldPiece: TetrisPiece, heldPiece: TetrisPiece, initialLocation: Tuple[int, int]):
        self.setCurrentPiece(heldPiece)
        self.setHeldPiece(priorHeldPiece)
        self.setHoldAvailable(True)
        self.setCurrentPieceLocation(initialLocation)

    def __reverseFirstHoldOfGame(self):
        # The first hold of the game involves a call to 'generateNewPiece()'. Reversing that will reset our current
        # piece and location to the state we want it to be in.
        self.state.heldPiece = None
        self.setHoldAvailable(True)

    def holdPiece(self):
        priorHeldPiece = self.state.heldPiece
        initialLocation = self.state.currentPieceLocation
        possible = super().holdPiece()
        if possible:
            self.setHoldAvailable(False)
            if priorHeldPiece is None:
                self.__reversalStack.addRevertAction(self.__reverseFirstHoldOfGame)
            else:
                self.__reversalStack.addRevertAction(lambda: self.__reverseHoldPiece(priorHeldPiece, self.state.heldPiece, initialLocation))
        return possible

    def placePiece(self):
        prevHoldAvailable = self.state.holdAvailable
        super().placePiece()
        if not prevHoldAvailable:
            self.__reversalStack.addRevertAction(lambda: self.setHoldAvailable(False))
        invertBlocksList = list()
        piece = self.state.currentPiece
        centerX = self.state.currentPieceLocation[0]
        centerY = self.state.currentPieceLocation[1]
        for x in range(-2, 2):
            for y in range(-2, 2):
                if piece.overlay.get(x, y):
                    invertBlocksList.append((x + centerX, y + centerY))
        self.__reversalStack.addRevertAction(lambda: self.__invertBlocks(invertBlocksList))

    def __reverseAddPoints(self, newPoints: int):
        self.addPoints(-1 * newPoints)
        self.pointsDelta -= newPoints

    def checkAndClearLines(self) -> Tuple[int, bool]:
        pointsAdded, gameOver = super().checkAndClearLines()
        if gameOver or pointsAdded == 0:
            return pointsAdded, gameOver
        self.pointsDelta += pointsAdded
        self.__reversalStack.addRevertAction(lambda: self.__reverseAddPoints(pointsAdded))
        return pointsAdded, gameOver

    def clearTopRows(self, rowsToClear: int):
        invertBlocksList = list()
        for y in range(PLAYFIELD_HEIGHT + BUFFER_HEIGHT - rowsToClear, PLAYFIELD_HEIGHT + BUFFER_HEIGHT):
            for x in range(0, PLAYFIELD_WIDTH):
                if self.state.overlay.get(x, y):
                    invertBlocksList.append((x, y))
                self.clearSquare(x, y)
        if len(invertBlocksList) != 0:
            self.__reversalStack.addRevertAction(lambda: self.__invertBlocks(invertBlocksList))

    def __invertBlocks(self, locations: List[Tuple[int, int]]):
        """For each block location, invert the boolean value (set it to False if it's currently True, etc.)"""
        for location in locations:
            blockState = self.state.overlay.get(location[0], location[1])
            self.state.overlay.set(location[0], location[1], not blockState)

    def clearBlock(self, bottomRowToShift: int, topRowToShift: int, rowsToShift: int):
        """Clears a block of fully completed lines and shifts the contents of higher blocks down"""
        locationsToReverse = list()
        for row in range(bottomRowToShift, topRowToShift + 1):
            for x in range(0, PLAYFIELD_WIDTH):
                if self.state.overlay.get(x, row) != self.state.overlay.get(x, row - rowsToShift):
                    # This is a small optimization to save stack space, don't save locations of blocks that didn't
                    # change by clearing
                    locationsToReverse.append((x, row - rowsToShift))
                self.copySquare((x, row), (x, row - rowsToShift))
        if len(locationsToReverse) != 0:
            self.__reversalStack.addRevertAction(lambda: self.__invertBlocks(locationsToReverse))
