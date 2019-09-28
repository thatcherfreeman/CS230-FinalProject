from agent.simulator.StateEvaluator import StateEvaluator
from game.GameState import GameState


class ScoreEvaluator(StateEvaluator):
    """This is a very simple evaluator that prefers making moves that result in the most points. It's pretty
    short-sighted."""
    def evaluate(self, state: GameState, pointsDelta: int):
        return pointsDelta

# Notes: With a depth of 3 queued pieces, the score evaluator can't see far enough into the future to get variation
# in how the states are evaluated. The observed behavior tends to be the shortest path since everything is tied.
