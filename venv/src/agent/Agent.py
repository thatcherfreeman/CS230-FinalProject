from typing import List, Tuple

from agent.Action import Action
from game.GameState import GameState


class Agent:
    def __init__(self):
        pass

    def chooseActions(self, state: GameState) -> Tuple[List[Action], bool]:
        """Returns a list of actions to be performed and a boolean indicating whether more actions will be supplied
        before piece placement"""
        raise NotImplementedError
