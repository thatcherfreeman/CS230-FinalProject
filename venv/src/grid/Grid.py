# Abstract base class for grid objects. It's expected that 'width' and 'height' instance variables exist.
class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def get(self, x: int, y: int):
        raise NotImplementedError

    def set(self, x: int, y: int, value):
        raise NotImplementedError
