from game.GameState import GameState


class StateEvaluator:
    """This is an interface for a state evaluation function. The simulator will look at many possibilities and choose
    a sequence of actions that result in the state that was evaluated highest. It returns something that can be
    compared to other variables of the same type."""
    def evaluate(self, state: GameState, pointsDelta: int):
        raise NotImplementedError
