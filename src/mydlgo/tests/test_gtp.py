import pytest

from mydlgo.gtp import CommandType, Command, Color, Point, Vertex


@pytest.fixture(scope="module")
def P():
    from typing import NamedTuple

    P = NamedTuple("P", [("row", int), ("col", int)])
    return P


@pytest.mark.parametrize("size", [9, 13, 19])
def test_boardsize_with_valid_size(size):
    assert Command.boardsize(size).to_string() == f"{CommandType.BOARDSIZE.value} {size}"


@pytest.mark.parametrize("size", [0, 20])
def test_boardsize_with_invalid_size(size):
    with pytest.raises(ValueError):
        Command.boardsize(size)


def test_clear_board():
    assert Command.clear_board().to_string() == f"{CommandType.CLEAR_BOARD.value}"


@pytest.mark.parametrize("color", ["Black", "White"])
def test_genmove_with_str(color):
    assert Command.genmove(color).to_string() == f"{CommandType.GENMOVE.value} {color.lower()}"


@pytest.mark.parametrize("color", [Color.BLACK, Color.WHITE])
def test_genmove_with_color(color):
    assert Command.genmove(color).to_string() == f"{CommandType.GENMOVE.value} {color.value}"


@pytest.mark.parametrize("komi", [0, 7.5])
def test_komi(komi):
    assert Command.komi(komi).to_string() == f"{CommandType.KOMI.value} {komi}"


@pytest.mark.parametrize("player", [Color.BLACK, 1, "Black"])
def test_player_is_black(player):
    assert Color.is_black(player) is True


@pytest.mark.parametrize("player", [Color.WHITE, 2, "White"])
def test_player_is_white(player):
    assert Color.is_black(player) is False


@pytest.mark.parametrize("point", [(1, 19), "A1", "T19", "pass"])
def test_point_can_be_converted_to_vertex(P, point):
    p = P(row=point[0], col=point[1]) if Point.is_point(point) else point
    v = Vertex.from_point(p)
    assert isinstance(v, Vertex)


@pytest.mark.parametrize("player, point", [(Color.BLACK, (1, 1)), (1, (4, 16)), ("Black", (19, 19))])
def test_play_legal_move_black(P, player, point):
    p = P(row=point[0], col=point[1])
    v = Vertex.from_point(p)
    assert Command.play(player, p).to_string() == f"{CommandType.PLAY.value} {Color.BLACK.value} {v}"


@pytest.mark.parametrize("player, point", [(Color.WHITE, (1, 1)), (2, (4, 16)), ("White", (19, 19))])
def test_play_legal_move_white(P, player, point):
    p = P(row=point[0], col=point[1])
    v = Vertex.from_point(p)
    assert Command.play(player, p).to_string() == f"{CommandType.PLAY.value} {Color.WHITE.value} {v}"


@pytest.mark.parametrize("player", [Color.BLACK, Color.WHITE])
def test_play_pass(player):
    assert Command.play(player, "pass").to_string() == f"{CommandType.PLAY.value} {player.value} pass"
