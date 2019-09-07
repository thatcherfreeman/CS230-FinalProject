from collections import deque
from typing import Tuple, Callable

from game.Direction import Direction
from game.GameDriver import GameDriver, PIECE_SPAWN_Y, PIECE_SPAWN_X
from game.piece.TetrisPiece import TetrisPiece


class ReversibleDriver(GameDriver):
    def __init__(self):
        super().__init__()
        """This is a deque of integers. The top element contains the number of actions to pop off of another deque to 
        reverse the most recent action. """
        self.numActionsToReverseDeque = deque()
        """This is a deque of lambdas. When an action is reversed, the top element of the 'numActionsToReverseDeque' deque is 
        popped, then that many elements of this deque are popped and performed. The goal is to duplicate as little game 
        state as possible during a recursive search. """
        self.reversalFunctionDeque = deque()
        self.numActionsToReverse = 0
        """This class overrides typical piece generation to allow the simulator to specify which piece comes next."""
        self.nextPiece = None

    def initGameState(self):
        self.state.pieceQueue = deque()

    def commit(self):
        self.numActionsToReverseDeque.append(self.numActionsToReverse)
        self.numActionsToReverse = 0

    def revert(self):
        # This should never be called with outstanding uncommitted actions
        actionsToReverse = self.numActionsToReverseDeque.pop()
        for i in range(0, actionsToReverse):
            reverseLambda = self.reversalFunctionDeque.pop()
            reverseLambda()

    def __addRevertAction(self, action: Callable):
        self.numActionsToReverse += 1
        self.reversalFunctionDeque.append(action)

    def __putNextPiece(self, piece: TetrisPiece):
        self.nextPiece = piece

    def setNextPiece(self, piece: TetrisPiece):
        prevNextPiece = self.nextPiece
        self.nextPiece = piece
        self.numActionsToReverse += 1
        self.reversalFunctionDeque.append(lambda: self.__putNextPiece(prevNextPiece))

    def __restoreQueuedPiece(self, piece: TetrisPiece):
        self.state.pieceQueue.pushLeft(piece)

    def generateNewPiece(self):
        prevPiece = self.state.currentPiece
        prevLocation = self.state.currentPieceLocation

        if len(self.state.pieceQueue) > 0:
            self.state.currentPiece = self.state.pieceQueue.popleft()
            self.__addRevertAction(lambda: self.__restoreQueuedPiece(self.state.currentPiece))
        else:
            self.state.currentPiece = self.nextPiece
            self.nextPiece = None
            self.__addRevertAction(lambda: self.__putNextPiece(self.state.currentPiece))

        self.setCurrentPieceLocation((PIECE_SPAWN_X, PIECE_SPAWN_Y))
        self.__addRevertAction(lambda: self.setCurrentPiece(prevPiece))
        self.__addRevertAction(lambda: self.setCurrentPieceLocation(prevLocation))

    def movePiece(self, direction: Direction):
        initialLocation = self.state.currentPieceLocation
        collision = super().movePiece(direction)
        if collision:
            self.__addRevertAction(lambda: self.setCurrentPieceLocation(initialLocation))
        return collision

    def reverseCWRotation(self, initialLocation: Tuple[int, int]):
        self.state.currentPiece.rotateCCW()
        self.setCurrentPieceLocation(initialLocation)

    def reverseCCWRotation(self, initialLocation: Tuple[int, int]):
        self.state.currentPiece.rotateCW()
        self.setCurrentPieceLocation(initialLocation)

    def rotatePiece(self, clockwise: bool):
        initialLocation = self.state.currentPieceLocation
        possible = super().rotatePiece(clockwise)
        if possible:
            if clockwise:
                self.__addRevertAction(lambda: self.reverseCWRotation(initialLocation))
            else:
                self.__addRevertAction(lambda: self.reverseCCWRotation(initialLocation))
        return possible

    def setHeldPiece(self, piece: TetrisPiece):
        self.state.heldPiece = piece

    def reverseHoldPiece(self, priorHeldPiece: TetrisPiece, heldPiece: TetrisPiece, initialLocation: Tuple[int, int]):
        self.setCurrentPiece(heldPiece)
        self.setHeldPiece(priorHeldPiece)
        self.setHoldAvailable(True)
        self.setCurrentPieceLocation(initialLocation)

    def reverseFirstHoldOfGame(self):
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
                self.__addRevertAction(self.reverseFirstHoldOfGame)
            else:
                self.__addRevertAction(lambda: self.reverseHoldPiece(priorHeldPiece, self.state.heldPiece, initialLocation))
        return possible

    # TODO: checkAndClearLines()

    # TODO: clearBlock()

