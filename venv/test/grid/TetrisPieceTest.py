import unittest
from src.grid.ListGrid import ListGrid
from src.grid.OffsetOverlay import OffsetOverlay
from src.TetrisPiece import TetrisPiece

# The T piece this method returns is facing up
def initTPiece():
    grid = ListGrid(5, 5, False)
    grid.set(1, 2, True)
    grid.set(2, 2, True)
    grid.set(3, 2, True)
    grid.set(2, 1, True)
    return TetrisPiece(grid)

def countOccupiedSpaces(piece: TetrisPiece):
    occupiedSpaces = 0
    for x in range(-2, 2):
        for y in range(-2, 2):
            occupiedSpaces += 1 if piece.overlay.get(x, y) else 0
    return occupiedSpaces

class TetrisPieceTest(unittest.TestCase):
    def test_rotate_ccw(self):
        tPiece = initTPiece()
        tPiece.rotateCCW()
        self.assertTrue(tPiece.overlay.get(0,0))
        self.assertTrue(tPiece.overlay.get(0, -1))
        self.assertTrue(tPiece.overlay.get(0, 1))
        self.assertTrue(tPiece.overlay.get(1, 0))
        self.assertEqual(4, countOccupiedSpaces(tPiece))

    def test_rotate_cw(self):
        tPiece = initTPiece()
        tPiece.rotateCW()
        self.assertTrue(tPiece.overlay.get(0, 0))
        self.assertTrue(tPiece.overlay.get(0, -1))
        self.assertTrue(tPiece.overlay.get(0, 1))
        self.assertTrue(tPiece.overlay.get(-1, 0))
        self.assertEqual(4, countOccupiedSpaces(tPiece))



if __name__ == '__main__':
    unittest.main()
