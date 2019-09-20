import unittest

from agent.simulator import SimulationUtils
from game.GameState import GameState, PLAYFIELD_WIDTH
from game.piece.standard import StandardPieceFactory
from game.piece.standard.StandardPiece import StandardPiece


def initCornerState():
    state = GameState()
    piece = StandardPieceFactory.getPiece(StandardPiece.T)
    state.currentPiece = piece
    state.currentPieceLocation = (1, 1)
    for x in range(3, PLAYFIELD_WIDTH):
        for y in range(0, 5):
            state.overlay.set(x, y, True)
    return state


class SimulationUtilsTest(unittest.TestCase):
    def testFindPlacements(self):
        state = initCornerState()
        prevLocation = state.currentPieceLocation
        prevRotIdx = state.currentPiece.getRotIdx()
        results = SimulationUtils.findPlacements(state)
        self.assertEqual(prevLocation, state.currentPieceLocation)
        self.assertEqual(prevRotIdx, state.currentPiece.getRotIdx())
        self.assertEqual(len(results[0]), len(results[1]))
        self.assertEqual(6, len(results[0]))


if __name__ == '__main__':
    unittest.main()
