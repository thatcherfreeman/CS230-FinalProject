import unittest

from agent.simulator.PathFindingDriver import PathFindingDriver
from game.Direction import Direction
from utils.GameStateUtils import initStateWithSparseBoard, initStateWithPossibleCollision


class PathFindingDriverTest(unittest.TestCase):

    def testRevertMoveDown(self):
        driver = PathFindingDriver(initStateWithSparseBoard())
        driver.movePiece(Direction.DOWN)
        driver.commit()
        driver.movePiece(Direction.DOWN)
        driver.commit()
        self.assertEqual((5, 8), driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual((5, 9), driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual((5, 10), driver.state.currentPieceLocation)

    def testRevertMoveLeftRight(self):
        driver = PathFindingDriver(initStateWithSparseBoard())
        driver.movePiece(Direction.LEFT)
        driver.commit()
        driver.movePiece(Direction.RIGHT)
        driver.commit()
        self.assertEqual((5, 10), driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual((4, 10), driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual((5, 10), driver.state.currentPieceLocation)

    def testRevertRotationWithoutWallKick(self):
        driver = PathFindingDriver(initStateWithSparseBoard())
        startingRotIdx = driver.state.currentPiece.getRotIdx()

        driver.rotatePiece(True)
        driver.commit()

        self.assertNotEqual(startingRotIdx, driver.state.currentPiece.getRotIdx())

        driver.revert()
        self.assertEqual(startingRotIdx, driver.state.currentPiece.getRotIdx())

    def testRevertRotationWithWallKick(self):
        driver = PathFindingDriver(initStateWithPossibleCollision())
        startingRotIdx = driver.state.currentPiece.getRotIdx()
        startingLocation = driver.state.currentPieceLocation

        driver.rotatePiece(True)
        driver.commit()

        self.assertNotEqual(startingRotIdx, driver.state.currentPiece.getRotIdx())
        self.assertNotEqual(startingLocation, driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual(startingRotIdx, driver.state.currentPiece.getRotIdx())
        self.assertEqual(startingLocation, driver.state.currentPieceLocation)


if __name__ == '__main__':
    unittest.main()
