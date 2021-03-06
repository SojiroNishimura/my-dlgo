from six.moves import input

from mydlgo.goboard import GameState, Move
from mydlgo.gotypes import Player, Point
from mydlgo.minimax import AlphaBetaAgent
from mydlgo.utils import print_board, print_move, point_from_coordinate


BOARD_SIZE = 5


def capture_diff(game_state: GameState):
    black_stones = 0
    white_stones = 0
    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            p = Point(r, c)
            color = game_state.board.get_player_at(p)
            if color == Player.BLACK:
                black_stones += 1
            elif color == Player.WHITE:
                white_stones += 1
    diff = black_stones - white_stones
    return diff if game_state.next_player == Player.BLACK else -diff


def main():
    game = GameState.new_game(BOARD_SIZE)
    bot = AlphaBetaAgent(2, capture_diff)

    while not game.is_over():
        print_board(game.board)
        if game.next_player == Player.BLACK:
            human_move = input("-- ")
            if human_move.find("pass") != -1:
                move = Move.pass_turn()
            elif human_move.find("resign") != -1:
                move = Move.resign()
            else:
                point = point_from_coordinate(human_move.strip())
                move = Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__ == "__main__":
    main()
