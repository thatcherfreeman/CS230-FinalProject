import copy
import threading
import time
import tkinter as tk
from collections import deque
from datetime import datetime, timedelta

from agent.Action import Action
from agent.Agent import Agent
from gui.DisplayDriver import DisplayDriver
from gui.GameDisplay import GameDisplay

FRAMES_PER_SECOND = 4
SECONDS_PER_FRAME = 1/FRAMES_PER_SECOND


def sleepUntilEndOfFrame(startTime):
    now = datetime.utcnow()
    delta = startTime - now + timedelta(seconds=SECONDS_PER_FRAME)
    seconds = delta.total_seconds()
    if seconds > 0:
        time.sleep(seconds)

# TODO: This should be refactored but it's a lower priority than getting a reasonably impressive agent working
class SinglePlayerGuiWrapper:
    """Call 'run()' to start a GUI-based game of tetris with the specified agent!"""
    def __init__(self, agent: Agent):
        self.agent = agent
        self.display = None
        self.driver = None
        self.actions = deque()
        self.userKilledGame = False

    def run(self):
        root = tk.Tk()
        self.display = GameDisplay(root)
        self.driver = DisplayDriver(self.display)
        gameThread = threading.Thread(target=self.gameLoop)
        gameThread.start()
        root.mainloop()
        self.userKilledGame = True
        gameThread.join()

    def resolveAction(self):
        return self.actions.popleft()

    def gameLoop(self):
        gameOver = False
        finalize = False
        done = False
        while not (gameOver or self.userKilledGame):
            startTime = datetime.utcnow()
            if finalize:
                finalize = False
                done = False
                self.driver.placePiece()
                gameOver = self.driver.checkAndClearLines()[1]
                self.driver.generateNewPiece()
                self.actions.clear()
                sleepUntilEndOfFrame(startTime)
                continue
            if len(self.actions) == 0 and not done:
                newActions, done = self.agent.chooseActions(self.driver.state)
                for seqAction in newActions:
                    self.actions.append(seqAction)
                continue
            elif len(self.actions) == 0:
                action = Action.MOVE_DOWN
            else:
                action = self.resolveAction()
            legalAction = action.func(self.driver)
            if not legalAction and action is Action.MOVE_DOWN:
                finalize = True
            sleepUntilEndOfFrame(startTime)
