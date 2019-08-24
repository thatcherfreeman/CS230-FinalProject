import unittest
from src.grid.ListGrid import ListGrid
from src.grid.OffsetOverlay import OffsetOverlay

def initGrid():
    return ListGrid(5, 5, False)

class OffsetOverlayTest(unittest.TestCase):

    def test_offset(self):
        grid = initGrid()
        grid.set(0, 2, True)
        offsetOverlay = OffsetOverlay(grid, -2, -2)
        self.assertEqual(True, offsetOverlay.get(-2, 0))
        self.assertEqual(False, offsetOverlay.get(0, 2))

    def test_bounds(self):
        grid = initGrid()
        offsetOverlay = OffsetOverlay(grid, -2, -2)
        tooLow = lambda: offsetOverlay.get(0, -3)
        tooHigh = lambda: offsetOverlay.get(0, 4)
        tooFarLeft = lambda: offsetOverlay.get(-3, 0)
        tooFarRight = lambda: offsetOverlay.get(4, 0)
        self.assertRaises(Exception, tooLow)
        self.assertRaises(Exception, tooHigh)
        self.assertRaises(Exception, tooFarLeft)
        self.assertRaises(Exception, tooFarRight)


if __name__ == '__main__':
    unittest.main()
