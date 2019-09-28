from collections import deque
from typing import Tuple

from agent.simulator.PiecePlacement import PiecePlacement
from agent.simulator.StateChangesStack import StateChangesStack
from game.Direction import Direction
from game.GameDriver import GameDriver
from game.GameState import GameState


class PathFindingDriver(GameDriver):
    def __init__(self, state: GameState = None):
        super().__init__(state)
        self.__reversalStack = StateChangesStack()
        self.nextPiece = None

    def initGameState(self):
        self.state.pieceQueue = deque()

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

    def movePiece(self, direction: Direction):
        initialLocation = self.state.currentPieceLocation
        collision = super().movePiece(direction)
        if collision:
            self.__reversalStack.addRevertAction(lambda: self.setCurrentPieceLocation(initialLocation))
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
                self.__reversalStack.addRevertAction(lambda: self.reverseCWRotation(initialLocation))
            else:
                self.__reversalStack.addRevertAction(lambda: self.reverseCCWRotation(initialLocation))
        return possible
