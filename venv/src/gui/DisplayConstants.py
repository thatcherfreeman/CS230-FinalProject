from piece.standard.StandardColor import StandardColor

# TODO: move these constants since they are only for the main display grid?
CELL_WIDTH = 4
CELL_HEIGHT = 2
GRID_LINE_THICKNESS = 1

EMPTY_CELL_COLOR = "gray" # TODO: replace with with a call to ColorMapper

# TODO: Tweak for prettiness
COLOR_MAP = {
    StandardColor.CYAN: "cyan",
    StandardColor.BLUE: "blue",
    StandardColor.GREEN: "green",
    StandardColor.ORANGE: "orange",
    StandardColor.PURPLE: "purple",
    StandardColor.RED: "red",
    StandardColor.YELLOW: "yellow",
    StandardColor.NONE: "gray"
}
