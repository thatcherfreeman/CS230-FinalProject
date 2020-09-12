from enum import Enum


class Direction(Enum):
    """Represents how movement in this direction would change the x and y coordinates of a piece's center"""
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, -1)

    def __init__(self, deltaX: int, deltaY: int):
        self.deltaX = deltaX
        self.deltaY = deltaY
