import unittest

from game.Direction import Direction
from game.GameDriver import GameDriver, CLEAR_POINTS, getClearPoints
from game.GameState import PLAYFIELD_WIDTH
from game.piece.standard import StandardPieceFactory
from game.piece.standard.StandardPiece import StandardPiece


def initClearTest():
    driver = GameDriver()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    driver.setCurrentPiece(piece)
    driver.setCurrentPieceLocation((5, 2))

    for x in range(0, PLAYFIELD_WIDTH):
        for y in range(0, 4):
            driver.state.overlay.set(x, y, True)
    return driver


def initMovePieceTest():
    driver = GameDriver()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    driver.setCurrentPiece(piece)
    driver.setCurrentPieceLocation((0, 3))
    return driver


class MyTestCase(unittest.TestCase):
    def testFullClear(self):
        driver = initClearTest()
        points = driver.checkAndClearLines()

        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(0, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(getClearPoints(4), points)

    def testSingleDisjointClear(self):
        driver = initClearTest()
        driver.state.overlay.set(0, 2, False)
        points = driver.checkAndClearLines()

        self.assertFalse(driver.state.overlay.get(0, 0))
        for x in range(1, PLAYFIELD_WIDTH):
            self.assertTrue(driver.state.overlay.get(x, 0))
        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(1, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(getClearPoints(1) + getClearPoints(2), points)

    def testDoubleDisjointClear(self):
        driver = initClearTest()
        driver.state.overlay.set(0, 3, False)
        driver.state.overlay.set(0, 1, False)
        points = driver.checkAndClearLines()

        self.assertFalse(driver.state.overlay.get(0, 0))
        self.assertFalse(driver.state.overlay.get(0, 1))
        for x in range(1, PLAYFIELD_WIDTH):
            for y in range(0, 2):
                self.assertTrue(driver.state.overlay.get(x, y))
        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(2, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(2 * getClearPoints(1), points)

    def testMovePieceWhenUnobstructedAndFinalizesPlacement(self):
        driver = initMovePieceTest()
        placed = driver.movePiece(Direction.DOWN)
        location = driver.state.currentPieceLocation
        self.assertEqual((0, 2), location)
        self.assertTrue(placed)

    def testMovePieceLaterallyWhenUnobstructed(self):
        driver = initMovePieceTest()
        placed = driver.movePiece(Direction.RIGHT)
        location = driver.state.currentPieceLocation
        self.assertEqual((1, 3), location)
        self.assertFalse(placed)

    def testMovePieceLaterallyWhenObstructed(self):
        driver = initMovePieceTest()
        placed = driver.movePiece(Direction.LEFT)
        location = driver.state.currentPieceLocation
        self.assertEqual((0, 3), location)
        self.assertFalse(placed)

if __name__ == '__main__':
    unittest.main()
