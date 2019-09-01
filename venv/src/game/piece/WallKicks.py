from typing import Tuple, List


class WallKicks:
    """When a tetris piece is rotated, it may collide with the board. A sequence of deltaX, deltaY translation pairs
    are applied to the piece. If a translation is successful, that becomes the final state of the piece. If a
    translation fails, the next translation is attempted. If the end of the list is reached, the rotation is discarded
    (it is an illegal rotation). See tetris.wiki/SRS for a more detailed explanation."""
    def __init__(self, cwKicks: List[Tuple[int, int]], ccwKicks: List[Tuple[int, int]]):
        self.cwKicks = cwKicks
        self.ccwKicks = ccwKicks
