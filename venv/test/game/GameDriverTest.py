import unittest

from game.Direction import Direction
from game.GameDriver import GameDriver, getClearPoints
from game.GameState import PLAYFIELD_WIDTH
from utils.GameStateUtils import initClearTest, initMovePieceTest, initSimpleRotationTest, initGameOverTest


class GameDriverTest(unittest.TestCase):
    def testFullClear(self):
        driver = GameDriver(initClearTest())
        points = driver.checkAndClearLines()[0]

        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(0, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(getClearPoints(4), points)

    def testSingleDisjointClear(self):
        driver = GameDriver(initClearTest())
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
        driver = GameDriver(initClearTest())
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
        driver = GameDriver(initGameOverTest())
        gameOver = driver.checkAndClearLines()[1]
        self.assertTrue(gameOver)

    def testGameOverWithClear(self):
        driver = GameDriver(initGameOverTest())
        for x in range(1, PLAYFIELD_WIDTH):
            for y in range(0, 4):
                driver.state.overlay.set(x, y, True)
        gameOver = driver.checkAndClearLines()[1]
        self.assertFalse(gameOver)

    def testMovePieceVerticallyWhenUnobstructed(self):
        driver = GameDriver(initMovePieceTest())
        legal = driver.movePiece(Direction.DOWN)
        location = driver.state.currentPieceLocation
        self.assertEqual((0, 2), location)
        self.assertTrue(legal)

    def testMovePieceLaterallyWhenUnobstructed(self):
        driver = GameDriver(initMovePieceTest())
        legal = driver.movePiece(Direction.RIGHT)
        location = driver.state.currentPieceLocation
        self.assertEqual((1, 3), location)
        self.assertTrue(legal)

    def testMovePieceLaterallyWhenObstructed(self):
        driver = GameDriver(initMovePieceTest())
        legal = driver.movePiece(Direction.LEFT)
        location = driver.state.currentPieceLocation
        self.assertEqual((0, 3), location)
        self.assertFalse(legal)

    def testIllegalRotation(self):
        driver = GameDriver(initSimpleRotationTest())
        # Obstruct the rotation
        for y in range(0, 4):
            driver.state.overlay.set(1, y, True)
        legal = driver.rotatePiece(True)
        driver.placePiece()
        self.assertFalse(legal)
        for y in range(0, 4):
            self.assertTrue(driver.state.overlay.get(0, y))

    def testRotationWithWallKick(self):
        driver = GameDriver(initSimpleRotationTest())
        legal = driver.rotatePiece(True)
        driver.placePiece()
        self.assertTrue(legal)
        for x in range(0, 4):
            self.assertTrue(driver.state.overlay.get(x, 1))


if __name__ == '__main__':
    unittest.main()
