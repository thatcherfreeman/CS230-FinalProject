import tkinter as tk
from gui.GameDisplay import GameDisplay

if __name__ == '__main__':
    root = tk.Tk()
    display = GameDisplay(root)
    root.mainloop()
