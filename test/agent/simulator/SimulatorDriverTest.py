import unittest

from collections import deque

from agent.simulator.PiecePlacement import PiecePlacement
from agent.simulator.SimulatorDriver import SimulatorDriver
from game import GameState
from game.GameDriver import PIECE_SPAWN_Y, PIECE_SPAWN_X, GameDriver, getClearPoints
from game.GameState import PLAYFIELD_WIDTH
from game.piece.standard import StandardPieceFactory
from game.piece.standard.StandardPiece import StandardPiece
from grid.Grid import Grid
from grid.ListGrid import ListGrid
from utils.GameStateUtils import initCornerState, initStateWithSparseBoard, initClearTest


def copyOverlay(state: GameState):
    overlayCopy = ListGrid(state.overlay.width, state.overlay.height, None)
    for x in range(0, state.overlay.width):
        for y in range(0, state.overlay.height):
            overlayCopy.set(x, y, state.overlay.get(x, y))
    return overlayCopy


def listOfQueuedPieces(driver: GameDriver):
    queuedPieces = list()
    for piece in driver.state.pieceQueue:
        queuedPieces.append(piece)
    return queuedPieces


class SimulatorDriverTest(unittest.TestCase):

    def testRevertSetToPlacement(self):
        driver = SimulatorDriver(initStateWithSparseBoard())
        originalLocation = driver.state.currentPieceLocation
        originalRotIdx = driver.state.currentPiece.getRotIdx()
        newPlacement = PiecePlacement()
        newPlacement.rotIdx = 2
        newPlacement.location = (3, 4)
        driver.setToPlacement(newPlacement)
        driver.commit()

        self.assertEqual(newPlacement.location, driver.state.currentPieceLocation)
        self.assertEqual(newPlacement.rotIdx, driver.state.currentPiece.getRotIdx())
        driver.revert()

        self.assertEqual(originalLocation, driver.state.currentPieceLocation)
        self.assertEqual(originalRotIdx, driver.state.currentPiece.getRotIdx())

    def testRevertPlacePiece(self):
        driver = SimulatorDriver(initCornerState())
        driver.setHoldAvailable(False)
        driver.placePiece()
        driver.commit()
        self.assertTrue(driver.state.holdAvailable)

        driver.revert()
        self.assertFalse(driver.state.holdAvailable)

    def testRevertFullClear(self):
        driver = SimulatorDriver(initClearTest())
        originalBoardOverlay = copyOverlay(driver.state)
        driver.checkAndClearLines()
        driver.commit()

        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(0, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(getClearPoints(4), driver.pointsDelta)

        driver.revert()
        self.assertEqual(0, driver.pointsDelta)
        self.assertBoardState(originalBoardOverlay, driver.state)

    def testRevertSingleDisjointClear(self):
        driver = SimulatorDriver(initClearTest())
        driver.state.overlay.set(0, 2, False)
        originalBoardOverlay = copyOverlay(driver.state)
        driver.checkAndClearLines()
        driver.commit()

        self.assertFalse(driver.state.overlay.get(0, 0))
        for x in range(1, PLAYFIELD_WIDTH):
            self.assertTrue(driver.state.overlay.get(x, 0))
        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(1, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(getClearPoints(1) + getClearPoints(2), driver.pointsDelta)

        driver.revert()
        self.assertEqual(0, driver.pointsDelta)
        self.assertBoardState(originalBoardOverlay, driver.state)

    def testRevertDoubleDisjointClear(self):
        driver = SimulatorDriver(initClearTest())
        driver.state.overlay.set(0, 3, False)
        driver.state.overlay.set(0, 1, False)
        originalBoardOverlay = copyOverlay(driver.state)
        driver.checkAndClearLines()
        driver.commit()

        self.assertFalse(driver.state.overlay.get(0, 0))
        self.assertFalse(driver.state.overlay.get(0, 1))
        for x in range(1, PLAYFIELD_WIDTH):
            for y in range(0, 2):
                self.assertTrue(driver.state.overlay.get(x, y))
        for x in range(0, PLAYFIELD_WIDTH):
            for y in range(2, 4):
                self.assertFalse(driver.state.overlay.get(x, y))
        self.assertEqual(2 * getClearPoints(1), driver.pointsDelta)

        driver.revert()
        self.assertEqual(0, driver.pointsDelta)
        self.assertBoardState(originalBoardOverlay, driver.state)

    def testRevertFirstHoldOfGame(self):
        driver = SimulatorDriver(initStateWithSparseBoard())
        driver.state.pieceQueue = deque()  # Initialize empty piece queue to avoid NPE
        Ipiece = driver.state.currentPiece
        Jpiece = StandardPieceFactory.getPiece(StandardPiece.J)
        driver.setNextPiece(Jpiece)
        driver.commit()

        driver.holdPiece()
        driver.commit()
        self.assertEqual((PIECE_SPAWN_X, PIECE_SPAWN_Y), driver.state.currentPieceLocation)
        self.assertEqual(False, driver.state.holdAvailable)
        self.assertEqual(Jpiece, driver.state.currentPiece)
        self.assertEqual(Ipiece, driver.state.heldPiece)

        driver.revert()
        self.assertEqual((5, 10), driver.state.currentPieceLocation)
        self.assertEqual(True, driver.state.holdAvailable)
        self.assertEqual(Ipiece, driver.state.currentPiece)
        self.assertEqual(None, driver.state.heldPiece)

    def testRevertSecondHoldOfGame(self):
        driver = SimulatorDriver(initStateWithSparseBoard())
        driver.state.pieceQueue = deque()  # Initialize empty piece queue to avoid NPE
        Ipiece = driver.state.currentPiece
        Jpiece = StandardPieceFactory.getPiece(StandardPiece.J)
        Spiece = StandardPieceFactory.getPiece(StandardPiece.S)
        driver.setHeldPiece(Ipiece)
        driver.setHoldAvailable(True)
        driver.setCurrentPiece(Jpiece)
        driver.setNextPiece(Spiece)
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
        self.assertEqual((5, 10), driver.state.currentPieceLocation)

    def testRevertGenerateNewPieceFromQueue(self):
        driver = SimulatorDriver(initCornerState())
        driver.initPieceQueue()
        originalQueuedPieces = listOfQueuedPieces(driver)
        originalPiece = driver.state.currentPiece
        originalLocation = driver.state.currentPieceLocation
        driver.generateNewPiece()
        driver.commit()
        self.assertNotEqual(originalPiece, driver.state.currentPiece)
        self.assertEqual((PIECE_SPAWN_X, PIECE_SPAWN_Y), driver.state.currentPieceLocation)
        self.assertNotEqual(originalQueuedPieces, listOfQueuedPieces(driver))

        driver.revert()
        self.assertEqual(originalPiece, driver.state.currentPiece)
        self.assertEqual(originalLocation, driver.state.currentPieceLocation)
        self.assertEqual(originalQueuedPieces, listOfQueuedPieces(driver))

    def testRevertGenerateNewPieceFromNextPiece(self):
        driver = SimulatorDriver(initCornerState())
        originalPiece = driver.state.currentPiece
        originalLocation = driver.state.currentPieceLocation
        Opiece = StandardPieceFactory.getPiece(StandardPiece.O)
        driver.state.pieceQueue = deque()  # initialize empty piece queue to avoid NPE
        driver.setNextPiece(Opiece)
        driver.commit()
        driver.generateNewPiece()
        driver.commit()
        self.assertEqual(Opiece, driver.state.currentPiece)
        self.assertEqual((PIECE_SPAWN_X, PIECE_SPAWN_Y), driver.state.currentPieceLocation)
        self.assertIsNone(driver.nextPiece)

        driver.revert()
        self.assertEqual(originalPiece, driver.state.currentPiece)
        self.assertEqual(originalLocation, driver.state.currentPieceLocation)
        self.assertEqual(Opiece, driver.nextPiece)

        driver.revert()
        self.assertIsNone(driver.nextPiece)

    def testNextPieceIgnoredIfPieceQueueNotEmpty(self):
        driver = SimulatorDriver(initCornerState())
        driver.state.pieceQueue = deque()
        Tpiece = driver.state.currentPiece
        Zpiece = StandardPieceFactory.getPiece(StandardPiece.Z)
        Spiece = StandardPieceFactory.getPiece(StandardPiece.S)
        driver.state.pieceQueue.append(Zpiece)
        driver.setNextPiece(Spiece)
        driver.commit()
        driver.generateNewPiece()
        driver.commit()

        self.assertEqual(Zpiece, driver.state.currentPiece)
        self.assertEqual(0, len(driver.state.pieceQueue))
        self.assertEqual(Spiece, driver.nextPiece)

        driver.revert()
        self.assertEqual(Tpiece, driver.state.currentPiece)
        self.assertEqual(1, len(driver.state.pieceQueue))
        self.assertEqual(Spiece, driver.nextPiece)

        driver.revert()
        self.assertIsNone(driver.nextPiece)

    def assertBoardState(self, expectedOverlay: Grid, state: GameState):
        for x in range(0, state.overlay.width):
            for y in range(0, state.overlay.height):
                self.assertEqual(expectedOverlay.get(x, y), state.overlay.get(x, y))


if __name__ == '__main__':
    unittest.main()
