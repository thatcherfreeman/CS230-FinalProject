from collections import deque
from typing import Tuple, List, Set, Deque

from agent.Action import Action
from agent.simulator.PathFindingDriver import PathFindingDriver
from agent.simulator.PiecePlacement import PiecePlacement
from game.Direction import Direction
from game.GameState import GameState, PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH

ACTIONS_TO_TRY = [Action.MOVE_DOWN, Action.MOVE_RIGHT, Action.MOVE_LEFT, Action.ROTATE_CCW, Action.ROTATE_CW]

# Automatically drop pieces until they are 2 higher than the highest occupied square on the board
QUICK_DROP_THRESHOLD = 2


# TODO: It might be unnecessarily slow to populate the list of action sequences when we know they won't be used
def findPlacements(state: GameState) -> Tuple[List[PiecePlacement], List[List[Action]]]:
    """Generates all possible placements of the current piece via DFS. Holding a piece is not considered here."""
    driver = PathFindingDriver(state)
    # An optimization that moves the piece down until the topmost occupied space is 2 spaces below it,
    # this can reduce the amount of time it takes to complete this search from about 120 ms to about 11 ms on an
    # empty board without losing correctness. I can't fathom why the agent would try to stack a tall tower of pieces,
    # so the slow case of simulating almost the entire board shouldn't happen often.
    pieceHeight = state.currentPieceLocation[1]
    quickDropRows = pieceHeight - (highestNonEmptyRow(state) + QUICK_DROP_THRESHOLD)
    if quickDropRows > 0:
        for i in range(0, quickDropRows):
            driver.movePiece(Direction.DOWN)
        driver.commit()
    placements = findPlacementsBFS(driver)
    actionSeqs = list()
    if quickDropRows > 0:
        for i in range(0, len(placements[1])):
            actionSeq = [Action.MOVE_DOWN] * quickDropRows
            actionSeq.extend(placements[1][i])
            actionSeqs.append(actionSeq)
        driver.revert()
    else:
        for i in range(0, len(placements[1])):
            actionSeq = list()
            actionSeq.extend(placements[1][i])
            actionSeqs.append(actionSeq)
    return placements[0], actionSeqs


def findPlacementsDFS(driver: PathFindingDriver, exploredPlacements: Set, actions: Deque[Action]) ->\
        Tuple[List[PiecePlacement], List[List[Action]]]:
    """Recursively search for piece placements with DFS. Return two lists: final piece placements and the
    corresponding sequences of actions that get there."""
    currentPlacement = placementFromState(driver.state)
    if currentPlacement in exploredPlacements:
        return None
    exploredPlacements.add(currentPlacement)
    recursiveResults = None
    isCurrentPlacementFinal = False
    for action in ACTIONS_TO_TRY:
        possible = action.func(driver)
        if not possible:
            if action == Action.MOVE_DOWN:
                isCurrentPlacementFinal = True
            continue
        driver.commit()
        actions.append(action)
        recursiveResult = findPlacementsDFS(driver, exploredPlacements, actions)
        if recursiveResult is not None:
            if recursiveResults is None:
                recursiveResults = list()
            recursiveResults.append(recursiveResult)
        actions.pop()
        driver.revert()

    # Merge results
    if not isCurrentPlacementFinal and recursiveResults is None:
        return None
    placementsFound = list()
    placementPaths = list()
    if isCurrentPlacementFinal:
        actionsCopy = list()
        actionsCopy.extend(actions)
        placementsFound.append(currentPlacement)
        placementPaths.append(actionsCopy)
    if recursiveResults is not None:
        for recursiveResult in recursiveResults:
            placementsFound.extend(recursiveResult[0])
            placementPaths.extend(recursiveResult[1])
    return placementsFound, placementPaths


def findPlacementsBFS(driver: PathFindingDriver):
    searchQueue = deque()
    placementDetails = dict()  # A dictionary that maps from PiecePlacement to (Action taken to get here, previous placement)
    finalPlacements = list()

    currentPlacement = placementFromState(driver.state)
    searchQueue.append(currentPlacement)
    placementDetails[currentPlacement] = None

    while len(searchQueue) > 0:
        currentPlacement = searchQueue.popleft()
        driver.setToPlacement(currentPlacement)
        driver.commit()
        for action in ACTIONS_TO_TRY:
            possible = action.func(driver)
            if not possible:
                if action == Action.MOVE_DOWN:
                    finalPlacements.append(currentPlacement)
                continue
            driver.commit()
            newPlacement = placementFromState(driver.state)
            if newPlacement not in placementDetails:
                placementDetails[newPlacement] = (action, currentPlacement)
                searchQueue.append(newPlacement)
            driver.revert()
        driver.revert()

    actionSequences = list()
    for placement in finalPlacements:
        actionSequence = deque()
        currentPlacement = placement
        while placementDetails[currentPlacement] is not None:
            details = placementDetails[currentPlacement]
            actionSequence.appendleft(details[0])
            currentPlacement = details[1]
        actionSequences.append(actionSequence)

    return finalPlacements, actionSequences


def placementFromState(state: GameState) -> PiecePlacement:
    placement = PiecePlacement()
    placement.location = state.currentPieceLocation
    placement.rotIdx = state.currentPiece.getRotIdx()
    return placement


def highestNonEmptyRow(state: GameState):
    for y in range(PLAYFIELD_HEIGHT - 1, -1, -1):
        for x in range(0, PLAYFIELD_WIDTH):
            if state.overlay.get(x, y):
                return y
    return 0
