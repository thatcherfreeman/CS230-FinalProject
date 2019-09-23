from typing import Dict, List, Tuple

from agent.Action import Action
from agent.Agent import Agent
from agent.simulator import SimulationUtils
from agent.simulator.PiecePlacement import PiecePlacement
from agent.simulator.SimulatorDriver import SimulatorDriver
from agent.simulator.StateEvaluator import StateEvaluator
from game.GameState import GameState


class SimulatorAgent(Agent):
    def __init__(self, evaluator: StateEvaluator):
        super().__init__()
        self.__evaluator = evaluator

    def chooseActions(self, state: GameState) -> Tuple[List[Action], bool]:
        # First, enumerate all of the placements and initialize the driver
        placements, actionSequences = SimulationUtils.findPlacements(state)
        simulatorDriver = SimulatorDriver(state)

        # Next, evaluate each placement and keep the maximum
        bestPlacementValue, bestPlacementIdx = self.findBestPlacement(simulatorDriver, placements)

        # If we can hold the piece, evaluate that too
        if simulatorDriver.state.holdAvailable:
            holdPlacementValue = self.evaluateHoldPiece(simulatorDriver)
            if holdPlacementValue > bestPlacementValue:
                return [Action.HOLD], True

        return actionSequences[bestPlacementIdx], True

    def findBestPlacement(self, driver: SimulatorDriver, placements: List[PiecePlacement]) -> Tuple:
        bestPlacementIdx = 0
        bestPlacementValue = self.evaluatePlacement(driver, placements[0])
        for i in range(1, len(placements)):
            currentPlacementValue = self.evaluatePlacement(driver, placements[i])
            if currentPlacementValue > bestPlacementValue:
                bestPlacementIdx = i
                bestPlacementValue = currentPlacementValue
        return bestPlacementValue, bestPlacementIdx

    def evaluatePlacement(self, driver: SimulatorDriver, placement: PiecePlacement):
        driver.setToPlacement(placement)
        driver.placePiece()
        driver.checkAndClearLines()
        driver.generateNewPiece()
        driver.commit()

        # Check for the base case, here it's 'piece queue is empty'
        if len(driver.state.pieceQueue) == 0:
            placementValue = self.__evaluator.evaluate(driver.state, driver.pointsDelta)
            driver.revert()
            return placementValue

        # Compare all possible piece placements to find the best one
        placements = SimulationUtils.findPlacements(driver.state)[0]
        bestPlacementValue = self.findBestPlacement(driver, placements)[1]

        # Consider holding the current piece if it's a possibility
        if driver.state.holdAvailable:
            bestPlacementValue = max(self.evaluateHoldPiece(driver), bestPlacementValue)
        driver.revert()
        return bestPlacementValue

    def evaluateHoldPiece(self, driver: SimulatorDriver):
        driver.holdPiece()
        driver.commit()
        placements = SimulationUtils.findPlacements(driver.state)[0]
        bestPlacementValue = self.findBestPlacement(driver, placements)[0]
        driver.revert()
        return bestPlacementValue
