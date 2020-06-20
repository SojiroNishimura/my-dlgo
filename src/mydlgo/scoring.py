from __future__ import absolute_import
from collections import namedtuple
from typing import Dict, List, Set, Tuple, Union, Optional

from .gotypes import Player, Point

# from .goboard import Board, GameState


class Territory:
    def __init__(self, territory_map: Dict[Point, Union[Player, str]]):  # <1>
        self.num_black_territory = 0
        self.num_white_territory = 0
        self.num_black_stones = 0
        self.num_white_stones = 0
        self.num_dame = 0
        self.dame_points = []
        for point, status in territory_map.items():  # <2>
            if status == Player.Black:
                self.num_black_stones += 1
            elif status == Player.White:
                self.num_white_stones += 1
            elif status == "territory_b":
                self.num_black_territory += 1
            elif status == "territory_w":
                self.num_white_territory += 1
            elif status == "dame":
                self.num_dame += 1
                self.dame_points.append(point)


# <1> A `territory_map` splits the board into stones, territory and neutral points (dame).
# <2> Depending on the status of a point, we increment the respective counter.


class GameResult(namedtuple("GameResult", "b w komi")):
    @property
    def winner(self) -> Player:
        return Player.Black if self.b > self.w + self.komi else Player.White

    @property
    def winning_margin(self) -> int:
        return abs(self.b - (self.w + self.komi))

    def __str__(self):
        w = self.w + self.komi
        if self.b > w:
            return "B+%.1f" % (self.b - w,)
        return "W+%.1f" % (w - self.b,)


""" evaluate_territory:
Map a board into territory and dame.

Any points that are completely surrounded by a single color are
counted as territory; it makes no attempt to identify even
trivially dead groups.
"""


# def evaluate_territory(board: Board) -> Territory:
def evaluate_territory(board) -> Territory:
    status: Dict[Point, Union[Player, str]] = {}
    for r in range(1, board.num_rows + 1):
        for c in range(1, board.num_cols + 1):
            p = Point(row=r, col=c)
            if p in status:  # <1>
                continue
            stone = board.get_player_at(p)
            if stone is not None:  # <2>
                status[p] = stone  # Add Player color as the holder of the point
            else:
                group, neighbors = _collect_region(p, board)
                if len(neighbors) == 1:  # <3>
                    neighbor_stone = neighbors.pop()
                    fill_with = "territory_b" if neighbor_stone == Player.Black else "territory_w"
                else:
                    fill_with = "dame"  # <4>
                for pos in group:
                    status[pos] = fill_with
    return Territory(status)


# <1> Skip the point, if you already visited this as part of a different group.
# <2> If the point is a stone, add it as status.
# <3> If a point is completely surrounded by black or white stones, count it as territory.
# <4> Otherwise the point has to be a neutral point, so we add it to dame.
# end::scoring_evaluate_territory[]


""" _collect_region:

Find the contiguous section of a board containing a point. Also
identify all the boundary points.
"""


def _collect_region(
    # start_pos: Point, board: Board, visited: Dict[Point, bool] = None
    start_pos: Point,
    board,
    visited: Dict[Point, bool] = None,
) -> Tuple[List[Point], Set[Optional[Player]]]:
    if visited is None:
        visited = {}
    if start_pos in visited:
        return [], set()

    all_points = [start_pos]
    all_borders = set()
    visited[start_pos] = True
    here = board.get_player_at(start_pos)
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for delta_r, delta_c in deltas:
        next_p = Point(row=start_pos.row + delta_r, col=start_pos.col + delta_c)
        if not board.is_on_grid(next_p):
            continue
        neighbor = board.get_player_at(next_p)
        if neighbor == here:
            points, borders = _collect_region(next_p, board, visited)
            all_points += points
            all_borders |= borders
        else:
            all_borders.add(neighbor)
    return all_points, all_borders


# def compute_game_result(game_state: GameState) -> GameResult:
def compute_game_result(game_state) -> GameResult:
    territory = evaluate_territory(game_state.board)
    return GameResult(
        territory.num_black_territory + territory.num_black_stones,
        territory.num_white_territory + territory.num_white_stones,
        komi=7.5,
    )
