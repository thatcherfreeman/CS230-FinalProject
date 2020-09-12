from game.piece.WallKicks import WallKicks

TWELVE_CW_KICKS = [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)]
TWELVE_CCW_KICKS = [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]

THREE_CW_KICKS = [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
THREE_CCW_KICKS = [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]

SIX_CW_KICKS = [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
SIX_CCW_KICKS = [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]

NINE_CW_KICKS = [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
NINE_CCW_KICKS = [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]

TWELVE_KICKS = WallKicks(TWELVE_CW_KICKS, TWELVE_CCW_KICKS)
THREE_KICKS = WallKicks(THREE_CW_KICKS, THREE_CCW_KICKS)
SIX_KICKS = WallKicks(SIX_CW_KICKS, SIX_CCW_KICKS)
NINE_KICKS = WallKicks(NINE_CW_KICKS, NINE_CCW_KICKS)
