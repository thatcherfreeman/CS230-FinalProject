# Abstract base class for grid objects. It's expected that 'width' and 'height' instance variables exist.
class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def get(self, x: int, y: int):
        raise NotImplementedError

    def set(self, x: int, y: int, value):
        raise NotImplementedError

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if other.height != self.height or other.width != self.width:
            return False
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.get(x, y) != other.get(x, y):
                    return False
        return True
