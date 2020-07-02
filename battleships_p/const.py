from collections import namedtuple

SIZE = 10
LINE_LENGTH = (SIZE * 3) + 3
EMPTY = "."
SHIP = "$"
HIT = "X"
MISS = "M"
SUNK = "Sunk"

SEPERATOR = "  "
BOARD_SEPERATOR = "  --|--  "

PROMPT = "-->"

START_SHIPS = [5,4,3,2,1]

Point = namedtuple("Point", "x y")
Ship = namedtuple("Ship", "position length orientation")
