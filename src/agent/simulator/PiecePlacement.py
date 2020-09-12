

class PiecePlacement:
    def __init__(self):
        self.location = None
        self.rotIdx = 0

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return other.location == self.location and other.rotIdx == self.rotIdx

    def __hash__(self):
        return hash((self.location, self.rotIdx))
