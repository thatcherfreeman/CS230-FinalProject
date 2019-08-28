import tkinter as tk

# This file is mostly just to help me remember stuff for later
# massive thanks to https://www.python-course.eu/tkinter_labels.php for the ramp-up into tkinter
if __name__ == '__main__':
    root = tk.Tk()
    title = tk.Label(root, text="Danny's Tetris")

    title.pack()

    totalCellWidth = 45
    totalCellHeight = 45
    gridLineThickness = 5

    gameBoard = tk.Canvas(root, width=totalCellWidth * 10, height=totalCellHeight * 20)
    colors = ["blue", "orange"]

    # fill cells
    for x in range(0, 10):
        for y in range(0, 20):
            topLeftX = x * totalCellWidth + gridLineThickness
            topLeftY = (y + 1) * totalCellHeight
            bottomRightX = topLeftX + totalCellWidth - gridLineThickness
            bottomRightY = topLeftY - totalCellHeight + gridLineThickness
            gameBoard.create_rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY, fill=colors[(x + y) % 2])

    # fill vertical gridlines
    for x in range(0, 11):
        topLeftX = x * totalCellWidth
        topLeftY = totalCellHeight * 20 + gridLineThickness
        bottomRightX = topLeftX + gridLineThickness
        bottomRightY = 0
        gameBoard.create_rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY, fill="black")

    # fill horizontal gridlines
    for y in range(0, 21):
        topLeftX = 0
        topLeftY = y * totalCellHeight + gridLineThickness
        bottomRightX = totalCellWidth * 10 + gridLineThickness
        bottomRightY = y * totalCellHeight
        rect = gameBoard.create_rectangle(topLeftX, topLeftY, bottomRightX, bottomRightY, fill="green")
        # This is how to change the color of a rectangle once it's already been created
        gameBoard.itemconfig(rect, fill="black")

    gameBoard.pack()

    root.mainloop()