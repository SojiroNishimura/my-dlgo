from __future__ import annotations  # type: ignore
from abc import ABC
from enum import Enum
from typing import Any, Optional, Union

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
    CLEAR_BOARD = "clear_board"
    KOMI = "komi"
    PLAY = "play"
    GENMOVE = "genmove"


# Just an interface for callers of this library
class Point(ABC):
    @property
    def row(self) -> int:
        raise NotImplementedError()

    @property
    def col(self) -> int:
        raise NotImplementedError()


# Just an interface for callers of this library
class Player(ABC):
    @property
    def BLACK(self) -> Union[int, str]:
        raise NotImplementedError()

    @property
    def WHITE(self) -> Union[int, str]:
        raise NotImplementedError()

    @staticmethod
    def is_black(player: Union[Player, int, str]) -> bool:
        val = player.value if isinstance(player, Enum) else player
        if (isinstance(val, int) and val == 1) or (isinstance(val, str) and val.lower() == Color.BLACK):
            return True
        else:
            return False


class Color(Enum):
    BLACK = "black"
    WHITE = "white"


class Vertex:
    def __init__(self, row: int, col: str, is_pass=False):
        self.row = row
        self.col = col
        self.pass_ = "pass" if is_pass else None

    def __str__(self):
        return f"{self.col}{self.row}"

    @staticmethod
    def from_point(p: Point) -> Vertex:
        return Vertex(row=p.row, col=COLS[p.col - 1])


class Command:
    def __init__(self, command_type: CommandType, id: Optional[int] = None, arg: Optional[Any] = None):
        self.id = id if id is not None else None
        self.command_type = command_type
        self.arg = arg

    @staticmethod
    def boardsize(id: Optional[int], size: int) -> Command:
        if size < 1 or MAX_ROW < size:
            raise ValueError(f"Board size is too big, must be 1 <= 19: {size}")
        return Command(CommandType.BOARDSIZE, id, arg=size)

    @staticmethod
    def clearBoard(id: Optional[int]) -> Command:
        return Command(CommandType.CLEAR_BOARD, id)

    @staticmethod
    def komi(id: Optional[int], komi: float) -> Command:
        return Command(CommandType.KOMI, id, arg=komi)

    @staticmethod
    def play(player: Player, id: Optional[int], point: Point) -> Command:
        color = Color.BLACK if Player == Player.BLACK else Color.WHITE
        v = Vertex.from_point(point)
        return Command(CommandType.PLAY, id, arg=f"{color} {v}")

    @staticmethod
    def genmove(id: Optional[int], color: Color) -> Command:
        return Command(CommandType.GENMOVE, id, arg=color)

    def __str__(self):
        return f"{self.command_type} {self.id if self.id is not None else ''} {self.arg}"


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
