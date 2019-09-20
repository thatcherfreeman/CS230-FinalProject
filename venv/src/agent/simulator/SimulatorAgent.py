from typing import Dict, List, Tuple

from agent.Action import Action
from agent.Agent import Agent
from agent.simulator.PiecePlacement import PiecePlacement
from game.GameState import GameState


class SimulatorAgent(Agent):
    def __init__(self):
        super().__init__()

    def chooseActions(self, state: GameState) -> Tuple[List[Action], bool]:
        # TODO: Implement this
        raise NotImplementedError
