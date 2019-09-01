from random import Random

from game.piece.standard import StandardPieceFactory
from game.piece.standard.StandardPiece import StandardPiece


def initPieceDefinitions():
    return [pieceDefinition for pieceDefinition in StandardPiece]


class PieceGenerator:
    """A reproducible-random piece generator that permutes all of the pieces, returns them, then repeats.
    This way it won't generate 3 of the same piece in a row, which can be unsolvable (infinite alternating S and Z
    pieces will eventually result in a game over regardless of what the player does). This is standard for Tetris."""
    def __init__(self, seed: str = None):
        self.generator = Random()
        if seed is not None:
            self.generator.seed(seed, 2)
        self.pieceSequence = initPieceDefinitions()
        self.seqIdx = 0
        self.initSequence()

    def initSequence(self):
        self.generator.shuffle(self.pieceSequence)

    def generatePiece(self):
        if self.seqIdx == len(self.pieceSequence):
            self.generator.shuffle(self.pieceSequence)
            self.seqIdx = 0
        piece = StandardPieceFactory.getPiece(self.pieceSequence[self.seqIdx])
        self.seqIdx += 1
        return piece
