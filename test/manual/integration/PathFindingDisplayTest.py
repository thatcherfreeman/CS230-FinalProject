import threading
import time
import tkinter as tk
from datetime import datetime

from agent.simulator import SimulationUtils
from game.GameState import PLAYFIELD_WIDTH
from game.piece.standard import StandardPieceFactory
from game.piece.standard.StandardColor import StandardColor
from game.piece.standard.StandardPiece import StandardPiece
from gui.DisplayDriver import DisplayDriver
from gui.GameDisplay import GameDisplay


def testDisplay(displayDriver):
    Zpiece = StandardPieceFactory.getPiece(StandardPiece.Z)
    displayDriver.setCurrentPiece(Zpiece)
    fillRows(displayDriver, 5)
    start = datetime.utcnow()
    placementsAndPaths = SimulationUtils.findPlacements(displayDriver.state)
    delta = datetime.utcnow() - start
    print("Find placements took about " + str(round(delta.microseconds/1000)) + " ms")
    time.sleep(1)
    while True:
        for path in placementsAndPaths[1]:
            displayPath(displayDriver, path)
        print("Reached end of found paths. Looping...")


def displayPath(displayDriver: DisplayDriver, path):
    initialPlacement = SimulationUtils.placementFromState(displayDriver.state)
    for action in path:
        time.sleep(0.5)
        action.func(displayDriver)
    print("Final placement reached")
    time.sleep(2)
    displayDriver.setCurrentPieceLocation(initialPlacement.location)
    rotIdx = displayDriver.state.currentPiece.getRotIdx()
    while rotIdx != initialPlacement.rotIdx:
        displayDriver.rotatePiece(True)
        rotIdx = displayDriver.state.currentPiece.getRotIdx()
    print("Piece reset")
    time.sleep(1)


def fillRows(displayDriver: DisplayDriver, numRows: int):
    for x in range(0, PLAYFIELD_WIDTH):
        for y in range(0, numRows):
            displayDriver.state.overlay.set(x, y, True)
            displayDriver.setPlayfieldCellColor(x, y, StandardColor.CYAN)


if __name__ == '__main__':
    root = tk.Tk()
    driver = DisplayDriver(GameDisplay(root))
    gameThread = threading.Thread(target=testDisplay, args=(driver, ))
    gameThread.start()
    root.mainloop()
    gameThread.join(0)
