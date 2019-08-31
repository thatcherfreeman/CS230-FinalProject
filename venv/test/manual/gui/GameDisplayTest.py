import threading
import time
import tkinter as tk
from gui.GameDisplay import GameDisplay
from piece.standard import StandardPieceFactory
from piece.standard.StandardColor import StandardColor
from piece.standard.StandardPiece import StandardPiece
from state.GameState import PIECE_QUEUE_LEN

PIECES = [StandardPieceFactory.getPiece(pieceDefinition) for pieceDefinition in StandardPiece]


def testDisplay(gameDisplay):
    i = 0
    holdPieceAvailable = True
    score = 0
    while True:
        time.sleep(1)
        gameDisplay.setPlayfieldCellColor(2, 15, StandardColor.RED)
        time.sleep(1)
        gameDisplay.setPlayfieldCellColor(2, 15, StandardColor.BLUE)
        gameDisplay.setHeldPiece(PIECES[i])
        i = (i + 1) % len(PIECES)
        setPieceQueue(gameDisplay, i)
        holdPieceAvailable = not holdPieceAvailable
        gameDisplay.setHoldAvailable(holdPieceAvailable)
        gameDisplay.setScoreText(str(score))
        score += 100


def setPieceQueue(gameDisplay, i):
    pieces = [PIECES[(j + i) % len(PIECES)] for j in range(0, PIECE_QUEUE_LEN)]
    gameDisplay.setQueuedPieces(pieces)


if __name__ == '__main__':
    root = tk.Tk()
    display = GameDisplay(root)
    gameThread = threading.Thread(target=testDisplay, args=(display, ))
    gameThread.start()
    root.mainloop()
    gameThread.join(0)

