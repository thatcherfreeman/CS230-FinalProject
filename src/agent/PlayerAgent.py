from typing import Tuple, List

from agent.Action import Action
from agent.Agent import Agent
from game.GameState import GameState


class PlayerAgent(Agent):
    def __init__(self):
        pass

    def chooseActions(self, state: GameState) -> Tuple[List[Action], bool]:
        # TODO: Implement this by returning a queue of actions. The queue will be populated asynchronously when a
        #  user presses a control key (like 'W' for 'move left'). Figure out some way to bind handlers for key
        #  presses. The boolean part of the return value should always be 'false' for a human player.
        raise NotImplementedError
