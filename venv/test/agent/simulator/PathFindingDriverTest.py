import unittest

from agent.simulator.PathFindingDriver import PathFindingDriver
from game.Direction import Direction
from game.GameDriver import PIECE_SPAWN_X, PIECE_SPAWN_Y
from game.piece.standard import StandardPieceFactory
from game.piece.standard.StandardPiece import StandardPiece


def initDriverWithSparseBoard():
    driver = PathFindingDriver()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    driver.setCurrentPiece(piece)
    driver.setCurrentPieceLocation((5, 10))
    return driver


def initDriverWithPossibleCollision():
    driver = PathFindingDriver()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    driver.setCurrentPiece(piece)
    driver.setCurrentPieceLocation((0, 2))
    return driver


class PathFindingDriverTest(unittest.TestCase):

    def testRevertMoveDown(self):
        driver = initDriverWithSparseBoard()
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
        driver = initDriverWithSparseBoard()
        driver.movePiece(Direction.LEFT)
        driver.commit()
        driver.movePiece(Direction.RIGHT)
        driver.commit()
        self.assertEqual((5, 10), driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual((4, 10), driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual((5, 10), driver.state.currentPieceLocation)

    def testRevertMoveAndHold(self):
        driver = initDriverWithSparseBoard()
        Ipiece = driver.state.currentPiece
        Jpiece = StandardPieceFactory.getPiece(StandardPiece.J)
        driver.setNextPiece(Jpiece)
        driver.commit()

        driver.movePiece(Direction.LEFT)
        driver.commit()
        driver.holdPiece()
        driver.commit()
        self.assertEqual((PIECE_SPAWN_X, PIECE_SPAWN_Y), driver.state.currentPieceLocation)
        self.assertEqual(False, driver.state.holdAvailable)
        self.assertEqual(Jpiece, driver.state.currentPiece)
        self.assertEqual(Ipiece, driver.state.heldPiece)

        driver.revert()
        self.assertEqual((4, 10), driver.state.currentPieceLocation)
        self.assertEqual(True, driver.state.holdAvailable)
        self.assertEqual(Ipiece, driver.state.currentPiece)
        self.assertEqual(None, driver.state.heldPiece)

        driver.revert()
        self.assertEqual((5, 10), driver.state.currentPieceLocation)

    def testRevertSecondHoldOfGame(self):
        driver = initDriverWithSparseBoard()
        Ipiece = driver.state.currentPiece
        Jpiece = StandardPieceFactory.getPiece(StandardPiece.J)
        Spiece = StandardPieceFactory.getPiece(StandardPiece.S)
        driver.setHeldPiece(Ipiece)
        driver.setHoldAvailable(True)
        driver.setCurrentPiece(Jpiece)
        driver.setNextPiece(Spiece)
        driver.commit()

        driver.movePiece(Direction.DOWN)
        driver.commit()
        driver.holdPiece()
        driver.commit()

        self.assertEqual(Ipiece, driver.state.currentPiece)
        self.assertEqual(Jpiece, driver.state.heldPiece)
        self.assertEqual(False, driver.state.holdAvailable)
        self.assertEqual(Spiece, driver.nextPiece)
        self.assertEqual((PIECE_SPAWN_X, PIECE_SPAWN_Y), driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual(Jpiece, driver.state.currentPiece)
        self.assertEqual(Ipiece, driver.state.heldPiece)
        self.assertEqual(True, driver.state.holdAvailable)
        self.assertEqual(Spiece, driver.nextPiece)
        self.assertEqual((5, 9), driver.state.currentPieceLocation)

        driver.revert()
        self.assertEqual((5, 10), driver.state.currentPieceLocation)

    def testRevertRotationWithoutWallKick(self):
        driver = initDriverWithSparseBoard()
        startingRotIdx = driver.state.currentPiece.getRotIdx()

        driver.rotatePiece(True)
        driver.commit()

        self.assertNotEqual(startingRotIdx, driver.state.currentPiece.getRotIdx())

        driver.revert()
        self.assertEqual(startingRotIdx, driver.state.currentPiece.getRotIdx())

    def testRevertRotationWithWallKick(self):
        driver = initDriverWithPossibleCollision()
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
