import random
from typing import Optional, Union

from mydlgo.gotypes import Player, Point


def to_python(state: Optional[Player]) -> Union[Player, str]:
    if state is None:
        return "None"
    return Player.BLACK if state == Player.BLACK else Player.WHITE


MAX63 = 0x7FFFFFFFFFFFFFFF

table = {}
empty_board = 0

for row in range(1, 20):
    for col in range(1, 20):
        for state in (None, Player.BLACK, Player.WHITE):
            code = random.randint(0, MAX63)
            table[(Point(row, col), state)] = code

print("from .gotypes import Player, Point")
print("")
print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
print("")
print("HASH_CODE = {")
for (pt, state), hash_code in table.items():
    print(f"    ({pt}, {to_python(state)}): {hash_code},")
print("}")
print("")
print(f"EMPTY_BOARD = {random.randint(empty_board, MAX63)}")
