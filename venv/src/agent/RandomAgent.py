from random import Random
from typing import Tuple, List

from agent.Agent import Agent
from agent.Action import Action
from game.GameState import GameState

ACTIONS = [action for action in Action]


class RandomAgent(Agent):
    """This is an Agent that chooses actions at random. A potentially useful benchmark."""
    def __init__(self, seed: str = None):
        super().__init__()
        self.generator = Random()
        if seed is not None:
            self.generator.seed(seed, 2)

    def chooseActions(self, state: GameState) -> Tuple[List[Action], bool]:
        action = ACTIONS[self.generator.randint(0, len(ACTIONS) - 1)]
        return [action], False
