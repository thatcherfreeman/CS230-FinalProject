from collections import deque
from typing import Callable


class StateChangesStack:
    """This class can be used to bundle individual state changes into 'commits' that can be reversed by
    calling 'revert'. Use the 'addRevertAction' method to add a Callable to the commit that, when reverted,
    will be invoked."""
    def __init__(self):
        """This is a deque of integers. The top element contains the number of actions to pop off of another deque to
                reverse the most recent action. """
        self.__numActionsToReverseDeque = deque()
        """This is a deque of lambdas. When an action is reversed, the top element of the 'numActionsToReverseDeque' deque is 
        popped, then that many elements of this deque are popped and performed. The goal is to duplicate as little game 
        state as possible during a recursive search. """
        self.__reversalFunctionDeque = deque()
        self.__numActionsToReverse = 0

    def commit(self):
        self.__numActionsToReverseDeque.append(self.__numActionsToReverse)
        self.__numActionsToReverse = 0

    def revert(self):
        # This should never be called with outstanding uncommitted actions
        if self.__numActionsToReverse != 0:
            raise ValueError("Cannot revert with uncommitted actions on stack!")
        if len(self.__numActionsToReverseDeque) == 0:
            raise ValueError("No committed changes, cannot revert!")
        actionsToReverse = self.__numActionsToReverseDeque.pop()
        for i in range(0, actionsToReverse):
            reverseLambda = self.__reversalFunctionDeque.pop()
            reverseLambda()

    def addRevertAction(self, action: Callable):
        self.__numActionsToReverse += 1
        self.__reversalFunctionDeque.append(action)
