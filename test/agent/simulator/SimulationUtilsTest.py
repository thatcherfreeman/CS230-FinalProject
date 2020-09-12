import unittest

from agent.simulator import SimulationUtils
from utils.GameStateUtils import initCornerState


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
