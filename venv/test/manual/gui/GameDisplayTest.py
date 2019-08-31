import threading
import time
import tkinter as tk
from gui.GameDisplay import GameDisplay
from piece.standard import StandardPieceFactory
from piece.standard.StandardPiece import StandardPiece


def blinkBox(gameDisplay):
    loopThroughPieces(gameDisplay)
    topLeftishTile = gameDisplay.playfieldDisplay.get(2, 15)
    while True:
        time.sleep(1)
        print("red")
        topLeftishTile.configure(bg="red")
        time.sleep(1)
        print("blue")
        topLeftishTile.configure(bg="blue")


def loopThroughPieces(gameDisplay):
    heldPieceWidget = gameDisplay.infoPanel.heldPieceWidget
    heldPieceWidget.setPiece(StandardPieceFactory.getPiece(StandardPiece.T))


if __name__ == '__main__':
    root = tk.Tk()
    display = GameDisplay(root)
    gameThread = threading.Thread(target=blinkBox, args=(display, ))
    gameThread.start()
    root.mainloop()
    gameThread.join(0)

