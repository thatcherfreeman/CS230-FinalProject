from collections import deque

from game.GameDriver import GameDriver
from game.GameState import GameState


class SimulatorDriver(GameDriver):
    def __init__(self, state: GameState = None):
        super().__init__(state)
        """This is a deque of integers. The top element contains the number of actions to pop off of another deque to 
        reverse the most recent action. """
        self.numActionsToReverseDeque = deque()
        """This is a deque of lambdas. When an action is reversed, the top element of the 'numActionsToReverseDeque' 
        deque is popped, then that many elements of this deque are popped and performed. The goal is to duplicate as 
        little game state as possible during a recursive search."""
        self.reversalFunctionDeque = deque()
        self.numActionsToReverse = 0
        """This class overrides typical piece generation to allow the simulator to specify which piece comes next."""
        self.nextPiece = None
