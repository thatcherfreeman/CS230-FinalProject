import unittest

from game.Direction import Direction
from game.GameDriver import GameDriver, CLEAR_POINTS, getClearPoints
from game.GameState import PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT
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


def initSimpleRotationTest():
    driver = GameDriver()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    driver.setCurrentPiece(piece)
    driver.setCurrentPieceLocation((0, 2))
    return driver


def initGameOverTest():
    driver = GameDriver()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    driver.setCurrentPiece(piece)
    driver.setCurrentPieceLocation((5, 2))
    for y in range(0, PLAYFIELD_HEIGHT + 3):
        driver.state.overlay.set(0, y, True)
    return driver


class GameDriverTest(unittest.TestCase):
    def testFullClear(self):
        driver = initClearTest()
        points = driver.checkAndClearLines()[0]

        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(0, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(getClearPoints(4), points)

    def testSingleDisjointClear(self):
        driver = initClearTest()
        driver.state.overlay.set(0, 2, False)
        points = driver.checkAndClearLines()[0]

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
        points = driver.checkAndClearLines()[0]

        self.assertFalse(driver.state.overlay.get(0, 0))
        self.assertFalse(driver.state.overlay.get(0, 1))
        for x in range(1, PLAYFIELD_WIDTH):
            for y in range(0, 2):
                self.assertTrue(driver.state.overlay.get(x, y))
        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(2, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(2 * getClearPoints(1), points)

    def testGameOver(self):
        driver = initGameOverTest()
        gameOver = driver.checkAndClearLines()[1]
        self.assertTrue(gameOver)

    def testGameOverWithClear(self):
        driver = initGameOverTest()
        for x in range(1, PLAYFIELD_WIDTH):
            for y in range(0, 4):
                driver.state.overlay.set(x, y, True)
        gameOver = driver.checkAndClearLines()[1]
        self.assertFalse(gameOver)

    def testMovePieceVerticallyWhenUnobstructed(self):
        driver = initMovePieceTest()
        legal = driver.movePiece(Direction.DOWN)
        location = driver.state.currentPieceLocation
        self.assertEqual((0, 2), location)
        self.assertTrue(legal)

    def testMovePieceLaterallyWhenUnobstructed(self):
        driver = initMovePieceTest()
        legal = driver.movePiece(Direction.RIGHT)
        location = driver.state.currentPieceLocation
        self.assertEqual((1, 3), location)
        self.assertTrue(legal)

    def testMovePieceLaterallyWhenObstructed(self):
        driver = initMovePieceTest()
        legal = driver.movePiece(Direction.LEFT)
        location = driver.state.currentPieceLocation
        self.assertEqual((0, 3), location)
        self.assertFalse(legal)

    def testIllegalRotation(self):
        driver = initSimpleRotationTest()
        # Obstruct the rotation
        for y in range(0, 4):
            driver.state.overlay.set(1, y, True)
        legal = driver.rotatePiece(True)
        driver.placePiece()
        self.assertFalse(legal)
        for y in range(0, 4):
            self.assertTrue(driver.state.overlay.get(0, y))

    def testRotationWithWallKick(self):
        driver = initSimpleRotationTest()
        legal = driver.rotatePiece(True)
        driver.placePiece()
        self.assertTrue(legal)
        for x in range(0, 4):
            self.assertTrue(driver.state.overlay.get(x, 1))


if __name__ == '__main__':
    unittest.main()
