from __future__ import annotations  # type: ignore
from enum import Enum, auto
from typing import Any, Optional

from mydlgo.gotypes import Player, Point

"""
See: http://www.lysator.liu.se/~gunnar/gtp/gtp2-spec-draft2/gtp2-spec.html
"""

COLS = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]
MAX_ROW = 19


class CommandType(Enum):
    PROTOCOL_VERSION = "protocol_version"
    NAME = "name"
    VERSION = "version"
    KNOWN_COMMAND = "known_command"
    LIST_COMMANDS = "list_commands"
    QUIT = "quit"
    BOARDSIZE = "boardsize"
    CLEAR_BOARD = "ClearBoard"
    KOMI = "komi"
    PLAY = "play"
    GENMOVE = "genmove"


class Color(Enum):
    BLACK = "Black"
    WHITE = "White"


class Vertex:
    def __init__(self, col: str, row: int, is_pass=False):
        self.col = col
        self.row = row
        self.pass_ = "pass" if is_pass else None

    def __str__(self):
        return f"{self.col}{self.row}"

    @staticmethod
    def from_point(point: Point) -> Vertex:
        pass


class Command:
    def __init__(self, command_type: CommandType, id: Optional[int] = None, arg: Optional[Any] = None):
        self.id = id if id is not None else None
        self.command_type = command_type
        self.arg = arg

    @staticmethod
    def boardsize(size: int) -> Command:
        return Command(CommandType.BOARDSIZE, arg=size)

    @staticmethod
    def clearBoard() -> Command:
        return Command(CommandType.CLEAR_BOARD)

    @staticmethod
    def komi(komi: float) -> Command:
        return Command(CommandType.KOMI, arg=komi)

    @staticmethod
    def play(player: Player, point: Point) -> Command:
        color = Color.BLACK if Player == Player.BLACK else Color.WHITE
        v = Vertex.from_point(point)
        return Command(CommandType.PLAY, arg=f"{color} {v}")

    @staticmethod
    def genmove(color: Color) -> Command:
        return Command(CommandType.GENMOVE, arg=color)


"""
3.2.1 Simple Entities
int
An int is an unsigned integer in the interval $0 <= x <=
2^{31} - 1$.
float
A float is a floating point number representable by a 32 bit IEEE 754 float.
string
A string is a sequence of printable, non-whitespace characters. Strings are case sensitive.
vertex
A vertex is a board coordinate consisting of one letter and one number, as defined in section 2.11, or the string ``pass''. Vertices are not case sensitive. Examples: ``B13'', ``j11''.
color
A color is one of the strings ``white'' or ``w'' to denote white, or ``black'' or ``b'' to denote black. Colors are not case sensitive.
move
A move is the combination of one color and one vertex, separated by space. Moves are not case sensitive. Examples: ``white h10'', ``B F5'', ``w pass''.
boolean
A boolean is one of the strings ``false'' and ``true''.

"""
