from src.grid.Grid import Grid
from src.grid.OffsetOverlay import OffsetOverlay

# TODO: Use flyweight pattern for grid rotation to save processing time?
# A class representing the orientation and content of a tetris piece. It has a 5x5 grid as its underlying storage.


class CustomTetrisPiece:
    def __init__(self, grid: Grid):
        if grid.height != 5 or grid.width != 5:
            raise Exception("Only 5x5 piece overlays are supported right now")
        self.overlay: OffsetOverlay = OffsetOverlay(grid, -2, -2)

    def rotateCW(self):
        for i in range(0, 3):
            for j in range(1, 3):
                topRight = self.overlay.get(i, j)
                topLeft = self.overlay.get(-1 * j, i)
                bottomLeft = self.overlay.get(-1 * i, -1 * j)
                bottomRight = self.overlay.get(j, -1 * i)
                self.overlay.set(-1 * j, i, bottomLeft)
                self.overlay.set(-1 * i, -1 * j, bottomRight)
                self.overlay.set(j, -1 * i, topRight)
                self.overlay.set(i, j, topLeft)

    def rotateCCW(self):
        for i in range(0, 3):
            for j in range(1, 3):
                topRight = self.overlay.get(i, j)
                topLeft = self.overlay.get(-1 * j, i)
                bottomLeft = self.overlay.get(-1 * i, -1 * j)
                bottomRight = self.overlay.get(j, -1 * i)
                self.overlay.set(-1 * j, i, topRight)
                self.overlay.set(-1 * i, -1 * j, topLeft)
                self.overlay.set(j, -1 * i, bottomLeft)
                self.overlay.set(i, j, bottomRight)
