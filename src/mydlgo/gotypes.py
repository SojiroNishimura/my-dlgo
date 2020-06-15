from __future__ import annotations
from enum import Enum
from collections import namedtuple
from typing import List


class Player(Enum):
    Black = 1
    White = 2

    @property
    def other(self) -> Player:
        return Player.Black if self == Player.White else Player.White


class Point(namedtuple("Point", "row col")):
    def neighbors(self) -> List[Point]:
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]
