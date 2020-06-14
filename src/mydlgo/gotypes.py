import enum
from collections import namedtuple


class Player(enum.Enum):
    Black = 1
    White = 2

    @property
    def other(self):
        return Player.Black if self == Player.White else Player.White


class Point(namedtuple("Point", "row col")):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]
