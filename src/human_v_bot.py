from mydlgo import agent
from mydlgo import goboard_slow
from mydlgo import gotypes
from mydlgo.utils import print_board, print_move, point_from_coordinate
from six.moves import input


def main():
    board_size = 9
    game = goboard_slow.GameState.new_game(board_size)
    bot = agent.RandomBot()

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        if game.next_player == gotypes.Player.BLACK:
            human_move = input("-- ")
            point = point_from_coordinate(human_move.strip())
            move = goboard_slow.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        if not game.is_valid_move(move) or move.is_pass:
            continue
        if move.is_resign:
            print(f"{game.next_player} resigned, {game.next_player.other} win!")
            break
        game = game.apply_move(move)


if __name__ == "__main__":
    main()
