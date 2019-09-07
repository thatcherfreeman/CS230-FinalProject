from typing import Dict, List

from agent.Action import Action
from agent.Agent import Agent
from agent.simulator.PiecePlacement import PiecePlacement
from game.GameState import GameState


class SimulatorAgent(Agent):
    def __init__(self):
        super().__init__()

    # TODO: make class 'SimulatorDriver/ReversibleDriver' which allows reversibility of action invocations (maybe by returning a lambda for each action that would reverse that action)

    def getPlacements(self, state: GameState) -> Dict[PiecePlacement, List[Action]]:
        # TODO: start with a game state, DFS through options, assemble a list of possible placements and paths (sequences of actions) for how to get there.
        pass
