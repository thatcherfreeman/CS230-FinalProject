from agent.simulator import SimulationUtils
from agent.simulator.StateEvaluator import StateEvaluator
from game.GameState import GameState, PLAYFIELD_WIDTH, BUFFER_HEIGHT, PLAYFIELD_HEIGHT
from disjoint_set import DisjointSet


class BubbleAvoidingEvaluator(StateEvaluator):
    """This is an evaluator that simply penalizes fully-surrounded bubbles of empty space on the board"""
    def evaluate(self, state: GameState, pointsDelta: int):
        height = SimulationUtils.highestNonEmptyRow(state)
        heightPenalty = 0
        if height > 4:
            heightPenalty = -1*15*(height - 4)

        return self.bubblePenaltySum(state, height + 1) + pointsDelta/2 + heightPenalty

    def bubblePenalty(self, bubbleSize: int):
        return -5 - bubbleSize

    def bubblePenaltySum(self, state: GameState, ceiling: int):
        overlay = state.overlay
        disjointBubbles = DisjointSet()

        # This row of squares can never contain bubbles since pieces can't get up here
        masterLocation = (0, ceiling)
        for x in range(1, PLAYFIELD_WIDTH):
            location = (x, PLAYFIELD_HEIGHT + BUFFER_HEIGHT - 1)
            disjointBubbles.union(location, masterLocation)

        for y in range(ceiling - 1, -1, -1):
            for x in range(0, PLAYFIELD_WIDTH):
                if overlay.get(x, y):
                    # This square is occupied
                    continue
                disjointBubbles.find((x, y))
                if not overlay.get(x, y + 1):
                    disjointBubbles.union((x, y + 1), (x, y))
                if y > 0 and not overlay.get(x, y - 1):
                    disjointBubbles.union((x, y - 1), (x, y))
                if x > 0 and not overlay.get(x - 1, y):
                    disjointBubbles.union((x - 1, y), (x, y))
                if x < (PLAYFIELD_WIDTH - 1) and not overlay.get(x + 1, y):
                    disjointBubbles.union((x + 1, y), (x, y))

        bubblePenalty = 0
        for bubble in disjointBubbles.itersets():
            if masterLocation in bubble:
                continue
            bubblePenalty += self.bubblePenalty(len(bubble))

        return bubblePenalty
