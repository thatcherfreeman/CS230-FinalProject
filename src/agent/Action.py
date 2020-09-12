from enum import Enum

from game.Direction import Direction


class FunctionHolder:
    """Python won't let me make enums that hold functions without other member variables, so this is a workaround"""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Action(Enum):
    # TODO: Add hard drop?
    MOVE_LEFT = FunctionHolder(lambda driver: driver.movePiece(Direction.LEFT))
    MOVE_RIGHT = FunctionHolder(lambda driver: driver.movePiece(Direction.RIGHT))
    MOVE_DOWN = FunctionHolder(lambda driver: driver.movePiece(Direction.DOWN))
    ROTATE_CW = FunctionHolder(lambda driver: driver.rotatePiece(True))
    ROTATE_CCW = FunctionHolder(lambda driver: driver.rotatePiece(False))
    HOLD = FunctionHolder(lambda driver: driver.holdPiece())

    def __init__(self, func):
        self.func = func
