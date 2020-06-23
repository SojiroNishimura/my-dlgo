import pytest

from mydlgo.gtp import CommandType, Command, Color


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


@pytest.mark.parametrize("komi", [0, 6.5, 7.5])
def test_komi(komi):
    assert Command.komi(komi).to_string() == f"{CommandType.KOMI.value} {komi}"
