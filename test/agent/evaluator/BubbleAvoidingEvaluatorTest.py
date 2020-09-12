import unittest

from agent.evaluator.intuitive.BubbleAvoidingEvaluator import BubbleAvoidingEvaluator
from game.GameState import GameState, PLAYFIELD_WIDTH


def dividedState():
    state = GameState()
    for x in range(0, PLAYFIELD_WIDTH):
        state.overlay.set(x, 5, True)
    return state


class BubbleAvoidingEvaluatorTest(unittest.TestCase):
    def testSingleLargeBubble(self):
        state = dividedState()
        evaluator = BubbleAvoidingEvaluator()
        self.assertEqual(-55, evaluator.evaluate(state, 0))


if __name__ == '__main__':
    unittest.main()
