from agent.Action import Action
from agent.Agent import Agent
from game.SinglePlayerGuiWrapper import SinglePlayerGuiWrapper

# Every n frames, the piece will be pulled down.
FRAMES_BETWEEN_GRAVITY = 5


class GravitySinglePlayerGuiWrapper(SinglePlayerGuiWrapper):
    """This game of Tetris features gravity that pulls the current piece downward every so often."""
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self.__gravityTicks = 0

    def resolveAction(self):
        if self.__gravityTicks == 0:
            action = Action.MOVE_DOWN
        else:
            action = super().resolveAction()
        self.__gravityTicks = (self.__gravityTicks + 1) % FRAMES_BETWEEN_GRAVITY
        return action
