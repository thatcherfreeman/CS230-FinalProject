"""The methods in this file initialize several different useful game states for tests."""
from game.GameState import GameState, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT
from game.piece.standard import StandardPieceFactory
from game.piece.standard.StandardPiece import StandardPiece


def initClearTest():
    state = GameState()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    state.currentPiece = piece
    state.currentPieceLocation = (5, 2)

    for x in range(0, PLAYFIELD_WIDTH):
        for y in range(0, 4):
            state.overlay.set(x, y, True)
    return state


def initMovePieceTest():
    state = GameState()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    state.currentPiece = piece
    state.currentPieceLocation = (0, 3)
    return state


def initSimpleRotationTest():
    state = GameState()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    state.currentPiece = piece
    state.currentPieceLocation = (0, 2)
    return state


def initGameOverTest():
    state = GameState()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    state.currentPiece = piece
    state.currentPieceLocation = (5, 2)
    for y in range(0, PLAYFIELD_HEIGHT + 3):
        state.overlay.set(0, y, True)
    return state


def initStateWithSparseBoard():
    state = GameState()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    state.currentPiece = piece
    state.currentPieceLocation = (5, 10)
    return state


def initStateWithPossibleCollision():
    state = GameState()
    piece = StandardPieceFactory.getPiece(StandardPiece.I)
    piece.rotateCW()
    state.currentPiece = piece
    state.currentPieceLocation = (0, 2)
    return state


def initCornerState():
    state = GameState()
    piece = StandardPieceFactory.getPiece(StandardPiece.T)
    state.currentPiece = piece
    state.currentPieceLocation = (1, 1)
    for x in range(3, PLAYFIELD_WIDTH):
        for y in range(0, 5):
            state.overlay.set(x, y, True)
    return state
