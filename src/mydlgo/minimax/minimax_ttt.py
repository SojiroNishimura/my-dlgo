import random
from enum import Enum
from typing import List

from mydlgo.agent import Agent
from mydlgo.goboard import Move, GameState


class GameResult(Enum):
    Loss = 1
    Draw = 2
    Win = 3


def reverse_game_result(result: GameResult) -> GameResult:
    if result == GameResult.Win:
        return GameResult.Loss
    elif result == GameResult.Loss:
        return GameResult.Win
    else:
        return GameResult.Draw


def best_result(game_state: GameState) -> GameResult:
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.Win
        elif game_state.winner() is None:
            return GameResult.Draw
        else:
            return GameResult.Loss

    best_result_so_far = GameResult.Loss
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state)
        our_result = reverse_game_result(opponent_best_result)
        if our_result.value > best_result_so_far.value:
            best_result_so_far = our_result

    return best_result_so_far


class MinimaxAgent(Agent):
    def select_move(self, game_state: GameState) -> Move:
        winning_moves: List[Move] = []
        draw_moves: List[Move] = []
        losing_moves: List[Move] = []

        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = best_result(next_state)
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            if our_best_outcome == GameResult.Win:
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.Draw:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)

        if len(winning_moves) > 0:
            return random.choice(winning_moves)
        elif len(draw_moves) > 0:
            return random.choice(draw_moves)
        else:
            return random.choice(losing_moves)
