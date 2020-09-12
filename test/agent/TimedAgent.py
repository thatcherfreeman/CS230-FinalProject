from datetime import datetime
from typing import Tuple, List

from agent.Action import Action
from agent.Agent import Agent
from game.GameState import GameState


class TimedAgent(Agent):
    """A decorator that prints the amount of time the agent took to make its decision to the console."""
    def __init__(self, delegate: Agent):
        super().__init__()
        self.__delegate = delegate

    def chooseActions(self, state: GameState) -> Tuple[List[Action], bool]:
        start = datetime.utcnow()
        actions = self.__delegate.chooseActions(state)
        finish = datetime.utcnow()
        delta = finish - start
        print("Choose actions took about " + str(delta.total_seconds()) + " seconds")
        return actions
