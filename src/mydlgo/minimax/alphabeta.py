import random
from typing import List, Callable

from mydlgo.agent import Agent
from mydlgo.goboard import GameState, Move
from mydlgo.gotypes import Player


MAX_SCORE = 999999
MIN_SCORE = -999999


def alpha_beta_result(
    game_state: GameState, max_depth: int, best_black: int, best_white: int, eval_fn: Callable
) -> int:
    if game_state.is_over():
        return MAX_SCORE if game_state.winner() == game_state.next_player else MIN_SCORE

    if max_depth == 0:
        return eval_fn(game_state)

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = alpha_beta_result(next_state, max_depth - 1, best_black, best_white, eval_fn)
        our_result = -opponent_best_result

        if our_result > best_so_far:
            best_so_far = our_result
        if game_state.next_player == Player.WHITE:
            if best_so_far > best_white:
                best_white = best_so_far
            outcome_for_black = -best_so_far
            if outcome_for_black < best_black:
                return best_so_far
        elif game_state.next_player == Player.BLACK:
            if best_so_far > best_black:
                best_black = best_so_far
            outcome_for_white = -best_so_far
            if outcome_for_white < best_white:
                return best_so_far
    return best_so_far


class AlphaBetaAgent(Agent):
    def __init__(self, max_depth: int, eval_fn: Callable):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state: GameState):
        best_moves: List[Move] = []
        best_score = MIN_SCORE
        best_black = MIN_SCORE
        best_white = MIN_SCORE
        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            # Since our opponent plays next, figure out their best
            # possible outcome from there.
            opponent_best_outcome = alpha_beta_result(next_state, self.max_depth, best_black, best_white, self.eval_fn)
            # Our outcome is the opposite of our opponent's outcome.
            our_best_outcome = -opponent_best_outcome
            if len(best_moves) == 0 or our_best_outcome > best_score:
                # This is the best move so far.
                best_moves = [possible_move]
                best_score = our_best_outcome
                if game_state.next_player == Player.BLACK:
                    best_black = best_score
                elif game_state.next_player == Player.WHITE:
                    best_white = best_score
            elif our_best_outcome == best_score:
                # This is as good as our previous best move.
                best_moves.append(possible_move)
        # For variety, randomly select among all equally good moves.
        return random.choice(best_moves)
